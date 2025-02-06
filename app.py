from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download')
def download():
    url = request.args.get('url')
    format_type = request.args.get('format')

    if not url or format_type not in ['mp3', 'mp4']:
        return {"error": "Invalid request"}, 400

    # Create downloads folder if not exists
    os.makedirs("downloads", exist_ok=True)

    # Define file format options
    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'mp3' else 'bestvideo+bestaudio',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save file inside downloads/
        'noplaylist': True,
    }

    # Add MP3 conversion settings
    if format_type == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    # Convert to MP3 if required
    if format_type == 'mp3':
        filename = filename.rsplit('.', 1)[0] + '.mp3'  # Change extension to .mp3

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
