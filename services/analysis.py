from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from uuid import uuid4

from core.models import (
    AnalysisResult,
    Case,
    CaseStatus,
    ClarifyingQuestion,
    ConfidenceLevel,
    ExtractedRecord,
    InputAsset,
    QuestionPriority,
    SourceMode,
    TaskType,
)
from core.text import normalise_whitespace, parse_dates, title_case_name

NAME_WORD_RE = "[A-Za-z][A-Za-z'\\u2019-]+"
NAME_PATTERN = rf"{NAME_WORD_RE}(?: {NAME_WORD_RE})+"


@dataclass(slots=True)
class AnalysisContext:
    combined_text: str
    source_mode: SourceMode
    assets: list[InputAsset]
    workflow_hint: str | None = None
    ocr_used: bool = False
    low_quality: bool = False
    anchor_date: date = field(default_factory=lambda: datetime.now(UTC).date())
    extra_warnings: list[str] | None = None


class AnalysisService:
    def analyse(self, context: AnalysisContext) -> AnalysisResult:
        text = normalise_whitespace(context.combined_text)
        detected_task = self.detect_task_type(text)
        warnings = list(context.extra_warnings or [])
        task_type = detected_task
        hinted_task = self.parse_workflow_hint(context.workflow_hint)
        if hinted_task is not None:
            task_type = hinted_task
            if hinted_task != detected_task:
                warnings.append(
                    f"Workflow override '{hinted_task.value}' conflicts with the message, which looks like a '{detected_task.value}' task."
                )
        multi_child = self.is_multi_child(text)
        dates, date_warnings = parse_dates(text, context.anchor_date)
        warnings.extend(date_warnings)

        extracted = ExtractedRecord(
            id=f"record_{uuid4().hex[:12]}",
            case_id="",
            student_name=self.extract_student_name(text),
            class_name=self.extract_class_name(text),
            guardian_name=self.extract_guardian_name(text),
            date_from=dates[0] if dates else None,
            date_to=dates[1]
            if len(dates) > 1
            else (dates[0] if task_type == TaskType.ABSENCE and dates else None),
            reason=self.extract_reason(text, task_type),
            request_type=self.request_type_for(task_type),
            meeting_topic=self.extract_meeting_topic(text)
            if task_type == TaskType.SCHEDULE
            else None,
            notes=self.make_case_note(text, task_type),
        )

        contradictions = self.detect_contradictions(task_type, dates, text)
        warnings.extend(contradictions)
        missing_fields = self.missing_fields(task_type, extracted)
        reply_required = self.reply_required(text, task_type)

        confidence_score = self.confidence_score(
            ocr_used=context.ocr_used,
            low_quality=context.low_quality,
            contradictions=contradictions,
            missing_fields=missing_fields,
            relative_date_warnings=date_warnings,
        )
        confidence = self.confidence_level(confidence_score)

        if multi_child:
            warnings.append("Multi-child messages are not supported in the MVP.")

        status = CaseStatus.READY
        if multi_child:
            status = CaseStatus.BLOCKED
            confidence = ConfidenceLevel.LOW
        elif warnings or missing_fields:
            status = CaseStatus.NEEDS_REVIEW

        case = Case(
            id=f"case_{uuid4().hex[:12]}",
            task_type=task_type,
            source_mode=context.source_mode,
            status=status,
            confidence=confidence,
            reply_required=reply_required,
            source_summary=self.build_source_summary(context),
            warnings=warnings,
        )
        extracted.case_id = case.id
        for asset in context.assets:
            asset.case_id = case.id

        questions = self.build_questions(task_type, missing_fields)
        return AnalysisResult(
            case=case,
            extracted_record=extracted,
            input_assets=context.assets,
            warnings=warnings,
            confidence_score=confidence_score,
            missing_fields=missing_fields,
            clarifying_questions=[question.question_text for question in questions],
            source_summary=case.source_summary,
        )

    def parse_workflow_hint(self, workflow_hint: str | None) -> TaskType | None:
        if not workflow_hint:
            return None
        try:
            return TaskType(workflow_hint)
        except ValueError:
            return None

    def detect_task_type(self, text: str) -> TaskType:
        lowered = text.lower()
        absence_score = self._keyword_score(
            lowered,
            ("absent", "absence", "off sick", "stomach illness", "won't be in", "unwell", "miss school"),
        )
        schedule_score = self._keyword_score(
            lowered,
            ("meeting", "schedule", "reschedule", "availability", "appointment"),
        )
        triage_score = self._keyword_score(
            lowered,
            ("form", "document", "attached", "application", "consent"),
        )
        reply_score = self._keyword_score(
            lowered,
            (
                "reply",
                "respond",
                "response",
                "explanation",
                "outraged",
                "complaint",
                "concerned",
                "unfair",
                "how dare",
                "demand",
            ),
        )
        if "homework" in lowered:
            reply_score += 2
        if "grade" in lowered or "grades" in lowered:
            reply_score += 2

        if absence_score >= max(schedule_score, triage_score, reply_score) and absence_score > 0:
            return TaskType.ABSENCE
        if schedule_score >= max(absence_score, triage_score, reply_score) and schedule_score > 0:
            return TaskType.SCHEDULE
        if triage_score >= max(absence_score, schedule_score, reply_score) and triage_score > 0:
            return TaskType.TRIAGE
        return TaskType.REPLY

    def _keyword_score(self, text: str, keywords: tuple[str, ...]) -> int:
        return sum(1 for keyword in keywords if keyword in text)

    def is_multi_child(self, text: str) -> bool:
        lowered = text.lower()
        return any(
            phrase in lowered
            for phrase in (
                "both my children",
                "our children",
                "my children",
                "two children",
                "siblings",
                "for leo and",
                "for mia and",
            )
        )

    def extract_student_name(self, text: str) -> str | None:
        patterns = [
            rf"(?:student|pupil)\s*(?:name|named|called)?\s*[:\-]?\s*[\"“”']?({NAME_PATTERN})[\"“”']?",
            rf"(?:student|pupil)\s+(?:named|called)\s*[\"“”']?({NAME_PATTERN})[\"“”']?",
            rf"[\"“”']?({NAME_PATTERN})[\"“”']?\s+from\s+class\s+[0-9]{{1,2}}[A-Z]?\b",
            rf"for\s+[\"“”']?({NAME_PATTERN})[\"“”']?",
            rf"({NAME_PATTERN})\s+in\s+(?:Year|Class)\s+[0-9]{{1,2}}[A-Z]?\b",
            rf"({NAME_PATTERN})\s+(?:will be|is|was)\s+(?:absent|off sick|not attending)",
            rf"({NAME_PATTERN})\s+is\s+(?:unwell|ill|sick)",
        ]
        return self._match_name(text, patterns)

    def extract_guardian_name(self, text: str) -> str | None:
        patterns = [
            rf"(?:kind regards|best regards|regards|many thanks|thanks|sincerely),?\s*\n+\s*({NAME_PATTERN})(?=\s*(?:\n|$))",
            rf"(?:mother|father|parent|guardian)\s+name\s*[:\-]\s*({NAME_PATTERN})",
            rf"i am\s+({NAME_PATTERN})",
            rf"from\s*:\s*({NAME_PATTERN})",
        ]
        extracted = self._match_name(text, patterns)
        if extracted:
            return extracted
        return self._signature_name(text)

    def extract_class_name(self, text: str) -> str | None:
        match = re.search(r"\b(?:Year|Class)\s+[0-9]{1,2}[A-Z]?\b", text, flags=re.IGNORECASE)
        if not match:
            return None
        raw = normalise_whitespace(match.group(0))
        pieces = raw.split()
        if len(pieces) == 2:
            return f"{pieces[0].capitalize()} {pieces[1].upper()}"
        return raw

    def extract_reason(self, text: str, task_type: TaskType) -> str | None:
        lowered = text.lower()
        if task_type == TaskType.REPLY:
            if "homework" in lowered and ("grade" in lowered or "grades" in lowered):
                return "Homework load and grading concern"
            if "homework" in lowered:
                return "Homework concern"
            if "grade" in lowered or "grades" in lowered:
                return "Grading concern"
            complaint_patterns = [
                r"(?:complaint|concern)\s+about\s+([A-Za-z0-9 ,'-]{4,80})",
                r"(?:outraged|unhappy|concerned)\s+about\s+([A-Za-z0-9 ,'-]{4,80})",
            ]
            for pattern in complaint_patterns:
                match = re.search(pattern, text, flags=re.IGNORECASE)
                if match:
                    return normalise_whitespace(match.group(1)).rstrip(".")
            return None
        if task_type == TaskType.SCHEDULE:
            return None
        patterns = [
            r"(?:because(?: of)?|due to|with)\s+([A-Za-z0-9 ,'-]{4,80})",
            r"reason\s*[:\-]\s*([A-Za-z0-9 ,'-]{4,80})",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return normalise_whitespace(match.group(1)).rstrip(".")
        if task_type == TaskType.ABSENCE and "sick" in text.lower():
            return "Illness"
        return None

    def extract_meeting_topic(self, text: str) -> str | None:
        patterns = [
            r"meeting (?:about|regarding)\s+([A-Za-z0-9 ,'-]{4,80})",
            r"subject\s*:\s*([A-Za-z0-9 ,'-]{4,80})",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return normalise_whitespace(match.group(1)).rstrip(".")
        return None

    def request_type_for(self, task_type: TaskType) -> str:
        mapping = {
            TaskType.ABSENCE: "absence_notice",
            TaskType.REPLY: "reply_draft",
            TaskType.SCHEDULE: "scheduling_summary",
            TaskType.TRIAGE: "document_triage",
        }
        return mapping[task_type]

    def detect_contradictions(self, task_type: TaskType, dates: list[str], text: str) -> list[str]:
        warnings: list[str] = []
        if len(set(dates)) > 2:
            warnings.append("Several date candidates were found and may conflict.")
        if len(dates) >= 2 and dates[0] > dates[1]:
            warnings.append("Date range appears to be reversed.")
        lowered = text.lower()
        if (
            task_type == TaskType.ABSENCE
            and "tomorrow" in lowered
            and any(marker in lowered for marker in ("last week", "yesterday"))
        ):
            warnings.append("The message mixes relative dates from different periods.")
        return warnings

    def missing_fields(self, task_type: TaskType, record: ExtractedRecord) -> list[str]:
        required_by_task = {
            TaskType.ABSENCE: ("student_name", "date_from"),
            TaskType.REPLY: ("student_name",),
            TaskType.SCHEDULE: ("student_name", "meeting_topic"),
            TaskType.TRIAGE: ("student_name", "request_type"),
        }
        missing: list[str] = []
        for field_name in required_by_task[task_type]:
            if not getattr(record, field_name):
                missing.append(field_name)
        return missing

    def reply_required(self, text: str, task_type: TaskType) -> bool:
        lowered = text.lower()
        if "no reply needed" in lowered or "for information only" in lowered:
            return False
        return task_type in {TaskType.ABSENCE, TaskType.REPLY}

    def confidence_score(
        self,
        *,
        ocr_used: bool,
        low_quality: bool,
        contradictions: list[str],
        missing_fields: list[str],
        relative_date_warnings: list[str],
    ) -> int:
        score = 100
        if ocr_used:
            score -= 20
        if low_quality:
            score -= 15
        score -= 20 * len(missing_fields)
        score -= 20 * len(contradictions)
        score -= 15 * len(relative_date_warnings)
        return max(0, min(100, score))

    def confidence_level(self, score: int) -> ConfidenceLevel:
        if score >= 85:
            return ConfidenceLevel.HIGH
        if score >= 60:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    def build_source_summary(self, context: AnalysisContext) -> str:
        parts: list[str] = []
        if context.combined_text:
            if context.source_mode == SourceMode.NOTE:
                parts.append("Manual note")
            elif context.source_mode == SourceMode.TEXT:
                parts.append("Pasted text")
            else:
                parts.append("Direct text")
        for asset in context.assets:
            label = asset.asset_type.value.upper()
            parts.append(f"{label} via {asset.parse_method.value}")
        return ", ".join(parts) if parts else "No source summary"

    def build_questions(
        self, task_type: TaskType, missing_fields: list[str]
    ) -> list[ClarifyingQuestion]:
        templates = {
            "student_name": "Please confirm the pupil's full name.",
            "date_from": "Please confirm the date or date range involved.",
            "meeting_topic": "Please confirm the meeting topic or purpose.",
            "request_type": "Please confirm what action or document is required.",
        }
        questions: list[ClarifyingQuestion] = []
        for field_name in missing_fields[:3]:
            questions.append(
                ClarifyingQuestion(
                    id=f"question_{uuid4().hex[:12]}",
                    case_id="",
                    question_text=templates.get(
                        field_name, f"Please confirm the {field_name.replace('_', ' ')}."
                    ),
                    priority=QuestionPriority.HIGH
                    if task_type != TaskType.TRIAGE
                    else QuestionPriority.MEDIUM,
                )
            )
        return questions

    def make_case_note(self, text: str, task_type: TaskType) -> str:
        first_sentence = text.split(".")[0]
        return normalise_whitespace(
            f"{task_type.value.title()} case summary: {first_sentence[:120]}"
        ).rstrip(".")

    def _match_name(self, text: str, patterns: list[str]) -> str | None:
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)
            if match:
                return title_case_name(match.group(1))
        return None

    def _signature_name(self, text: str) -> str | None:
        lines = [line.strip(" ,") for line in text.splitlines() if line.strip()]
        skip_prefixes = ("ask ", "call ", "phone ", "please ", "he'll", "she'll", "teacher ", "mr. ", "ms. ")
        for line in reversed(lines):
            if line.lower().startswith(skip_prefixes):
                continue
            if re.fullmatch(NAME_PATTERN, line, flags=re.IGNORECASE):
                return title_case_name(line)
        return None
