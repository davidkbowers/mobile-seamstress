from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q, Sum
from .models import Payment
from .forms import PaymentForm
from customers.models import Customer
from jobs.models import Job
import csv


@login_required
def payment_list(request):
    """List all payments with filtering and search"""
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    payments = Payment.objects.filter(created_by=request.user).select_related('customer', 'job')
    
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    if search_query:
        payments = payments.filter(
            Q(customer__name__icontains=search_query) |
            Q(notes__icontains=search_query) |
            Q(amount__icontains=search_query)
        )
    
    payments = payments.order_by('-date', '-created_at')
    
    # Calculate totals
    totals = Payment.objects.filter(created_by=request.user).aggregate(
        total_paid=Sum('amount', filter=Q(status='paid')),
        total_unpaid=Sum('amount', filter=Q(status='unpaid')),
        total_partial=Sum('amount', filter=Q(status='partial')),
    )
    
    context = {
        'payments': payments,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Payment.STATUS_CHOICES,
        'totals': totals,
    }
    return render(request, 'payments/payment_list.html', context)


@login_required
def payment_detail(request, pk):
    """Show payment details"""
    payment = get_object_or_404(Payment, pk=pk, created_by=request.user)
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/payment_detail.html', context)


@login_required
def payment_create(request):
    """Create a new payment"""
    if request.method == 'POST':
        form = PaymentForm(user=request.user, data=request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.created_by = request.user
            payment.save()
            messages.success(request, f'Payment of ${payment.amount} recorded successfully!')
            return redirect('payment_detail', pk=payment.pk)
    else:
        form = PaymentForm(user=request.user)
        # Pre-select customer and job if provided in URL
        customer_id = request.GET.get('customer')
        job_id = request.GET.get('job')
        if customer_id:
            try:
                customer = Customer.objects.get(pk=customer_id, created_by=request.user)
                form.initial['customer'] = customer
            except Customer.DoesNotExist:
                pass
        if job_id:
            try:
                job = Job.objects.get(pk=job_id, created_by=request.user)
                form.initial['job'] = job
                form.initial['customer'] = job.customer
            except Job.DoesNotExist:
                pass
    
    context = {
        'form': form,
        'title': 'Record New Payment',
    }
    return render(request, 'payments/payment_form.html', context)


@login_required
def payment_edit(request, pk):
    """Edit an existing payment"""
    payment = get_object_or_404(Payment, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = PaymentForm(user=request.user, data=request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Payment updated successfully!')
            return redirect('payment_detail', pk=payment.pk)
    else:
        form = PaymentForm(user=request.user, instance=payment)
    
    context = {
        'form': form,
        'payment': payment,
        'title': f'Edit Payment: ${payment.amount}',
    }
    return render(request, 'payments/payment_form.html', context)


@login_required
def payment_delete(request, pk):
    """Delete a payment"""
    payment = get_object_or_404(Payment, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        payment_amount = payment.amount
        payment.delete()
        messages.success(request, f'Payment of ${payment_amount} deleted successfully!')
        return redirect('payment_list')
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/payment_confirm_delete.html', context)


@login_required
def export_payments_csv(request):
    """Export payments to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Customer', 'Job', 'Amount', 'Date', 'Payment Method', 'Status', 'Notes', 'Created Date'])
    
    payments = Payment.objects.filter(created_by=request.user).select_related('customer', 'job')
    for payment in payments:
        writer.writerow([
            payment.customer.name,
            payment.job.description[:50] if payment.job else 'N/A',
            str(payment.amount),
            payment.date.strftime('%Y-%m-%d'),
            payment.get_payment_method_display(),
            payment.get_status_display(),
            payment.notes,
            payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])
    
    return response
