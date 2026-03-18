from __future__ import annotations

import html
import json
from uuid import uuid4

import streamlit.components.v1 as components


def render_copy_button(label: str, value: str) -> None:
    safe_label = html.escape(label)
    safe_value = json.dumps(value)
    button_id = f"copy_{uuid4().hex}"
    components.html(
        f"""
        <style>
          html, body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: transparent;
            font-family: Aptos, 'Segoe UI', sans-serif;
          }}
        </style>
        <button id="{button_id}" style="
            border-radius:22px;
            border:2px solid rgba(10,25,47,0.82);
            background:linear-gradient(180deg, rgba(255,255,255,0.97), rgba(244,244,249,0.92));
            color:#0A192F;
            font-family:Aptos, Segoe UI, sans-serif;
            font-size:20px;
            font-weight:700;
            padding:0 18px;
            cursor:pointer;
            width:100%;
            min-height:60px;
            box-shadow:none;
            line-height:1.1;
            letter-spacing:-0.02em;
        ">{safe_label}</button>
        <script>
        const button = document.getElementById({json.dumps(button_id)});
        button.addEventListener("click", async () => {{
          await navigator.clipboard.writeText({safe_value});
          button.textContent = "Copied";
          setTimeout(() => button.textContent = {json.dumps(safe_label)}, 1200);
        }});
        </script>
        """,
        height=60,
    )
