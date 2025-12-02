# 🏥 KFH Hospital Management System

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2.8-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A comprehensive hospital management system built with Django that streamlines patient care, vital signs monitoring, and health analytics. Features intelligent risk assessment algorithms and advanced data visualization capabilities.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Deployment](#-deployment)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Data Models](#-data-models)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Authors](#-authors)
- [License](#-license)
- [Support](#-support)

---

## 🎯 Overview

The KFH Hospital Management System is a full-featured healthcare management platform designed to help medical facilities efficiently manage patient records, monitor vital signs, and analyze health trends. The system includes automated risk assessment algorithms that evaluate patient vital signs and assign risk levels, enabling healthcare providers to prioritize care effectively.

### Key Highlights

- **Automated Risk Assessment**: Intelligent algorithms calculate risk scores based on vital signs
- **Real-time Analytics**: Advanced data visualization using pandas, matplotlib, and seaborn
- **Comprehensive Patient Management**: Complete patient lifecycle tracking
- **Role-based Access Control**: Secure authentication and authorization
- **Production Ready**: Configured for deployment on Render with PostgreSQL support

---

## ✨ Features

### 🏥 Patient Management
- **Patient Registration**: Register patients with unique identifiers (e.g., P0001)
- **Patient Profiles**: Comprehensive patient information including demographics, contact details, and medical history
- **Patient Search**: Quick search by patient ID, name, or phone number
- **Age Analysis**: Automatic calculation and tracking of patient ages, including elderly patient counting (60+ years)

### 💓 Vital Signs Monitoring
- **Vital Signs Recording**: Track heart rate, temperature, systolic/diastolic blood pressure
- **Automatic Risk Assessment**: 
  - Calculates risk scores (0-100) based on vital sign thresholds
  - Assigns risk levels: **LOW** (0-30), **MEDIUM** (31-60), **HIGH** (61-100)
  - Identifies specific risk factors (bradycardia, tachycardia, fever, hypertension, etc.)
- **Risk Factor Analysis**: Detailed breakdown of why a patient is at risk
- **Historical Tracking**: Complete history of all vital sign recordings per patient

### 📊 Analytics & Visualization
- **Interactive Dashboard**: Real-time statistics and key performance indicators
- **Data Visualization**: 
  - Heart rate distribution histograms
  - Temperature density plots
  - Blood pressure violin plots
  - Heart rate vs. blood pressure scatter plots
  - Trend analysis over time
  - Correlation heatmaps
- **Abnormal Case Detection**: Automatic identification of:
  - High heart rate cases (>100 bpm)
  - Fever cases (>37.5°C)
  - Hypertension cases (BP >140/90 mmHg)
- **Statistical Analysis**: Average vital signs calculations and trend monitoring

### 🔐 Security & Access Control
- **User Authentication**: Secure login/logout system
- **Role-based Access**: Support for different user roles (Admin, Doctor, Receptionist, Patient)
- **Session Management**: Secure session handling
- **Protected Routes**: Login-required decorators for sensitive pages

### 🎨 User Interface
- **Modern Design**: Clean, responsive Bootstrap-based interface
- **Dashboard**: Centralized control panel with key metrics
- **Patient Detail Views**: Comprehensive patient information pages
- **Admin Panel**: Full Django admin integration for data management

---

## 🛠 Technologies Used

### Backend
- **Django 5.2.8**: High-level Python web framework
- **Python 3.8+**: Programming language
- **Gunicorn 23.0.0**: Python WSGI HTTP Server for production

### Database
- **SQLite3**: Development database
- **PostgreSQL**: Production database (via `psycopg2-binary`)
- **dj-database-url**: Database URL configuration

### Data Analysis & Visualization
- **Pandas 2.3.3**: Data manipulation and analysis
- **NumPy 2.3.5**: Numerical computing
- **Matplotlib 3.10.7**: Plotting and visualization
- **Seaborn 0.13.2**: Statistical data visualization

### Frontend
- **HTML5/CSS3**: Markup and styling
- **JavaScript**: Client-side interactivity
- **Bootstrap**: Responsive UI framework
- **Font Awesome**: Icons

### Deployment & Infrastructure
- **WhiteNoise 6.11.0**: Static file serving
- **Render**: Cloud hosting platform
- **Git & GitHub**: Version control

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package manager - usually comes with Python)
- **Git** ([Download Git](https://git-scm.com/downloads))
- **Virtual environment** (recommended - `venv` comes with Python 3.3+)

### Optional (for production)
- **PostgreSQL** (for production database)
- **Render account** (for cloud deployment)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/kezacardine/kfh_hospital.git
cd kfh_hospital
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> **Note**: Your terminal prompt should now show `(venv)` indicating the virtual environment is active.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including Django, pandas, matplotlib, seaborn, and other dependencies.

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

**Windows (PowerShell):**
```powershell
New-Item -Path .env -ItemType File
```

**macOS/Linux:**
```bash
touch .env
```

Add the following content to `.env`:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

> **⚠️ Security Note**: Generate a strong secret key for production. You can use:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### Step 5: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the database tables for Patient and VitalSign models.

### Step 6: Create Superuser Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. You'll need:
- Username
- Email address (optional)
- Password (will be hidden as you type)

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This collects all static files (CSS, JavaScript, images) into the `staticfiles` directory.

### Step 8: Run the Development Server

**Windows:**
```bash
start_kfh.bat
```

**macOS/Linux:**
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000`

### Step 9: Access the Application

- **Home Page**: `http://127.0.0.1:8000`
- **Admin Panel**: `http://127.0.0.1:8000/admin`
- **Dashboard**: `http://127.0.0.1:8000/dashboard` (requires login)
- **Analytics**: `http://127.0.0.1:8000/analytics` (requires login)

---

## ⚙️ Configuration

### Database Configuration

The system automatically uses SQLite for development. For production, configure PostgreSQL:

1. Set `DATABASE_URL` environment variable:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

2. The system uses `dj-database-url` to parse the connection string automatically.

### Static Files Configuration

Static files are served using WhiteNoise in production. No additional configuration needed.

### Time Zone

Default timezone is set to `Africa/Kigali`. To change, modify `TIME_ZONE` in `kfh_project/settings.py`.

---

## 💻 Usage

### Accessing the Admin Panel

1. Navigate to `http://127.0.0.1:8000/admin`
2. Login with your superuser credentials
3. Manage patients, vital signs, and users from the dashboard

### User Roles

The system supports multiple user roles:

- **Admin**: Full access to all features, admin panel, and system configuration
- **Doctor**: Access to patient records, vital signs, and analytics
- **Receptionist**: Patient registration and appointment booking capabilities
- **Patient**: View personal medical records and appointment history

### Adding a Patient

1. Login to the admin panel or use the application interface
2. Navigate to Patients section
3. Click "Add Patient"
4. Fill in required information:
   - Patient ID (unique identifier)
   - First Name, Last Name
   - Date of Birth
   - Gender
   - Phone Number
   - Email (optional)
   - Address
5. Save the patient record

### Recording Vital Signs

1. Navigate to a patient's detail page
2. Click "Add Vital Signs"
3. Enter measurements:
   - Heart Rate (bpm)
   - Temperature (°C)
   - Systolic Blood Pressure (mmHg)
   - Diastolic Blood Pressure (mmHg)
4. The system automatically:
   - Calculates risk score
   - Assigns risk level (LOW/MEDIUM/HIGH)
   - Identifies risk factors

### Viewing Analytics

1. Login to the system
2. Navigate to Analytics dashboard
3. View interactive charts and visualizations:
   - Heart rate distributions
   - Temperature trends
   - Blood pressure analysis
   - Correlation heatmaps
   - Trend analysis

### Risk Assessment Algorithm

The system uses the following thresholds for risk calculation:

| Vital Sign | Normal Range | Risk Factors |
|------------|--------------|--------------|
| Heart Rate | 60-100 bpm | <40 (Severe), <60 (Mild), >100 (Mild), >120 (Severe) |
| Temperature | 36.1-37.2°C | <35 (Severe), <36 (Mild), >37.5 (Mild), >39 (Severe) |
| Systolic BP | 90-120 mmHg | <90 (Low), >140 (Elevated), >180 (Crisis) |
| Diastolic BP | 60-80 mmHg | <60 (Low), >90 (Elevated), >120 (Crisis) |

**Risk Score Calculation:**
- Each abnormal vital sign contributes points to the total risk score
- Score ranges from 0-100
- Risk levels: LOW (0-30), MEDIUM (31-60), HIGH (61-100)

---

## 📁 Project Structure

```
kfh_hospital/
├── hospital/                    # Main Django application
│   ├── migrations/             # Database migration files
│   │   ├── 0001_initial.py
│   │   └── 0002_vitalsign_risk_level_vitalsign_risk_score.py
│   ├── templates/              # HTML templates
│   │   └── hospital/
│   │       ├── base.html       # Base template
│   │       ├── home.html       # Home page
│   │       ├── login.html      # Login page
│   │       ├── dashboard.html  # Main dashboard
│   │       ├── analytics.html  # Analytics dashboard
│   │       └── patient_detail.html
│   ├── __init__.py
│   ├── admin.py               # Django admin configuration
│   ├── apps.py                # App configuration
│   ├── models.py              # Database models (Patient, VitalSign)
│   ├── views.py               # View functions and business logic
│   ├── urls.py                # URL routing
│   └── tests.py               # Unit tests
│
├── kfh_project/               # Django project settings
│   ├── __init__.py
│   ├── settings.py            # Django settings and configuration
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI configuration for production
│   └── asgi.py                # ASGI configuration
│
├── static/                    # Static files (CSS, JS, images)
│   └── images/
│       ├── kfh-logo.png
│       └── doctor-bg.jpg
│
├── staticfiles/               # Collected static files (generated)
│
├── templates/                 # Global templates directory
│
├── venv/                      # Virtual environment (not in git)
│
├── db.sqlite3                 # SQLite database (not in git)
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── Procfile                   # Deployment configuration for Render
├── build.sh                   # Build script for deployment
├── start_kfh.bat             # Windows startup script
└── README.md                  # This file
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/` | GET | Home page | Public |
| `/login/` | GET, POST | User login | Public |
| `/logout/` | GET | User logout | Authenticated |
| `/dashboard/` | GET | Main dashboard | Authenticated |
| `/analytics/` | GET | Analytics dashboard | Authenticated |
| `/patient/<patient_id>/` | GET | Patient detail view | Authenticated |
| `/elderly-count/` | GET | Count of elderly patients (60+) | Public |
| `/admin/` | GET | Django admin panel | Admin only |

---

## 🗄️ Data Models

### Patient Model

```python
- patient_id: CharField (unique identifier)
- first_name: CharField
- last_name: CharField
- date_of_birth: DateField
- gender: CharField (M/F)
- phone: CharField
- email: EmailField (optional)
- address: TextField
- created_at: DateTimeField (auto)
- updated_at: DateTimeField (auto)
```

**Methods:**
- `get_latest_risk_level()`: Returns latest risk level from vital signs
- `get_latest_risk_color()`: Returns Bootstrap color for risk badge

### VitalSign Model

```python
- patient: ForeignKey (Patient)
- heart_rate: FloatField
- temperature: FloatField
- systolic_bp: FloatField
- diastolic_bp: FloatField
- risk_level: CharField (LOW/MEDIUM/HIGH)
- risk_score: IntegerField (0-100)
- recorded_at: DateTimeField
- recorded_by: ForeignKey (User)
```

**Methods:**
- `calculate_risk_score()`: Calculates risk score based on vital signs
- `determine_risk_level()`: Maps score to risk level
- `get_risk_factors()`: Returns list of specific risk factors

**Properties:**
- `high_hr`: Boolean (heart rate > 100)
- `fever`: Boolean (temperature > 37.5°C)
- `hypertension`: Boolean (BP exceeds thresholds)

---

## 🌐 Deployment

### Deploy to Render

This project is pre-configured for deployment on [Render](https://render.com).

#### Prerequisites
1. GitHub account
2. Render account (free tier available)
3. Code pushed to GitHub repository

#### Deployment Steps

1. **Push Code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Create New Web Service on Render**
   - Log in to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Build Settings**
   - Render will auto-detect the `build.sh` script
   - Build command: (automatically detected)
   - Start command: `gunicorn kfh_project.wsgi`

4. **Set Environment Variables**
   In Render dashboard, add these environment variables:
   ```
   SECRET_KEY=your-production-secret-key-here
   DEBUG=False
   DATABASE_URL=postgresql://user:password@host:port/dbname
   PYTHON_VERSION=3.11.0
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Your app will be available at `https://your-app.onrender.com`

#### Production Checklist

- [ ] Set `DEBUG=False` in environment variables
- [ ] Use PostgreSQL database (not SQLite)
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Set up HTTPS (automatic on Render)
- [ ] Configure backup system for database
- [ ] Set up monitoring and logging
- [ ] Review security settings

### Alternative Deployment Options

- **Heroku**: Similar process, use `Procfile` and `requirements.txt`
- **AWS Elastic Beanstalk**: Configure for Django application
- **DigitalOcean App Platform**: Connect GitHub repository
- **Self-hosted**: Use Gunicorn + Nginx on VPS

---

## 🤝 Contributing

Contributions are welcome and greatly appreciated! Here's how you can contribute:

### Getting Started

1. **Fork the Repository**
   ```bash
   # Click "Fork" button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/kfh_hospital.git
   cd kfh_hospital
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Changes**
   - Write clean, documented code
   - Follow PEP 8 style guidelines
   - Add comments for complex logic
   - Update tests if applicable

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: Description of your feature"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Open a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Describe your changes clearly

### Contribution Guidelines

- Follow the existing code style
- Write meaningful commit messages
- Update documentation if needed
- Test your changes thoroughly
- Ensure all tests pass

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations
- 🧪 Test coverage
- 🌐 Internationalization

---

## 👥 Authors

- **kayi122** - *Initial work* - [@kezacardine](https://github.com/kezacardine)

### Contributors

- **Celine** - *Elderly patient counting feature*
- **Leiss Uwase** - *Enhanced Vitalsign admin readability  for better audditing*
- **mbishflavien** - *Conducted user acceptance testing and bug fixes* 

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 KFH Hospital Management System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

### Getting Help

- **GitHub Issues**: [Open an issue](https://github.com/kezacardine/kfh_hospital/issues) for bug reports or feature requests
- **Documentation**: Check this README and code comments
- **Contact**: Reach out to the development team via GitHub

### Common Issues

**Issue**: `ModuleNotFoundError` when running server
- **Solution**: Ensure virtual environment is activated and dependencies are installed

**Issue**: Database migration errors
- **Solution**: Delete `db.sqlite3` and migration files in `migrations/` (except `__init__.py`), then run migrations again

**Issue**: Static files not loading
- **Solution**: Run `python manage.py collectstatic --noinput`

**Issue**: Port already in use
- **Solution**: Use a different port: `python manage.py runserver 8001`

---

## 🙏 Acknowledgments

- **Django Community** - For the excellent framework and documentation
- **Bootstrap** - For the responsive UI components
- **Matplotlib & Seaborn** - For powerful data visualization capabilities
- **Pandas** - For efficient data manipulation
- **Open Source Community** - For inspiration and support

---

## 📊 Project Status

![GitHub last commit](https://img.shields.io/github/last-commit/kezacardine/kfh_hospital?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/kezacardine/kfh_hospital?style=flat-square)
![GitHub pull requests](https://img.shields.io/github/issues-pr/kezacardine/kfh_hospital?style=flat-square)

**Current Version**: 1.0.0  
**Status**: Active Development  
**Last Updated**: 2024

---

## ⚠️ Important Notes

### Development vs Production

This is a development project. For production use, ensure you:

- ✅ Change `DEBUG=False` in production environment
- ✅ Use a production-grade database (PostgreSQL recommended)
- ✅ Implement proper security measures (HTTPS, secure headers)
- ✅ Set up automated backups
- ✅ Configure proper logging and monitoring
- ✅ Use environment variables for sensitive data
- ✅ Regularly update dependencies for security patches
- ✅ Follow HIPAA compliance guidelines if handling real patient data

### Disclaimer

This software is provided for educational and development purposes. For production healthcare applications, ensure compliance with:
- HIPAA (Health Insurance Portability and Accountability Act)
- Local healthcare regulations
- Data protection laws (GDPR, etc.)

---

<div align="center">

**Made with ❤️ for better healthcare management**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/kezacardine/kfh_hospital/issues) • [Request Feature](https://github.com/kezacardine/kfh_hospital/issues) • [Documentation](#-documentation)

</div>
