import os
from transformers import AutoModelForCausalLM, AutoTokenizer, SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from dotenv import load_dotenv

load_dotenv()

def download_models():
    token = os.getenv("HUGGINGFACE_HUB_TOKEN")

    # Загрузка языковой модели GPT-2
    model_name = "gpt2"
    llama_model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)
    llama_tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
    llama_model.save_pretrained(model_name)
    llama_tokenizer.save_pretrained(model_name)
    print("GPT-2 model downloaded successfully.")
    
    # Загрузка модели и процессора SpeechT5
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts", use_auth_token=token)
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts", use_auth_token=token)
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan", use_auth_token=token)
    
    processor.save_pretrained("speecht5_tts_processor")
    model.save_pretrained("speecht5_tts_model")
    vocoder.save_pretrained("speecht5_hifigan_vocoder")

    print("SpeechT5 model and components downloaded successfully.")

if __name__ == "__main__":
    download_models()
