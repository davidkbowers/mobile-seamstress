from django import forms
from .models import Job
from customers.models import Customer


class JobForm(forms.ModelForm):
    """Form for creating and editing jobs with voice input support"""
    
    class Meta:
        model = Job
        fields = ['customer', 'description', 'measurements', 'due_date', 'status', 'notes', 
                 'image1', 'image2', 'image3']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control voice-input',
                'rows': 4,
                'placeholder': 'Describe the job details',
                'data-voice-field': 'description'
            }),
            'measurements': forms.Textarea(attrs={
                'class': 'form-control voice-input',
                'rows': 3,
                'placeholder': 'Customer measurements',
                'data-voice-field': 'measurements'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control voice-input',
                'rows': 3,
                'placeholder': 'Additional notes',
                'data-voice-field': 'notes'
            }),
            'image1': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'capture': 'environment'
            }),
            'image2': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'capture': 'environment'
            }),
            'image3': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'capture': 'environment'
            }),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Limit customer choices to user's customers
            self.fields['customer'].queryset = Customer.objects.filter(created_by=user)
        
        # Make required fields
        self.fields['customer'].required = True
        self.fields['description'].required = True
        self.fields['due_date'].required = True
