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
        
class CustomUserUpdateForm(forms.ModelForm):
    DOB = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )

    class Meta:
        model = get_user_model()  # Use the custom User model
        fields = ("username", "email", "DOB")  # Fields to update

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Check if another user exists with the same username
        if get_user_model().objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return username
