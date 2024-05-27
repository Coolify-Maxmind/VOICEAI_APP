from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from transformers import Wav2Vec2CTCTokenizer, Wav2Vec2ForCTC, Wav2Vec2Processor, TrainingArguments, Wav2Vec2FeatureExtractor, Trainer
import torch
import datetime
import soundfile as sf
import os
import librosa
import csv
import io
app = Flask(__name__)
# Charger le modèle Wav2Vec2 pré-entraîné et le tokenizer
""" try:
    tokenizer = Wav2Vec2CTCTokenizer("vocab.json", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")
    processor = Wav2Vec2Processor.from_pretrained('/src/llms/wav2vec-xlsr-large-darija', tokenizer=tokenizer)
    model=Wav2Vec2ForCTC.from_pretrained('/src/llms/wav2vec-xlsr-large-darija')
except Exception as e:
    app.logger.error(f"Error loading model: {e}")
    raise SystemExit(f"Error loading model: {e}") """
try:
    with open('/src/llms/example.txt', 'r') as file:
        content = file.read()
        print(content)
        
except FileNotFoundError:
    print("Error: The file 'example.txt' was not found.")
    app.logger.error(f"Error loading model: ")
except IOError:
    print("Error: An IOError occurred while handling the file.")


AUDIO_DIR = "audios"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['POST'])
def process_data():
    data = request.get_json()
    response_data = {
        "message": "Data received successfully",
        "received_data": data
    }
    return jsonify(response_data)
@app.route('/transcrib', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = secure_filename(file.filename)
            filepath = os.path.join(AUDIO_DIR, f"audio_{current_datetime}_{filename}")

            # Enregistrer le fichier audio dans le dossier spécifié
            file.save(filepath)
            # Process the file in memory
            #file_content = file.read()
            #audio_bytes = io.BytesIO(file_content)

            input_audio, sr = librosa.load(filepath, sr=16000)

            # tokenize
            input_values = processor(input_audio, return_tensors="pt", padding=True).input_values

            # retrieve logits
            logits = model(input_values).logits

            tokens = torch.argmax(logits, axis=-1)

            # decode using n-gram
            transcription = tokenizer.batch_decode(tokens)

            #with open("transcriptions.csv", "a", newline="",encoding="utf-8") as csvfile:
            #    writer = csv.writer(csvfile)
            #   writer.writerow([filepath, transcription[0]])

            return jsonify({"transcription": transcription[0]})
        except Exception as e:
             
          return jsonify({"transcription": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='3000',debug=True)
