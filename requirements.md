# Seamstress Management App: Requirements Document

## Purpose
Design a mobile-friendly Django app to help seamstresses manage customers, jobs, and payments with keyboard and voice input options.

## Users
- Seamstresses (main user)
- Potentially assistants

## Features

### 1. Customer Management
- Add/edit/delete customer records
- Fields: Name, Phone, Email, Address, Notes

### 2. Job Management
- Link jobs to customers
- Fields: Job Description, Measurements, Due Date, Status (In Progress, Completed, Delivered), Images (optional)
- Track completion, attach files/photos

### 3. Payment Management
- Link payments to jobs/customers
- Fields: Amount, Date, Payment Method, Paid/Unpaid status

### 4. Data Entry Methods
- Keyboard input (standard forms)
- Voice input (speech-to-text for all major text fields, including notes, descriptions, measurements)

### 5. Mobile-First Design
- Responsive UI for phone/tablet
- Touch-friendly interfaces

### 6. Authentication
- Simple login for seamstress
- Optional: PIN or biometric (device-dependent)

### 7. Data Export
- Export customer/job/payment data to CSV/PDF

### 8. Notifications/Reminders
- Job due date reminders (optional)

## Tech Stack

- Backend: Django (Python 3.10+)
- Frontend: Django Templates, Bootstrap (for responsive UI)
- Speech: Web Speech API (browser-based) for voice input
- Database: SQLite (default), easy migration to Postgres
- Deployment: Heroku, PythonAnywhere, or similar

---

## Constraints

- All features must be operable via mobile web browsers.
- Voice input must be available for Chrome/Edge/Safari on mobile.
