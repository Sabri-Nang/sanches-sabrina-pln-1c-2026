# Detector de Discurso de Odio en Tweets (Español)

Este es un MVP (Producto Mínimo Viable) para detectar discurso de odio en tweets en español utilizando el modelo [delarosajav95/HateSpeech-BETO-cased-v2](https://huggingface.co/delarosajav95/HateSpeech-BETO-cased-v2) de Hugging Face.

## Cómo usar localmente

1. Clone este repositorio
2. Instale las dependencias: `pip install -r requirements.txt`
3. Ejecute la aplicación: `python app.py`
4. Abra en su navegador la URL que se muestra (generalmente http://127.0.0.1:7860)

## Despliegue en Hugging Face Spaces

Esta aplicación está diseñada para desplegarse fácilmente en [Hugging Face Spaces](https://huggingface.co/spaces). Solo necesita:

1. Crear un nuevo Space de tipo Gradio
2. Copiar estos archivos (app.py, requirements.txt) al repositorio del Space
3. El Space se construirá y desplegará automáticamente

## Modelo utilizado

- **Modelo**: delarosajav95/HateSpeech-BETO-cased-v2
- **Arquitectura**: BETO (BERT en español) fine-tuneado para clasificación de discurso de odio
- **Idioma**: Español
- **Entrada**: Texto corto (tweets)
- **Salida**: Etiqueta de discurso de odio y puntuación de confianza

## Ejemplos de uso

- "Odio a todos los inmigrantes, deberían desaparecer." → Probabilidad alta de discurso de odio
- "Me encanta el nuevo parque del barrio, es muy bonito." → Probabilidad baja de discurso de odio

## Limitaciones

- El modelo está entrenado para detectar discurso de odio general, puede no capturar todas las formas específicas de violencia.
- El contexto y el sarcasmo pueden afectar la precisión.
- Se recomienda usar este modelo como una herramienta de apoyo, no como decisión final.

## Licencia

Este proyecto se proporciona bajo la licencia MIT.