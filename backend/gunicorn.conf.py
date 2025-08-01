# backend/gunicorn.conf.py
def on_starting(server):
    print("Gunicorn master process is starting. Pre-loading AI model...")
    try:
        from api.views import get_sentence_transformer_model
        get_sentence_transformer_model()
        print("AI model pre-loaded successfully.")
    except Exception as e:
        print(f"Error pre-loading AI model: {e}")