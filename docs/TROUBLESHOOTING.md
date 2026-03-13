# Troubleshooting

## Backend offline

- Confirm LM Studio is running.
- Confirm the local server is started.
- Confirm `base_url` and `model_id` in `config.toml`.
- Use the Diagnostics panel in the app to inspect reachability and recent errors.

## Wrong model loaded

- Check the model loaded in LM Studio.
- Make sure `model_id` in `config.toml` matches what LM Studio is actually serving.
- Restart the local server after changing models.

## Vision OCR unavailable

- Enable `supports_vision = true` only when the selected local model actually supports image input.
- If vision is unavailable, paste text manually and continue with the text workflow.

## PDF parsing failed

- Check the file size and page count limits in `config.toml`.
- If the PDF is scanned and no vision model is active, paste the text manually or load a vision-capable model.

## Python command not found on macOS

- Run `python3 --version`.
- If `python3` exists, use `python3 -m venv .venv`.
- Do not worry if `python3.12` is missing. That is normal on many Macs.

## Launcher command not found

- Activate the virtual environment first.
- On macOS, run `source .venv/bin/activate`.
- On Windows, run `.venv\Scripts\Activate.ps1`.
- If needed, launch the app directly from `.venv`.

## Windows virtual environment issues

- Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` if PowerShell blocks activation.
- Re-open the shell after Python installation if `py -3.12` is not found immediately.

## The browser still shows an old broken page

- Stop the app.
- Start it again.
- Hard refresh the browser tab.
- If the app was recently restyled, the browser may be showing cached assets.
