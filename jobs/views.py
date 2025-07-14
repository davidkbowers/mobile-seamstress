from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Job
from .forms import JobForm
from customers.models import Customer
import csv


@login_required
def job_list(request):
    """List all jobs with filtering and search"""
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    jobs = Job.objects.filter(created_by=request.user).select_related('customer')
    
    if status_filter:
        jobs = jobs.filter(status=status_filter)
    
    if search_query:
        jobs = jobs.filter(
            Q(description__icontains=search_query) |
            Q(customer__name__icontains=search_query) |
            Q(notes__icontains=search_query)
        )
    
    jobs = jobs.order_by('-created_at')
    
    # Get overdue jobs for alert
    overdue_jobs = Job.objects.filter(
        created_by=request.user,
        status__in=['pending', 'in_progress']
    ).extra(where=["due_date < date('now')"])
    
    context = {
        'jobs': jobs,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Job.STATUS_CHOICES,
        'overdue_count': overdue_jobs.count(),
    }
    return render(request, 'jobs/job_list.html', context)


@login_required
def job_detail(request, pk):
    """Show job details"""
    job = get_object_or_404(Job, pk=pk, created_by=request.user)
    payments = job.payment_set.all().order_by('-date')
    
    context = {
        'job': job,
        'payments': payments,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def job_create(request):
    """Create a new job"""
    if request.method == 'POST':
        form = JobForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, f'Job for "{job.customer.name}" created successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(user=request.user)
        # Pre-select customer if provided in URL
        customer_id = request.GET.get('customer')
        if customer_id:
            try:
                customer = Customer.objects.get(pk=customer_id, created_by=request.user)
                form.initial['customer'] = customer
            except Customer.DoesNotExist:
                pass
    
    context = {
        'form': form,
        'title': 'Add New Job',
    }
    return render(request, 'jobs/job_form.html', context)


@login_required
def job_edit(request, pk):
    """Edit an existing job"""
    job = get_object_or_404(Job, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = JobForm(user=request.user, data=request.POST, files=request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f'Job updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(user=request.user, instance=job)
    
    context = {
        'form': form,
        'job': job,
        'title': f'Edit Job: {job.description[:50]}',
    }
    return render(request, 'jobs/job_form.html', context)


@login_required
def job_delete(request, pk):
    """Delete a job"""
    job = get_object_or_404(Job, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        job_desc = job.description[:50]
        job.delete()
        messages.success(request, f'Job "{job_desc}" deleted successfully!')
        return redirect('job_list')
    
    context = {
        'job': job,
    }
    return render(request, 'jobs/job_confirm_delete.html', context)


@login_required
def export_jobs_csv(request):
    """Export jobs to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jobs.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Customer', 'Description', 'Measurements', 'Due Date', 'Status', 'Notes', 'Created Date'])
    
    jobs = Job.objects.filter(created_by=request.user).select_related('customer')
    for job in jobs:
        writer.writerow([
            job.customer.name,
            job.description,
            job.measurements,
            job.due_date.strftime('%Y-%m-%d'),
            job.get_status_display(),
            job.notes,
            job.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])
    
    return response
