from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """Customer model for managing seamstress clients"""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Additional notes about the customer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def active_jobs_count(self):
        """Return count of active jobs for this customer"""
        return self.job_set.filter(status__in=['pending', 'in_progress']).count()

    @property
    def total_jobs_count(self):
        """Return total count of jobs for this customer"""
        return self.job_set.count()

    @property
    def outstanding_balance(self):
        """Return total outstanding payment balance"""
        from payments.models import Payment
        return Payment.objects.filter(
            customer=self,
            status='unpaid'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
