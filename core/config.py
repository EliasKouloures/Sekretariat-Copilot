from __future__ import annotations

import os
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class BackendProfile:
    provider_name: str = "lm_studio"
    base_url: str = "http://127.0.0.1:1234/v1"
    model_id: str = "meta-llama-3.1-8b-instruct"
    temperature: float = 0.2
    max_tokens: int = 900
    context_limit: int = 8192
    timeout_seconds: int = 120
    supports_vision: bool = False
    api_key: str = "local"


@dataclass(slots=True)
class StorageConfig:
    database_path: str = "data/secure-ai-ssistant.db"
    retain_audit_days: int = 30
    save_raw_inputs: bool = False


@dataclass(slots=True)
class InputLimits:
    max_assets: int = 5
    max_file_mb: int = 10
    max_pdf_pages: int = 10


@dataclass(slots=True)
class FeatureFlags:
    enable_intranet_mode: bool = False
    allow_export_bundle: bool = False
    show_privacy_panel: bool = True


@dataclass(slots=True)
class AppConfig:
    title: str = "Secure-AI-ssistant"
    locale: str = "en-GB"
    bind_host: str = "127.0.0.1"
    bind_port: int = 8501
    backend: BackendProfile = field(default_factory=BackendProfile)
    storage: StorageConfig = field(default_factory=StorageConfig)
    limits: InputLimits = field(default_factory=InputLimits)
    features: FeatureFlags = field(default_factory=FeatureFlags)


ENV_MAP: dict[str, tuple[str, str]] = {
    "SECURE_AI_SSISTANT_TITLE": ("app", "title"),
    "SECURE_AI_SSISTANT_BIND_HOST": ("app", "bind_host"),
    "SECURE_AI_SSISTANT_BIND_PORT": ("app", "bind_port"),
    "SECURE_AI_SSISTANT_DATABASE_PATH": ("app", "database_path"),
    "SECURE_AI_SSISTANT_BACKEND_PROVIDER": ("backend", "provider_name"),
    "SECURE_AI_SSISTANT_BACKEND_BASE_URL": ("backend", "base_url"),
    "SECURE_AI_SSISTANT_BACKEND_MODEL_ID": ("backend", "model_id"),
    "SECURE_AI_SSISTANT_BACKEND_TEMPERATURE": ("backend", "temperature"),
    "SECURE_AI_SSISTANT_BACKEND_MAX_TOKENS": ("backend", "max_tokens"),
    "SECURE_AI_SSISTANT_BACKEND_CONTEXT_LIMIT": ("backend", "context_limit"),
    "SECURE_AI_SSISTANT_BACKEND_TIMEOUT_SECONDS": ("backend", "timeout_seconds"),
    "SECURE_AI_SSISTANT_BACKEND_SUPPORTS_VISION": ("backend", "supports_vision"),
    "SECURE_AI_SSISTANT_BACKEND_API_KEY": ("backend", "api_key"),
    "SECURE_AI_SSISTANT_RETAIN_AUDIT_DAYS": ("storage", "retain_audit_days"),
    "SECURE_AI_SSISTANT_SAVE_RAW_INPUTS": ("storage", "save_raw_inputs"),
    "SECURE_AI_SSISTANT_MAX_ASSETS": ("limits", "max_assets"),
    "SECURE_AI_SSISTANT_MAX_FILE_MB": ("limits", "max_file_mb"),
    "SECURE_AI_SSISTANT_MAX_PDF_PAGES": ("limits", "max_pdf_pages"),
    "SECURE_AI_SSISTANT_ENABLE_INTRANET_MODE": ("features", "enable_intranet_mode"),
    "SECURE_AI_SSISTANT_ALLOW_EXPORT_BUNDLE": ("features", "allow_export_bundle"),
    "SECURE_AI_SSISTANT_SHOW_PRIVACY_PANEL": ("features", "show_privacy_panel"),
}


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _coerce_int(value: Any) -> int:
    return int(value)


def _coerce_float(value: Any) -> float:
    return float(value)


def load_config(path: str | Path | None = None, env: Mapping[str, str] | None = None) -> AppConfig:
    env_map = dict(os.environ if env is None else env)
    raw = _load_toml(path)

    app_section = raw.get("app", {})
    backend_section = raw.get("backend", {})
    storage_section = raw.get("storage", {})
    limits_section = raw.get("limits", {})
    features_section = raw.get("features", {})

    for env_key, (section, option) in ENV_MAP.items():
        if env_key not in env_map:
            continue
        target = {
            "app": app_section,
            "backend": backend_section,
            "storage": storage_section,
            "limits": limits_section,
            "features": features_section,
        }[section]
        target[option] = env_map[env_key]

    storage = StorageConfig(
        database_path=str(app_section.get("database_path", storage_section.get("database_path", "data/secure-ai-ssistant.db"))),
        retain_audit_days=_coerce_int(storage_section.get("retain_audit_days", 30)),
        save_raw_inputs=_coerce_bool(storage_section.get("save_raw_inputs", False)),
    )
    backend = BackendProfile(
        provider_name=str(backend_section.get("provider_name", "lm_studio")),
        base_url=str(backend_section.get("base_url", "http://127.0.0.1:1234/v1")),
        model_id=str(backend_section.get("model_id", "meta-llama-3.1-8b-instruct")),
        temperature=_coerce_float(backend_section.get("temperature", 0.2)),
        max_tokens=_coerce_int(backend_section.get("max_tokens", 900)),
        context_limit=_coerce_int(backend_section.get("context_limit", 8192)),
        timeout_seconds=_coerce_int(backend_section.get("timeout_seconds", 120)),
        supports_vision=_coerce_bool(backend_section.get("supports_vision", False)),
        api_key=str(backend_section.get("api_key", "local")),
    )
    limits = InputLimits(
        max_assets=_coerce_int(limits_section.get("max_assets", 5)),
        max_file_mb=_coerce_int(limits_section.get("max_file_mb", 10)),
        max_pdf_pages=_coerce_int(limits_section.get("max_pdf_pages", 10)),
    )
    features = FeatureFlags(
        enable_intranet_mode=_coerce_bool(features_section.get("enable_intranet_mode", False)),
        allow_export_bundle=_coerce_bool(features_section.get("allow_export_bundle", False)),
        show_privacy_panel=_coerce_bool(features_section.get("show_privacy_panel", True)),
    )
    return AppConfig(
        title=str(app_section.get("title", "Secure-AI-ssistant")),
        locale=str(app_section.get("locale", "en-GB")),
        bind_host=str(app_section.get("bind_host", "127.0.0.1")),
        bind_port=_coerce_int(app_section.get("bind_port", 8501)),
        backend=backend,
        storage=storage,
        limits=limits,
        features=features,
    )


def _load_toml(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        default_path = Path("config.toml")
        if not default_path.exists():
            return {}
        path = default_path
    target = Path(path)
    if not target.exists():
        return {}
    return tomllib.loads(target.read_text(encoding="utf-8"))
