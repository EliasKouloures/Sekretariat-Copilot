from __future__ import annotations

from datetime import date

from core.models import CaseStatus, ConfidenceLevel, SourceMode, TaskType
from services.analysis import AnalysisContext, AnalysisService


def test_detects_absence_and_extracts_fields() -> None:
    service = AnalysisService()
    result = service.analyse(
        AnalysisContext(
            combined_text="Leo Martin in Year 4B will be absent on 2026-03-12 because of stomach illness.\nKind regards,\nSarah Martin",
            source_mode=SourceMode.TEXT,
            assets=[],
            anchor_date=date(2026, 3, 12),
        )
    )

    assert result.case.task_type == TaskType.ABSENCE
    assert result.extracted_record.student_name == "Leo Martin"
    assert result.extracted_record.class_name == "Year 4B"
    assert result.extracted_record.date_from == "2026-03-12"
    assert result.extracted_record.reason == "stomach illness"
    assert result.case.status == CaseStatus.READY
    assert result.case.confidence == ConfidenceLevel.HIGH


def test_missing_dates_generate_questions_and_medium_confidence() -> None:
    service = AnalysisService()
    result = service.analyse(
        AnalysisContext(
            combined_text="Phone note: Leo Martin is unwell and will miss school. Please update the office.",
            source_mode=SourceMode.NOTE,
            assets=[],
            anchor_date=date(2026, 3, 12),
        )
    )

    assert "date_from" in result.missing_fields
    assert result.clarifying_questions
    assert result.case.status == CaseStatus.NEEDS_REVIEW
    assert result.case.confidence == ConfidenceLevel.MEDIUM


def test_multi_child_cases_are_blocked() -> None:
    service = AnalysisService()
    result = service.analyse(
        AnalysisContext(
            combined_text="Both my children, Leo Martin and Mia Martin, will be absent tomorrow.",
            source_mode=SourceMode.TEXT,
            assets=[],
            anchor_date=date(2026, 3, 12),
        )
    )

    assert result.case.status == CaseStatus.BLOCKED
    assert result.case.confidence == ConfidenceLevel.LOW
    assert any("Multi-child" in warning for warning in result.warnings)


def test_contradictions_reduce_confidence() -> None:
    service = AnalysisService()
    result = service.analyse(
        AnalysisContext(
            combined_text="Leo Martin will be absent tomorrow. He was also absent yesterday and last week.",
            source_mode=SourceMode.TEXT,
            assets=[],
            anchor_date=date(2026, 3, 12),
        )
    )

    assert any("mixes relative dates" in warning for warning in result.warnings)
    assert result.confidence_score < 85


def test_complaint_reply_extracts_student_guardian_and_issue_summary() -> None:
    service = AnalysisService()
    result = service.analyse(
        AnalysisContext(
            combined_text=(
                'Hello School Board,\n\n'
                'This is the mother of student named "Johnny Knoxville" from class 8b of your Berlin Mitte School.\n\n'
                "I am outraged over the amount of homework you are giving my son every day, which kills all of his quality time with his family.\n\n"
                "On-top you are also giving him ever worsening grades, which is not fair because my son is the smartest kid in the world!!!\n\n"
                "How dare you treat my son so badly!!!\n\n"
                "I demand an explanation!11!!11!!\n\n"
                "Regards,\nKaren Miller\n\n"
                "Ask Ms. Miller to call teacher Mr. Madison: 030-123456789.\n\n"
                "He'll happily discuss any questions she might have."
            ),
            source_mode=SourceMode.MIXED,
            assets=[],
            anchor_date=date(2026, 3, 17),
        )
    )

    assert result.case.task_type == TaskType.REPLY
    assert result.extracted_record.student_name == "Johnny Knoxville"
    assert result.extracted_record.guardian_name == "Karen Miller"
    assert result.extracted_record.class_name == "Class 8B"
    assert result.extracted_record.reason == "Homework load and grading concern"
    assert result.missing_fields == []


def test_manual_workflow_override_warns_when_content_points_elsewhere() -> None:
    service = AnalysisService()
    result = service.analyse(
        AnalysisContext(
            combined_text=(
                'Hello School Board,\n\n'
                'This is the mother of student named "Johnny Knoxville" from class 8b.\n\n'
                "I demand an explanation for the unfair homework and grading.\n\n"
                "Regards,\nKaren Miller"
            ),
            source_mode=SourceMode.TEXT,
            assets=[],
            workflow_hint="schedule",
            anchor_date=date(2026, 3, 17),
        )
    )

    assert result.case.task_type == TaskType.SCHEDULE
    assert result.extracted_record.student_name == "Johnny Knoxville"
    assert any("Workflow override" in warning for warning in result.warnings)
