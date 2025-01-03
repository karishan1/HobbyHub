from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(UserCreationForm):
    DOB = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )

    class Meta:
        model = get_user_model()  # Use the custom User model
        fields = ("username", "email", "DOB", "password1", "password2")  # Include DOB
