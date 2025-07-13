# backend/gunicorn.conf.py

# This function is a Gunicorn hook that runs once, when the master process starts.
def on_starting(server):
    """
    The AI model pre-loading is disabled for deployment on Render's free tier.
    """
    print("Gunicorn master process starting. AI model pre-loading is disabled.")
    # """
    # Pre-load the Sentence Transformer model into memory before the workers are forked.
    # This is crucial for platforms with low memory like Render's free tier.
    # """
    # print("Gunicorn master process is starting. Pre-loading AI model...")
    # try:
    #     from api.views import get_sentence_transformer_model
    #     # This call will load the model and cache it in the master process.
    #     # When workers are forked, they will inherit this cached model via copy-on-write memory.
    #     get_sentence_transformer_model()
    #     print("AI model pre-loaded successfully.")
    # except Exception as e:
    #     print(f"Error pre-loading AI model: {e}")