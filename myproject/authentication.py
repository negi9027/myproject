# your_app/authentication/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.apps import apps
from rest_framework.response import Response


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        profile = request.data.get('profile')
        
        if not user_id or not password:
            raise AuthenticationFailed('No user_id or password provided')

        try:
            # Dynamically get the model class
            model_class = apps.get_model(app_label="superadmin", model_name=profile)
        except LookupError:
            return Response({"error": f"Invalid profile type: {profile}"}, status=400)

        try:
            # Find user with user_id
            user = model_class.objects.get(user_id=user_id)
        except:
            raise AuthenticationFailed('User not found')

        if user.password != password:  # Replace this with hashed password check
            raise AuthenticationFailed('Invalid password')

        return (user, None)  # Return the user and None (the second part is for optional token)
