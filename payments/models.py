from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from jobs.models import Job


class Payment(models.Model):
    """Payment model for tracking payments from customers"""
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_payment', 'Mobile Payment'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True,
                           help_text="Link to specific job (optional)")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='paid')
    notes = models.TextField(blank=True, help_text="Payment notes or reference number")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.customer.name} - ${self.amount} ({self.get_status_display()})"

    def get_status_display_class(self):
        """Return CSS class for status display"""
        status_classes = {
            'paid': 'badge-success',
            'unpaid': 'badge-danger',
            'partial': 'badge-warning',
        }
        return status_classes.get(self.status, 'badge-light')
