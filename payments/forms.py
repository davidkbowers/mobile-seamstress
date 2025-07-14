from django import forms
from .models import Payment
from customers.models import Customer
from jobs.models import Job


class PaymentForm(forms.ModelForm):
    """Form for creating and editing payments"""
    
    class Meta:
        model = Payment
        fields = ['customer', 'job', 'amount', 'date', 'payment_method', 'status', 'notes']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control'
            }),
            'job': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Payment amount'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control voice-input',
                'rows': 3,
                'placeholder': 'Payment notes or reference',
                'data-voice-field': 'notes'
            }),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Limit customer choices to user's customers
            self.fields['customer'].queryset = Customer.objects.filter(created_by=user)
            self.fields['job'].queryset = Job.objects.filter(created_by=user).select_related('customer')
        
        # Make job field optional
        self.fields['job'].required = False
        self.fields['job'].empty_label = "No specific job"
        
        # Make required fields
        self.fields['customer'].required = True
        self.fields['amount'].required = True
        self.fields['date'].required = True
