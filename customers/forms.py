from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    """Form for creating and editing customers with voice input support"""
    
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control voice-input',
                'placeholder': 'Customer name',
                'data-voice-field': 'name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control voice-input',
                'rows': 3,
                'placeholder': 'Customer address',
                'data-voice-field': 'address'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control voice-input',
                'rows': 4,
                'placeholder': 'Additional notes about the customer',
                'data-voice-field': 'notes'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make name field required
        self.fields['name'].required = True
