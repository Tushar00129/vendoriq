from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Vendor
import re


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class VendorLoginForm(AuthenticationForm):
    """
    Custom login form with user-friendly labels and basic validation.
    Keeps Django authentication semantics (username/password) while presenting
    "Name" to the user as requested.
    """

    username = forms.CharField(
        label="Username",
        required=True,
        min_length=3,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "placeholder": "Enter your username",
                "autofocus": True,
                "inputmode": "text",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        required=True,
        min_length=4,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Enter your password",
            }
        ),
    )

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        # Letters + numbers, but must start with a letter (not an integer).
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", username or ""):
            raise forms.ValidationError(
                "Username can contain letters and numbers, but must start with a letter."
            )
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password") or ""
        if len(password) < 4:
            raise forms.ValidationError("Password must be at least 4 characters.")
        if password.strip() != password:
            raise forms.ValidationError("Password cannot start or end with spaces.")
        return password


class VendorForm(forms.ModelForm):
    name = forms.CharField(
        label="Vendor Name",
        min_length=2,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z][A-Za-z\s&.'-]*$",
                message="Name must use letters and spaces only (no numbers).",
            )
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g., Acme Supplies",
                "autocomplete": "organization",
                "inputmode": "text",
                "pattern": "[A-Za-z][A-Za-z\\s&.'-]*",
                "title": "Use letters and spaces only. Numbers are not allowed.",
            }
        ),
    )

    delivery_rating = forms.DecimalField(
        label="Delivery Rating (1-5)",
        min_value=1,
        max_value=5,
        decimal_places=1,
        max_digits=2,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "1.0 to 5.0",
                "step": "0.1",
                "min": "1",
                "max": "5",
                "inputmode": "decimal",
            }
        ),
    )
    quality_rating = forms.DecimalField(
        label="Quality Rating (1-5)",
        min_value=1,
        max_value=5,
        decimal_places=1,
        max_digits=2,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "1.0 to 5.0",
                "step": "0.1",
                "min": "1",
                "max": "5",
                "inputmode": "decimal",
            }
        ),
    )
    price_rating = forms.DecimalField(
        label="Price Rating (1-5)",
        min_value=1,
        max_value=5,
        decimal_places=1,
        max_digits=2,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "1.0 to 5.0",
                "step": "0.1",
                "min": "1",
                "max": "5",
                "inputmode": "decimal",
            }
        ),
    )
    communication_rating = forms.DecimalField(
        label="Communication Rating (1-5)",
        min_value=1,
        max_value=5,
        decimal_places=1,
        max_digits=2,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "1.0 to 5.0",
                "step": "0.1",
                "min": "1",
                "max": "5",
                "inputmode": "decimal",
            }
        ),
    )

    class Meta:
        model = Vendor
        fields = ("name", "delivery_rating", "quality_rating", "price_rating", "communication_rating")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} form-input".strip()

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        name = re.sub(r"\s+", " ", name)
        if Vendor.objects.filter(name__iexact=name).exists():
            raise ValidationError("A vendor with this name already exists.")
        return name
