import gradio as gr
from transformers import pipeline

# Load the hate speech detection model
model_name = "delarosajav95/HateSpeech-BETO-cased-v2"
classifier = pipeline("text-classification", model=model_name)

def detect_hate_speech(text):
    """
    Detect hate speech in the given text.
    Returns a dictionary with labels and scores for Gradio Label component.
    """
    if not text.strip():
        return {"No texto proporcionado": 1.0}
    
    # Get prediction
    result = classifier(text)[0]
    # Model returns LABEL_0 (no hate) or LABEL_1 (hate)
    # Map to human-readable labels
    hate_score = result['score'] if result['label'] == 'LABEL_1' else 1 - result['score']
    no_hate_score = 1 - hate_score
    
    # Return dict for Gradio Label
    return {
        "Discurso de odio": round(hate_score, 4),
        "No discurso de odio": round(no_hate_score, 4)
    }

# Define the interface
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

# Launch the app
if __name__ == "__main__":
    iface.launch(theme="default")