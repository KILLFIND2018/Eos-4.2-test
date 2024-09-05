import os
import json
import torch
import logging
from flask import Flask, request, jsonify, send_from_directory, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer, SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Загрузка токена из .env файла
load_dotenv()
token = os.getenv("HUGGINGFACE_HUB_TOKEN")

app = Flask(__name__, static_url_path='/static')

# Настройка логирования
if not os.path.exists('logs'):
    os.makedirs('logs')
file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App Startup')

# Загрузка языковой модели GPT-2
model_name = "gpt2"
llama_tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
llama_model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)

# Загрузка модели и процессора SpeechT5
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts", use_auth_token=token)
speech_model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts", use_auth_token=token)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan", use_auth_token=token)

# Хранение имени последнего аудиофайла
last_audio_file = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions', methods=['GET'])
def get_questions():
    with open('web/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return jsonify(questions)

@app.route('/process', methods=['POST'])
def process():
    global last_audio_file
    data = request.json
    text = data.get('message')

    if not text:
        app.logger.error('No text provided')
        return jsonify({"error": "No text provided"}), 400

    try:
        # Удаление предыдущего аудиофайла
        if last_audio_file and os.path.exists(last_audio_file):
            os.remove(last_audio_file)
            app.logger.info(f'Deleted previous audio file: {last_audio_file}')

        # Генерация текста с помощью GPT-2
        inputs = llama_tokenizer.encode(text, return_tensors='pt')
        outputs = llama_model.generate(inputs, max_length=50)
        generated_text = llama_tokenizer.decode(outputs[0], skip_special_tokens=True)
        app.logger.info(f'Generated text: {generated_text}')

        # Генерация речи с помощью SpeechT5
        inputs = processor(generated_text, return_tensors="pt")
        speaker_embeddings = torch.zeros(1, 512)  # Используем нулевые эмбеддинги для простоты
        with torch.no_grad():
            speech = speech_model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        app.logger.info('Generated speech')

        # Сохранение аудио
        audio_file = "output.wav"
        with open(audio_file, "wb") as f:
            f.write(speech.numpy().tobytes())
        app.logger.info(f'Saved audio file: {audio_file}')

        # Обновление имени последнего аудиофайла
        last_audio_file = audio_file

        response = {
            "reply": generated_text,
            "audio_file": f"/audio/{audio_file}"
        }

        return jsonify(response)

    except Exception as e:
        app.logger.error(f'Error processing message: {str(e)}')
        return jsonify({"error": str(e)}), 500

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(port=8000)
