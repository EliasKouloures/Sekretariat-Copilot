from __future__ import annotations

import json
from pathlib import Path

from services.prompt_library import PromptLibraryService


def test_prompt_library_preserves_seed_order(tmp_path: Path) -> None:
    seed_path = tmp_path / "seed.json"
    seed_path.write_text(
        json.dumps(
            [
                {"title": "Z Prompt", "body": "Last"},
                {"title": "A Prompt", "body": "First"},
            ]
        ),
        encoding="utf-8",
    )

    service = PromptLibraryService(
        library_path=tmp_path / "library.json",
        seed_path=seed_path,
    )

    prompts = service.list_prompts()

    assert [item.title for item in prompts] == ["Z Prompt", "A Prompt"]


def test_prompt_library_derives_title_for_new_prompt(tmp_path: Path) -> None:
    service = PromptLibraryService(
        library_path=tmp_path / "library.json",
        seed_path=tmp_path / "missing-seed.json",
    )

    saved = service.save_prompt("Write a calm school reply.\nUse British English.")

    assert saved.title == "Write a calm school reply"
    assert service.get_prompt(saved.title).body.startswith("Write a calm school reply")


def test_prompt_library_merges_missing_seed_prompts_into_existing_library(tmp_path: Path) -> None:
    seed_path = tmp_path / "seed.json"
    seed_path.write_text(
        json.dumps(
            [
                {"title": "Prompt One", "body": "Body one"},
                {"title": "Prompt Two", "body": "Body two"},
            ]
        ),
        encoding="utf-8",
    )
    library_path = tmp_path / "library.json"
    library_path.write_text(
        json.dumps(
            [{"title": "Custom Prompt", "body": "Custom body"}, {"title": "Prompt One", "body": "Older body"}]
        ),
        encoding="utf-8",
    )

    service = PromptLibraryService(
        library_path=library_path,
        seed_path=seed_path,
    )

    prompts = service.list_prompts()

    assert [item.title for item in prompts] == ["Prompt One", "Prompt Two", "Custom Prompt"]
    assert service.get_prompt("Prompt One").body == "Older body"


def test_prompt_library_puts_seed_prompts_first_and_drops_legacy_defaults(tmp_path: Path) -> None:
    seed_path = tmp_path / "seed.json"
    seed_path.write_text(
        json.dumps(
            [
                {"title": "Prompt One", "body": "Body one"},
                {"title": "Prompt Two", "body": "Body two"},
            ]
        ),
        encoding="utf-8",
    )
    library_path = tmp_path / "library.json"
    library_path.write_text(
        json.dumps(
            [
                {
                    "title": "Draft a calm reply",
                    "body": "Draft a calm, professional reply in British English. Keep it clear, polite, and easy to copy into an email.",
                },
                {"title": "Custom Prompt", "body": "Custom body"},
            ]
        ),
        encoding="utf-8",
    )

    service = PromptLibraryService(
        library_path=library_path,
        seed_path=seed_path,
    )

    prompts = service.list_prompts()

    assert [item.title for item in prompts] == ["Prompt One", "Prompt Two", "Custom Prompt"]
