from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.db.models import Model
from typing import Tuple

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    DOB: forms.DateField = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )

    class Meta:
        model: type[Model] = User  
        fields: Tuple[str, str, str, str, str] = (
            "username",
            "email",
            "DOB", 
            "password1", 
            "password2")  
        
class CustomUserUpdateForm(forms.ModelForm):
    DOB: forms.DateField = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )

    class Meta:
        model: type[Model] = User  
        fields: Tuple[str,str,str] = ("username", "email", "DOB") 

    def clean_username(self) -> str:
        username: str = self.cleaned_data.get("username")
        if get_user_model().objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return username
