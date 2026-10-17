# Clipbox – YouTube video downloader

Flask + yt-dlp backend with a clean single-page frontend.

## Run locally
```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000

## Deploy
GitHub Pages only hosts static files, so it can't download videos by itself.
Push this repo to GitHub, then deploy it on Render / Railway / Fly.io
(start command: `gunicorn app:app --timeout 300`). The backend serves the page too.

Optional: host `static/index.html` on GitHub Pages and set `API_BASE` in it
to your backend URL.

## Note
Only download content you own or have permission to save.
