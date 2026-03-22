# Copilot Instructions for `ai-term`

## Build, test, and lint commands

### Frontend (`frontend/`)

- Install dependencies: `npm ci`
- Start local dev server: `npm run dev`
- Production build: `npm run build`
- Preview production build locally: `npm run preview`

### Backend (`backend/`)

- Create a local virtualenv with the repo's preferred tool: `uv venv && source .venv/bin/activate`
- Install local backend dependencies as needed for the scripts you are running: `uv pip install dotenv google-genai boto3`
- Package the Lambda deployment zip: `bash build_lambda.sh`
- Manual smoke check for prompt generation: `python term.py`
- Manual prompt-template check: `python prompts.py`
- Manual smoke check for the Lambda handler shape: `python lambda_function.py`
- Deploy the packaged Lambda manually: `python update_lambda.py`

### Current test/lint situation

- There are currently no repository-defined test scripts or lint scripts in `frontend/package.json`, and no dedicated backend test suite is checked in.
- Because there is no test runner configured, there is no supported "single test" command yet; backend validation is currently done with the `if __name__ == "__main__"` entrypoints in `term.py`, `prompts.py`, and `lambda_function.py`.

## High-level architecture

- This repo is a two-part app:
  - `frontend/` is a Svelte 5 + Vite single-page app.
  - `backend/` is an AWS Lambda-style Python service that calls Google's Gemini API.
- The frontend is URL-driven rather than router-driven. `frontend/src/App.svelte` reads `type` and `prompt` from query parameters on mount and on `popstate`, updates browser history on submit, and uses those params as the source of truth for navigation/state restoration.
- `frontend/src/lib/SearchForm.svelte` owns the search UX: it exposes the prompt type picker, validates YouTube inputs, and exports `focusInputElement()` so `App.svelte` can implement the `/` keyboard shortcut and restore focus after navigation.
- `frontend/src/lib/aiService.js` is the only frontend API client. It POSTs `{ prompt_type, term }` to `VITE_REST_ENDPOINT` with `x-api-key`, and `App.svelte` renders the returned `result` as Markdown via `marked`.
- Backend request handling is split cleanly:
  - `backend/lambda_function.py` handles API Gateway/Lambda event parsing, input validation, enum conversion, CORS headers, and JSON response shape.
  - `backend/term.py` handles Gemini client setup, model selection, request assembly, and the actual `generate()` call.
  - `backend/prompts.py` is the prompt catalog and the canonical definition of supported `PromptType` values.
- Deployment is also split across both halves of the app. `.github/workflows/deploy.yml` builds the frontend with Node 24, packages the backend with Python 3.13 + `uv`, updates the Lambda zip, syncs `frontend/dist` to `s3://.../ai`, and invalidates CloudFront.

## Key conventions

- Treat `backend/prompts.py` as the source of truth for prompt types. The exact enum strings there must stay aligned with:
  - the `<option value="...">` entries in `frontend/src/lib/SearchForm.svelte`
  - the default URL parameter handling in `frontend/src/App.svelte`
  - any request payloads sent from `frontend/src/lib/aiService.js`
- Prompt behavior is intentionally centralized in Python. If you add or change a content mode, update both the enum and the prompt template in `backend/prompts.py` before wiring the frontend UI.
- Backend responses are Markdown, not HTML. The frontend relies on `marked` in `App.svelte` to render the backend output, so backend prompt changes should continue returning Markdown-friendly content.
- The frontend build is configured for static hosting with relative asset paths (`base: './'` in `frontend/vite.config.js`). Keep that in mind when changing asset URLs or build assumptions because the deployment workflow syncs the built app into an S3 subpath (`/ai`), not the bucket root.
- The YouTube flow has an important cross-file contract: `SearchForm.svelte` currently validates raw `https://youtu...` links, but `backend/term.py` passes `term` into Gemini as `types.FileData(file_uri=term)`, and the project docs describe YouTube requests as needing a Gemini `file_uri`. If you work on YouTube support, verify the end-to-end contract across frontend validation, backend request assembly, and prompt expectations instead of changing only one side.
- Local backend testing is done through script entrypoints rather than a test harness. `term.py`, `prompts.py`, and `lambda_function.py` each have `__main__` blocks that are the current lightweight way to probe behavior.
