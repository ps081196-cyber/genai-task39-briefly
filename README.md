---
title: Briefly GenAI Summarizer
emoji: 📝
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# Assignment 39 — GenAI App Deployment

Author: Devendra Singh

## Project
Briefly summarizes pasted text or a UTF-8 .txt upload. It supports bullet summaries, paragraphs and study notes in English or Hindi through Hugging Face Inference Providers. An explicitly labeled offline preview extracts original sentences and works without a token; it is not generative AI.

Architecture: Streamlit UI → input validation → Hugging Face InferenceClient → supported chat model/provider → summary and text download. Preview mode performs sentence ranking locally. No database is required. Input limit: 16,000 characters and at least 20 words. Upload limit: 100 KB.

## Local setup (Python 3.11)
Open a terminal inside this folder:
```bash
python -m venv .venv
```
Windows PowerShell activation:
```powershell
.venv\Scripts\Activate.ps1
```
macOS/Linux activation:
```bash
source .venv/bin/activate
```
Then:
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Open the local URL shown by Streamlit. Click **Load example**, then **Create summary** to try offline preview.

For actual AI output, create a Hugging Face access token with permission to call Inference Providers. Either enter your token in the password field or copy `secrets.example.toml` into `.streamlit/secrets.toml` and replace the placeholder. Select Generative AI. Model support changes; choose a currently available chat model from Hugging Face Inference Providers if the default is unavailable. Inference requires internet and sufficient account credits and is not guaranteed free. The app does not download model weights or require a local GPU.

## Task 1: Streamlit Community Cloud
1. Create a GitHub repository and upload the contents of this folder at repository root, including app.py, core.py, requirements.txt and .streamlit/config.toml. Never upload real secrets, .env or your virtual environment.
2. Sign into https://share.streamlit.io with GitHub and choose **Create app**.
3. Select the repository, branch and entrypoint `app.py`. Choose Python 3.11 in advanced settings if offered.
4. Paste the edited example TOML into the platform's Secrets settings. For public apps, consider leaving out the shared token and letting each visitor supply their own token, because a shared credential permits visitor usage of your credits.
5. Deploy; inspect build logs if it fails.
6. Open the generated live URL and run the validation checklist below. Record the actual URL and screenshots in DEPLOYMENT_RECORD.md. No live URL is supplied in this package because it has not been deployed.

## Task 2: Hugging Face Spaces
The assignment refers to a Streamlit Space. Hugging Face deprecated Streamlit as a built-in SDK; use a Docker Space that runs this same Streamlit application.
1. Sign into https://huggingface.co and create a new Space.
2. Choose **Docker SDK** (blank Docker template is sufficient), a name and desired visibility. Select CPU hardware appropriate to your account; no GPU is needed for this API client.
3. Upload this folder's contents at the Space root, including Dockerfile and README.md. The README frontmatter sets `sdk: docker` and `app_port: 7860`.
4. In Space settings, add HF_TOKEN as a secret and optionally HF_MODEL as a variable. Do not commit a real token. Alternatively visitors can supply their own token in the app.
5. Wait for the image build and app startup. Streamlit listens on 0.0.0.0:7860 as required by this Docker configuration.
6. Open the Space and test both preview and real AI mode. Record the actual Space URL and results. Upload directly or push to the Space's own Git repository; a GitHub repository is not automatically synchronized unless you separately configure synchronization.

## Task 3: Platform comparison
| Aspect | Streamlit Community Cloud | Hugging Face Spaces (Docker) |
|---|---|---|
| Setup | Direct GitHub deployment; select app.py | Dockerfile plus Space README metadata |
| Main advantage | Simple deployment for Python Streamlit apps | Flexible runtime and strong ML demo ecosystem |
| Main limitation | Platform environment/resource limits and less runtime control | Docker configuration adds complexity; hardware and inactivity behavior depend on the plan |
| Secrets | Cloud Secrets using TOML | Space secrets exposed as environment variables |
| Updates | Repository changes trigger deployment | Space Git/upload changes trigger rebuild |
| Choose when | Quickly sharing dashboards or Streamlit prototypes | Hosting ML demonstrations or needing a custom container/runtime |

Both platforms still depend on the external inference service for this app's AI mode. Compare observed startup time and inference latency only after running the same text/model on both; no performance numbers have been invented.

## Validation checklist
- Open the live URL in a fresh browser session; ensure no startup error.
- Load example → offline preview produces three original sentences.
- Valid token/model → Generative AI returns a summary; verify facts against the input.
- Try English and Hindi, and each AI format/length setting.
- Empty or fewer than 20 words → helpful validation error.
- Oversized or invalid UTF-8 upload → error without a crash.
- Invalid token or unavailable model → safe failure message; no credential printed.
- Download summary.txt and check its contents.
- Check narrow/mobile layout and confirm secret files are absent from the repository.

## Tests and limitations
Run `python -m unittest -v`. Tests cover validation, source-preserving preview, missing credentials and the AI request/response contract using a fake client. These tests do not establish live provider availability. AI outputs can contain mistakes. Generation length/language is requested in the prompt and not guaranteed. User text is sent to an external service only in AI mode. Session content is not written to a database. Public deployment with an owner token needs additional authentication/rate limiting before production use.

## Submission
Keep all files inside **GenAI-Task39-DevendraSingh** and ZIP the main folder. Fill the deployment record with actual URLs, screenshots and observations after completing live deployment. Submit the ZIP through your course portal yourself. This project was prepared with AI assistance; do not claim it was unaided work if your course prohibits AI.

## Official references
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
- https://huggingface.co/docs/hub/spaces-sdks-streamlit
- https://huggingface.co/docs/hub/spaces-sdks-docker
- https://huggingface.co/docs/huggingface_hub/package_reference/inference_client
