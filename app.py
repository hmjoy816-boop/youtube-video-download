import os
import re
import shutil
import tempfile

import yt_dlp
from flask import Flask, jsonify, request, send_file, after_this_request
from flask_cors import CORS

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

YT_REGEX = re.compile(r"^(https?://)?([\w-]+\.)?(youtube\.com|youtu\.be)/.+", re.I)

# Progressive MP4 formats work without ffmpeg (max ~720p).
FORMATS = {
    "best": "best[ext=mp4]/best",
    "720": "best[height<=720][ext=mp4]/best[height<=720]/best",
    "480": "best[height<=480][ext=mp4]/best[height<=480]/best",
    "360": "best[height<=360][ext=mp4]/best[height<=360]/best",
    "audio": "bestaudio[ext=m4a]/bestaudio",
}


def valid_url(url):
    return bool(url and YT_REGEX.match(url.strip()))


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/info")
def info():
    url = request.args.get("url", "").strip()
    if not valid_url(url):
        return jsonify(error="Enter a valid YouTube link."), 400
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "noplaylist": True}) as ydl:
            data = ydl.extract_info(url, download=False)
        return jsonify(
            title=data.get("title"),
            channel=data.get("uploader"),
            duration=data.get("duration"),
            thumbnail=data.get("thumbnail"),
        )
    except Exception:
        return jsonify(error="Couldn't read that video. Check the link and try again."), 400


@app.route("/api/download")
def download():
    url = request.args.get("url", "").strip()
    quality = request.args.get("quality", "best")
    if not valid_url(url) or quality not in FORMATS:
        return jsonify(error="Invalid request."), 400

    tmp = tempfile.mkdtemp()

    @after_this_request
    def cleanup(response):
        shutil.rmtree(tmp, ignore_errors=True)
        return response

    opts = {
        "format": FORMATS[quality],
        "outtmpl": os.path.join(tmp, "%(title).80s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        filename = os.listdir(tmp)[0]
        return send_file(os.path.join(tmp, filename), as_attachment=True, download_name=filename)
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        return jsonify(error="Download failed. Try another quality."), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
