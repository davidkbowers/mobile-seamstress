from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from customers.models import Customer
from jobs.models import Job
from payments.models import Payment
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Create sample data for testing the Seamstress app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username of the user to create sample data for',
            default='admin'
        )

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" not found. Please create a user first.')
            )
            return

        self.stdout.write(f'Creating sample data for user: {user.username}')

        # Create sample customers
        customers_data = [
            {
                'name': 'Sarah Johnson',
                'phone': '(555) 123-4567',
                'email': 'sarah.johnson@email.com',
                'address': '123 Main St, Anytown, ST 12345',
                'notes': 'Prefers alterations on weekends. Has 2 daughters who also need alterations.'
            },
            {
                'name': 'Maria Garcia',
                'phone': '(555) 987-6543',
                'email': 'maria.garcia@email.com',
                'address': '456 Oak Ave, Somewhere, ST 67890',
                'notes': 'Wedding dress customer. Very detail-oriented.'
            },
            {
                'name': 'Jennifer Smith',
                'phone': '(555) 555-0123',
                'email': '',
                'address': '',
                'notes': 'Regular customer for hem adjustments.'
            }
        ]

        customers = []
        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                name=customer_data['name'],
                created_by=user,
                defaults=customer_data
            )
            customers.append(customer)
            if created:
                self.stdout.write(f'  Created customer: {customer.name}')
            else:
                self.stdout.write(f'  Customer already exists: {customer.name}')

        # Create sample jobs
        jobs_data = [
            {
                'customer': customers[0],
                'description': 'Hem dress pants - 2 inches shorter',
                'measurements': 'Inseam: 28 inches, Waist: 32 inches',
                'due_date': date.today() + timedelta(days=7),
                'status': 'in_progress',
                'notes': 'Customer wants cuffs preserved'
            },
            {
                'customer': customers[1],
                'description': 'Wedding dress alterations - fit bodice and adjust train',
                'measurements': 'Bust: 36, Waist: 28, Hips: 38, Height: 5\'6"',
                'due_date': date.today() + timedelta(days=21),
                'status': 'pending',
                'notes': 'Wedding is on March 15th. Very important!'
            },
            {
                'customer': customers[0],
                'description': 'Shorten sleeves on blazer',
                'measurements': 'Arm length: 23 inches',
                'due_date': date.today() - timedelta(days=2),
                'status': 'completed',
                'notes': 'Rush job - completed early'
            },
            {
                'customer': customers[2],
                'description': 'Hem 3 pairs of jeans',
                'measurements': 'All size 8, inseam should be 30 inches',
                'due_date': date.today() + timedelta(days=5),
                'status': 'in_progress',
                'notes': 'Regular customer discount applied'
            }
        ]

        jobs = []
        for job_data in jobs_data:
            job, created = Job.objects.get_or_create(
                customer=job_data['customer'],
                description=job_data['description'],
                created_by=user,
                defaults=job_data
            )
            jobs.append(job)
            if created:
                self.stdout.write(f'  Created job: {job.description[:30]}...')
            else:
                self.stdout.write(f'  Job already exists: {job.description[:30]}...')

        # Create sample payments
        payments_data = [
            {
                'customer': customers[0],
                'job': jobs[2],  # Completed blazer job
                'amount': 25.00,
                'date': date.today() - timedelta(days=1),
                'payment_method': 'cash',
                'status': 'paid',
                'notes': 'Paid in cash upon pickup'
            },
            {
                'customer': customers[1],
                'job': jobs[1],  # Wedding dress job
                'amount': 150.00,
                'date': date.today(),
                'payment_method': 'check',
                'status': 'paid',
                'notes': 'Deposit payment - Check #1234'
            },
            {
                'customer': customers[2],
                'job': jobs[3],  # Jeans hemming
                'amount': 45.00,
                'date': date.today() + timedelta(days=5),
                'payment_method': 'cash',
                'status': 'unpaid',
                'notes': 'Will pay on pickup'
            }
        ]

        for payment_data in payments_data:
            payment, created = Payment.objects.get_or_create(
                customer=payment_data['customer'],
                job=payment_data['job'],
                amount=payment_data['amount'],
                created_by=user,
                defaults=payment_data
            )
            if created:
                self.stdout.write(f'  Created payment: ${payment.amount} from {payment.customer.name}')
            else:
                self.stdout.write(f'  Payment already exists: ${payment.amount} from {payment.customer.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSample data created successfully!\n'
                f'Created {len(customers)} customers, {len(jobs)} jobs, and {len(payments_data)} payments.\n'
                f'You can now test the application with realistic data.'
            )
        )
