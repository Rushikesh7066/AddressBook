from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip
import os
import youtube_dl

app = Flask(__name__)

# Directory to save downloaded videos
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Helper function to download video from YouTube
def download_video(url):
    options = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
        'format': 'best',
    }
    
    with youtube_dl.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join(DOWNLOAD_DIR, f"{info['id']}.{info['ext']}")

# Route to handle video processing
@app.route('/process_video', methods=['POST'])
def process_video():
    data = request.json
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({'error': 'Video URL is required'}), 400

    try:
        # Download the video
        video_path = download_video(video_url)
        
        # Load the video and trim to 60 seconds
        clip = VideoFileClip(video_path).subclip(0, min(60, VideoFileClip(video_path).duration))

        # Save the processed short video
        short_video_path = os.path.join(DOWNLOAD_DIR, "short_video.mp4")
        clip.write_videofile(short_video_path, codec="libx264")
        
        return jsonify({'message': 'Video processed successfully!', 'short_video_path': short_video_path})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
