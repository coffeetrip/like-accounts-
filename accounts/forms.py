from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):  # UserCreationForm 상속받음
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
