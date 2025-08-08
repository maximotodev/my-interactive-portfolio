import os
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """
        This method is called when the Django app is initialized.
        """
        
        # --- THIS IS THE NEW AND CRITICAL PART ---
        # Initialize the AI Assistant singleton when the server starts.
        # This builds the knowledge base once for high performance.
        # We check for a specific environment variable to avoid running this
        # during other management commands like 'makemigrations'.
        if os.environ.get('RUN_MAIN') or os.environ.get('IS_RENDER'):
            from . import ai_service
            # Initialize the singleton, which builds and embeds the KB
            ai_service.KnowledgeBaseService()
        # We only want this to run on the Render server, not locally
        is_render = os.getenv('IS_RENDER', 'False') == 'True'
        if is_render:
            try:
                # Import necessary modules here to avoid circular imports
                from django.contrib.auth import get_user_model
                
                User = get_user_model()
                username = os.getenv('DJANGO_SUPERUSER_USERNAME')
                password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

                if username and password:
                    # Check if a user with this username already exists
                    if not User.objects.filter(username=username).exists():
                        print(f"Creating superuser '{username}' for production...")
                        User.objects.create_superuser(
                            username=username,
                            password=password
                        )
                        print("Superuser created successfully.")
                    else:
                        print(f"Superuser '{username}' already exists. Skipping creation.")
            except Exception as e:
                print(f"An error occurred during superuser creation: {e}")