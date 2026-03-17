from __future__ import annotations

from typing import Any


def queue_reset(state: Any) -> None:
    state["reset_requested"] = True


def queue_clarification_input_clear(state: Any) -> None:
    state["clear_clarification_input_requested"] = True


def apply_clarification_input_clear(state: Any) -> None:
    state["clarification_answers_input"] = ""
    state["clear_clarification_input_requested"] = False


def apply_reset(state: Any) -> None:
    raw_nonce = state.get("file_uploader_nonce", 0)
    next_nonce = raw_nonce if isinstance(raw_nonce, int) else int(str(raw_nonce))
    state["case_id"] = None
    state["analysis"] = None
    state["outputs"] = None
    state["error_message"] = None
    state["pasted_text_input"] = ""
    state["manual_note_input"] = ""
    state["file_uploader_nonce"] = next_nonce + 1
    state["reset_requested"] = False
    queue_clarification_input_clear(state)
