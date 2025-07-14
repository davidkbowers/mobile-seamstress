from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm
import csv


@login_required
def customer_list(request):
    """List all customers with search functionality"""
    search_query = request.GET.get('search', '')
    customers = Customer.objects.filter(created_by=request.user)
    
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    customers = customers.order_by('name')
    
    context = {
        'customers': customers,
        'search_query': search_query,
    }
    return render(request, 'customers/customer_list.html', context)


@login_required
def customer_detail(request, pk):
    """Show customer details with jobs and payments"""
    customer = get_object_or_404(Customer, pk=pk, created_by=request.user)
    jobs = customer.job_set.all().order_by('-created_at')
    payments = customer.payment_set.all().order_by('-date')
    
    context = {
        'customer': customer,
        'jobs': jobs,
        'payments': payments,
    }
    return render(request, 'customers/customer_detail.html', context)


@login_required
def customer_create(request):
    """Create a new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            messages.success(request, f'Customer "{customer.name}" created successfully!')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    
    context = {
        'form': form,
        'title': 'Add New Customer',
    }
    return render(request, 'customers/customer_form.html', context)


@login_required
def customer_edit(request, pk):
    """Edit an existing customer"""
    customer = get_object_or_404(Customer, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer "{customer.name}" updated successfully!')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
        'title': f'Edit Customer: {customer.name}',
    }
    return render(request, 'customers/customer_form.html', context)


@login_required
def customer_delete(request, pk):
    """Delete a customer"""
    customer = get_object_or_404(Customer, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        customer_name = customer.name
        customer.delete()
        messages.success(request, f'Customer "{customer_name}" deleted successfully!')
        return redirect('customer_list')
    
    context = {
        'customer': customer,
    }
    return render(request, 'customers/customer_confirm_delete.html', context)


@login_required
def export_customers_csv(request):
    """Export customers to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Email', 'Address', 'Notes', 'Created Date'])
    
    customers = Customer.objects.filter(created_by=request.user)
    for customer in customers:
        writer.writerow([
            customer.name,
            customer.phone,
            customer.email,
            customer.address,
            customer.notes,
            customer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])
    
    return response
