# Seamstress Management App

A mobile-friendly Django web application designed to help seamstresses manage customers, jobs, and payments efficiently. Features include voice input capabilities, responsive design, and data export functionality.

## Features

### ✨ Core Functionality
- **Customer Management**: Add, edit, delete, and search customer records
- **Job Management**: Track jobs with descriptions, measurements, due dates, and status
- **Payment Management**: Record and track payments with multiple payment methods
- **Dashboard**: Overview of key metrics and recent activity

### 📱 Mobile-First Design
- Responsive Bootstrap UI optimized for phones and tablets
- Touch-friendly interfaces with large buttons and forms
- Mobile camera integration for job photos

### 🎤 Voice Input
- Speech-to-text input for text fields (notes, descriptions, measurements)
- Works with Chrome, Edge, and Safari on mobile devices
- Visual feedback during voice recording

### 🔒 Authentication & Security
- User authentication with login/logout
- Data isolation per user
- Secure session management

### 📊 Data Management
- Export data to CSV format
- Search and filter functionality
- Image attachments for jobs

## Technology Stack

- **Backend**: Django 4.2+ (Python 3.10+)
- **Frontend**: Bootstrap 5, Django Templates
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Voice Input**: Web Speech API
- **Icons**: Bootstrap Icons
- **Deployment**: Ready for Heroku, PythonAnywhere, or similar

## Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd mobile-seamstress
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv seamstress_env
   
   # Windows
   seamstress_env\Scripts\activate
   
   # macOS/Linux
   source seamstress_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env with your settings (optional for development)
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### First Steps
1. Log in with your superuser account
2. Create your first customer
3. Add a job for that customer
4. Record payments as they come in

### Voice Input
- Look for microphone icons 🎤 next to text fields
- Click the icon and speak your text
- Works best in quiet environments
- Supported in Chrome, Edge, and Safari

### Mobile Usage
- Access the app through your mobile browser
- Add the site to your home screen for app-like experience
- Use device camera for job photos
- Voice input works great on mobile devices

## Project Structure

```
mobile-seamstress/
├── seamstress_app/          # Main Django project settings
├── customers/               # Customer management app
├── jobs/                   # Job tracking app
├── payments/               # Payment management app
├── core/                   # Dashboard and shared functionality
├── templates/              # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── core/              # Dashboard templates
│   └── registration/      # Authentication templates
├── static/                 # CSS, JS, images (created when needed)
├── media/                  # User uploaded files (created when needed)
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── .env.example           # Environment variables template
```

## Key Models

### Customer
- Name, phone, email, address
- Notes field with voice input
- Links to jobs and payments

### Job
- Customer relationship
- Description and measurements (voice input supported)
- Due date and status tracking
- Optional image attachments
- Status: Pending → In Progress → Completed → Delivered

### Payment
- Customer and optional job relationship
- Amount, date, payment method
- Status: Paid, Unpaid, Partially Paid
- Notes field

## Development

### Adding Features
1. Models go in the respective app's `models.py`
2. Views in `views.py`
3. URL patterns in `urls.py`
4. Templates in `templates/app_name/`

### Running Tests
```bash
python manage.py test
```

### Creating Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

The app is ready for deployment to platforms like:

- **Heroku**: Add `Procfile` and configure PostgreSQL
- **PythonAnywhere**: Upload files and configure WSGI
- **DigitalOcean**: Use App Platform or Droplets
- **Railway**: Simple deployment with PostgreSQL

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure static file serving
- [ ] Set up proper secret key
- [ ] Configure allowed hosts
- [ ] Set up SSL/HTTPS

## Browser Compatibility

### Voice Input Support
- ✅ Chrome (desktop & mobile)
- ✅ Edge (desktop & mobile)
- ✅ Safari (mobile - iOS 14.5+)
- ❌ Firefox (Web Speech API not supported)

### General App Support
- All modern browsers support the main functionality
- Mobile browsers work great for touch input
- Progressive Web App features can be added

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the Django documentation
2. Review the code comments
3. Test in different browsers
4. Check browser console for errors

## Roadmap

Future enhancements could include:
- [ ] Push notifications for due dates
- [ ] Calendar integration
- [ ] Invoice generation
- [ ] Customer portal
- [ ] Inventory management
- [ ] Multi-user support with roles
- [ ] API for mobile app integration
