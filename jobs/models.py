from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer


class Job(models.Model):
    """Job model for tracking seamstress work"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField(help_text="Job description and details")
    measurements = models.TextField(blank=True, help_text="Customer measurements")
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Additional notes about the job")
    
    # File attachments
    image1 = models.ImageField(upload_to='job_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='job_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='job_images/', blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.name} - {self.description[:50]}"

    @property
    def is_overdue(self):
        """Check if job is overdue"""
        from datetime import date
        return self.due_date < date.today() and self.status in ['pending', 'in_progress']

    @property
    def total_payments(self):
        """Return total payments received for this job"""
        return self.payment_set.aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    @property
    def outstanding_payment(self):
        """Return outstanding payment amount for this job"""
        return self.payment_set.filter(
            status='unpaid'
        ).aggregate(total=models.Sum('amount'))['total'] or 0

    def get_status_display_class(self):
        """Return CSS class for status display"""
        status_classes = {
            'pending': 'badge-warning',
            'in_progress': 'badge-info',
            'completed': 'badge-success',
            'delivered': 'badge-secondary',
        }
        return status_classes.get(self.status, 'badge-light')
