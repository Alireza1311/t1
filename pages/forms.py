from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 6, "class": "form-control form-control-lg"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "message":
                field.widget.attrs.update({"class": "form-control form-control-lg"})


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg"})
    )
