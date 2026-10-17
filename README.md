# Clipbox – YouTube video downloader

A Flask + yt-dlp app. The Python server serves the page and does the downloading.

> GitHub Pages cannot run Python, so this app can't work there.
> Use one of the options below.

## Option 1 – Run on GitHub (Codespaces)
1. On the repo page: **Code → Codespaces → Create codespace on main**
2. In the terminal that opens, run: `python app.py`
3. Click **Open in Browser** on the port 5000 popup (or the **Ports** tab).

## Option 2 – Run on your computer
```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000

## Option 3 – Deploy on Render
New → Web Service → pick this repo. It reads `render.yaml` automatically.
(YouTube may block cloud server IPs; running locally is the most reliable.)

## Notes
- If you see "Sign in to confirm you're not a bot", export your YouTube cookies to
  `cookies.txt` and set the environment variable `COOKIES_FILE=cookies.txt`.
- Keep yt-dlp updated: `pip install -U yt-dlp`.
- Only download videos you own or have permission to save.
