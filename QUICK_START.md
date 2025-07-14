# 🚀 Quick Start Guide - Seamstress Management App

## What You've Got
A complete Django web application for managing seamstress business with:
- Customer management
- Job tracking  
- Payment records
- Voice input for mobile
- Responsive design
- Data export capabilities

## 🏁 Quick Setup (Windows)

### Option 1: Use the Setup Script
1. Open Command Prompt or PowerShell
2. Navigate to your project folder: `cd c:\Users\swc4jym\source\repos\mobile-seamstress`
3. Run: `setup.bat`
4. Follow the prompts

### Option 2: Manual Setup
1. **Create virtual environment:**
   ```bash
   python -m venv seamstress_env
   seamstress_env\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create admin user:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the server:**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser:** http://127.0.0.1:8000/

## 🎯 First Steps

1. **Login** with your superuser account
2. **Add a customer** - try the voice input feature!
3. **Create a job** for that customer  
4. **Record a payment** when work is done
5. **Explore the dashboard** to see your progress

## 📱 Testing Voice Input

1. Open the app in **Chrome, Edge, or Safari**
2. Look for **microphone icons** 🎤 next to text fields
3. Click and speak - works great on mobile!
4. Try adding customer notes or job descriptions

## 🔧 Customization

### Add Sample Data (Optional)
```bash
python manage.py create_sample_data --username your_username
```

### Access Admin Panel
- URL: http://127.0.0.1:8000/admin/
- Manage users, view all data, advanced features

### Modify for Your Needs
- Edit models in `customers/models.py`, `jobs/models.py`, `payments/models.py`
- Update templates in `templates/` folder
- Customize forms in `*_app/forms.py` files

## 📊 Key Features to Test

✅ **Voice Input**: Try speaking into text fields  
✅ **Mobile Design**: Test on your phone  
✅ **Search**: Find customers and jobs quickly  
✅ **Export**: Download CSV reports  
✅ **Dashboard**: See business overview  
✅ **File Upload**: Add photos to jobs  

## 🚨 Troubleshooting

**Voice input not working?**
- Use Chrome, Edge, or Safari
- Allow microphone permissions
- Test in quiet environment

**Server won't start?**
- Check if virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`

**Can't access admin?**
- Create superuser: `python manage.py createsuperuser`
- Visit: http://127.0.0.1:8000/admin/

## 🔄 Daily Usage

1. **Activate environment:** `seamstress_env\Scripts\activate`
2. **Start server:** `python manage.py runserver` 
3. **Open browser:** http://127.0.0.1:8000/
4. **Start managing your business!**

## 📱 Mobile Usage

1. Open the app in your mobile browser
2. **Add to home screen** for app-like experience:
   - **iPhone**: Share → Add to Home Screen
   - **Android**: Menu → Add to Home Screen
3. Use voice input for faster data entry
4. Take photos of jobs with device camera

## 🚀 Ready for Production?

When ready to deploy:
- Change `DEBUG=False` in settings
- Use PostgreSQL database
- Configure static file serving
- Deploy to Heroku, PythonAnywhere, etc.

## 💡 Tips

- **Voice works best** in quiet environments
- **Mobile camera** integration for job photos  
- **Export data** regularly for backups
- **Search feature** helps find customers quickly
- **Dashboard shows** overdue jobs and pending payments

---

**You're all set!** 🎉 Start managing your seamstress business efficiently with voice input, mobile design, and complete job tracking.
