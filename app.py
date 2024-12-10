from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
import uuid
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Это разрешит CORS для всех маршрутов

def run_ffmpeg(rtsp_url, output_dir, output_file):
    command = [
        'ffmpeg', 
        '-rtsp_transport', 'tcp',
        '-analyzeduration', '10000000',
        '-probesize', '10000000',
        '-i', rtsp_url,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-f', 'hls',
        '-hls_time', '10',
        '-hls_list_size', '0',
        '-hls_segment_filename', f"{output_dir}/segment_%03d.ts",
        output_file
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {str(e)}")

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    rtsp_url = data.get('rtsp_url')

    if not rtsp_url:
        return jsonify({'error': 'RTSP URL is required'}), 400

    output_dir = f"/app/output/{uuid.uuid4()}"
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"{output_dir}/output.m3u8"

    # Start FFmpeg in a separate thread
    threading.Thread(target=run_ffmpeg, args=(rtsp_url, output_dir, output_file)).start()

    return jsonify({'message': 'Conversion started', 'hls_link': f"/output/{os.path.basename(output_dir)}/output.m3u8"}), 202

@app.route('/output/<path:filename>', methods=['GET'])
def get_output_file(filename):
    output_dir = "/app/output"
    return send_from_directory(output_dir, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
