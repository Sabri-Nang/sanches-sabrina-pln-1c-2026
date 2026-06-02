import gradio as gr
from transformers import pipeline
import time
import threading

model_name = "delarosajav95/HateSpeech-BETO-cased-v2"
classifier = pipeline("text-classification", model=model_name)

def detect_hate_speech(text):
    if not text.strip():
        return {"No texto proporcionado": 1.0}
    result = classifier(text)[0]
    hate_score = result['score'] if result['label'] == 'LABEL_1' else 1 - result['score']
    no_hate_score = 1 - hate_score
    return {
        "Discurso de odio": round(hate_score, 4),
        "No discurso de odio": round(no_hate_score, 4)
    }

iface = gr.Interface(
    fn=detect_hate_speech,
    inputs=gr.Textbox(lines=2, placeholder="Ingrese un tweet para analizar...", label="Tweet"),
    outputs=gr.Label(num_top_classes=2, label="Resultado de detección de discurso de odio"),
    title="Detector de Discurso de Odio en Tweets (Español)",
    description="Este modelo detecta discurso de odio en texto en español utilizando el modelo BETO fine-tuneado. Ingrese un tweet y obtendrá la probabilidad de que contenga discurso de odio.",
    examples=[
        ["Odio a todos los inmigrantes, deberían desaparecer."],
        ["Me encanta el nuevo parque del barrio, es muy bonito."],
        ["Los políticos son unos corruptos, merecen ir a la cárcel."],
        ["Hoy fui al cine con mis amigos y nos divertimos mucho."]
    ]
)

def launch_and_stop():
    iface.launch(theme="default", share=False, prevent_thread_lock=True)
    
thread = threading.Thread(target=launch_and_stop)
thread.start()
time.sleep(5)
print("Launch attempted (no error expected)")
