from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from customers.models import Customer
from jobs.models import Job
from payments.models import Payment
from django.db.models import Sum, Count
from datetime import datetime, timedelta


def home(request):
    """Home page - redirect to dashboard if authenticated, otherwise show login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    """Main dashboard showing overview of customers, jobs, and payments"""
    # Get recent stats
    total_customers = Customer.objects.count()
    active_jobs = Job.objects.filter(status__in=['in_progress', 'pending']).count()
    completed_jobs = Job.objects.filter(status='completed').count()
    
    # Recent jobs (last 10)
    recent_jobs = Job.objects.select_related('customer').order_by('-created_at')[:10]
    
    # Overdue jobs
    overdue_jobs = Job.objects.filter(
        due_date__lt=datetime.now().date(),
        status__in=['in_progress', 'pending']
    ).select_related('customer')
    
    # Payment stats
    total_payments = Payment.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    pending_payments = Payment.objects.filter(
        status='unpaid'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'total_customers': total_customers,
        'active_jobs': active_jobs,
        'completed_jobs': completed_jobs,
        'recent_jobs': recent_jobs,
        'overdue_jobs': overdue_jobs,
        'total_payments': total_payments,
        'pending_payments': pending_payments,
    }
    
    return render(request, 'core/dashboard.html', context)
