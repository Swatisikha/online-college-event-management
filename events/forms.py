from django import forms
from .models import Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'student_name',
            'email',
            'phone_number',
            'college_roll_number',
        ]

        widgets = {
            'student_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number'
            }),
            'college_roll_number': forms.TextInput(attrs={
                'placeholder': 'Enter your college roll number'
            }),
        }