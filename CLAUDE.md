# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered dictionary and encyclopedia web application with a dual architecture:
- **Frontend**: Svelte + Vite single-page application
- **Backend**: Python AWS Lambda function using Google's Gemini API

The application generates various types of content (dictionary definitions, encyclopedia articles, YouTube video summaries) in multiple languages using specialized prompts.

## Architecture

### Frontend (Svelte SPA)
- **Location**: `frontend/`
- **Framework**: Svelte 5 with Vite
- **Entry point**: `frontend/src/App.svelte`
- **Core service**: `frontend/src/lib/aiService.js` handles API communication
- **URL-based state**: Uses query parameters (`?type=...&prompt=...`) for navigation
- **Markdown rendering**: Uses `marked` library to render AI responses
- **Keyboard shortcut**: `/` key focuses the search input

### Backend (AWS Lambda)
- **Location**: `backend/`
- **Entry point**: `backend/lambda_function.py` (AWS Lambda handler)
- **Core logic**: `backend/term.py` contains the `generate()` function
- **Prompts**: `backend/prompts.py` defines prompt templates via `PromptType` enum
- **AI Provider**: Google Gemini API (via `google-genai` SDK)
- **Model selection**: Uses different models for standard text vs. YouTube video analysis

### Prompt Types
Defined in `backend/prompts.py`:
- `DICTIONARY_EN`: ESL-focused English word definitions
- `ENCYCLOPEDIA_EN`: Detailed encyclopedia articles in English
- `ENCYCLOPEDIA_DE`: Detailed encyclopedia articles in German
- `YOUTUBE_EN`: YouTube video summaries (first 5 minutes) in English
- `YOUTUBE_DE`: YouTube video summaries (first 5 minutes) in German

YouTube prompts use video metadata with a 300-second time window and 0.1 fps sampling.

## Development Commands

### Frontend Development
```bash
cd frontend
npm install                # Install dependencies
npm run dev               # Start development server
npm run build             # Build for production (output: frontend/dist/)
npm run preview           # Preview production build
```

### Backend Development (Local Testing)
**Note**: This project uses **uv** as the Python package manager.

```bash
cd backend
uv venv                   # Create virtual environment
source .venv/bin/activate # Activate venv
uv pip install dotenv google-genai  # Install dependencies

# Run locally for testing
python term.py            # Test generate() function directly
python lambda_function.py # Test Lambda handler locally
```

### Backend Deployment (AWS Lambda)
```bash
cd backend
./build_lambda.sh         # Build Lambda deployment package
python update_lambda.py   # Build and upload to AWS Lambda
```

The `build_lambda.sh` script:
- Uses `uv pip install` to install dependencies for `aarch64-manylinux2014` platform (Python 3.13)
- Cross-compiles packages for AWS Lambda's ARM64 architecture
- Packages dependencies: `dotenv>=0.9.9`, `google-genai>=1.56.0`
- Creates `lambda_function.zip` with all Python files and dependencies

**Python Package Manager**: This project uses **uv** (not pip) for all Python package management, including local development and Lambda packaging.

## Environment Variables

### Backend (`backend/.env`)
- `GOOGLE_API_KEY`: Google Gemini API key
- `GOOGLE_MODEL`: Main Gemini model (e.g., `gemini-2.5-flash`)
- `GOOGLE_MODEL_YOUTUBE`: Gemini model for YouTube video analysis
- `AWS_LAMBDA_FUNCTION_NAME`: ARN of the Lambda function
- `AWS_REGION`: AWS region (e.g., `us-east-1`)
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: AWS credentials
- `S3_BUCKET_NAME`, `CLOUDFRONT_DISTRIBUTION_ID`: For frontend deployment

### Frontend (`frontend/.env.local`)
- `VITE_REST_ENDPOINT`: Backend API endpoint
- `VITE_REST_API_KEY`: API key for backend authentication

## Deployment

### Frontend Deployment
GitHub Actions workflow (`.github/workflows/deploy.yml`) automatically deploys on push to `main`:
1. Builds the frontend with Vite
2. Deploys to GitHub Pages
3. Syncs to AWS S3 bucket
4. Invalidates CloudFront cache

### Backend Deployment
Manual deployment via `python backend/update_lambda.py`:
1. Runs `build_lambda.sh` to create deployment package
2. Uploads to AWS Lambda using boto3

## Key Implementation Details

### Response Flow
1. User enters term in `SearchForm.svelte`
2. `App.svelte` updates URL query params and calls `askAi()`
3. `aiService.js` sends POST request to Lambda endpoint
4. Lambda handler validates input and calls `generate(prompt_type, term)`
5. `generate()` constructs prompt and calls Gemini API
6. Response rendered as Markdown in `App.svelte`

### Error Handling
- Frontend: Displays errors in `.error` div
- Backend: Returns structured error responses with status codes (400, 500)
- Lambda validates prompt_type and term length (max 1000 chars)

### CORS Configuration
Lambda responses include CORS headers:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Headers: Content-Type`
- `Access-Control-Allow-Methods: POST, OPTIONS`

## Testing and Debugging

### Local Testing Pattern
Both `term.py` and `prompts.py` have `if __name__ == "__main__"` blocks for testing:
- Test different prompt types by uncommenting examples
- Output written to `backend/answer.md` for inspection

### YouTube URL Handling
YouTube prompts expect a video URI that's been processed by Gemini's file API, not raw YouTube URLs. The `term` parameter for YouTube types should be a `file_uri` from Gemini's video upload API.
