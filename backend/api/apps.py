# backend/api/apps.py

import os
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    # Add this 'ready' method
    def ready(self):
        """
        This method is called when the Django app is initialized.
        We use it to run our one-time superuser creation logic.
        """
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