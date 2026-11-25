from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
import importlib.util

# Import transcribe_audio from audio-transcribe.py (hyphenated filename)
spec = importlib.util.spec_from_file_location("audio_transcribe", "audio-transcribe.py")
audio_transcribe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio_transcribe)
transcribe_audio = audio_transcribe.transcribe_audio

app = Flask(__name__)
CORS(app)  # Enable CORS for browser requests


@app.route('/')
def index():
    """Serve the HTML recording interface"""
    return send_from_directory('.', 'index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Receive audio file and transcribe it.
    Expects multipart/form-data with 'audio' file field.
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get model name from request (default to 'base')
        model_name = request.form.get('model', 'base')
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp_file:
            audio_file.save(tmp_file.name)
            temp_path = tmp_file.name
        
        try:
            # Transcribe the audio
            transcript = transcribe_audio(temp_path, model_name=model_name)
            
            return jsonify({
                'success': True,
                'transcript': transcript
            })
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🎤 Starting Audio Transcription Server...")
    print("📝 Open http://localhost:5000 in your browser to record audio")
    app.run(debug=True, host='0.0.0.0', port=5000)

