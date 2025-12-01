# KFH Hospital Management System

A comprehensive hospital management system built with Django to streamline hospital operations, patient management, and administrative tasks.

## 📋 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Patient Management**: Register and manage patient records
- **Appointment Scheduling**: Book and track patient appointments
- **Staff Management**: Manage hospital staff and their roles
- **Medical Records**: Maintain comprehensive patient medical histories
- **Admin Dashboard**: Centralized control panel for administrators
- **User Authentication**: Secure login system for different user roles

## 🛠 Technologies Used

- **Backend**: Django 3.4
- **Database**: SQLite3 (Development) / PostgreSQL (Production)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render
- **Version Control**: Git & GitHub

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kezacardine/kfh_hospital.git
cd kfh_hospital
```

### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 8. Run the Development Server

**On Windows:**
```bash
start_kfh.bat
```

**On macOS/Linux:**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 💻 Usage

### Accessing the Admin Panel

1. Navigate to `http://127.0.0.1:8000/admin`
2. Login with your superuser credentials
3. Manage patients, appointments, and staff from the dashboard

### User Roles

- **Admin**: Full access to all features
- **Doctor**: Access to patient records and appointments
- **Receptionist**: Patient registration and appointment booking
- **Patient**: View personal medical records and appointments

## 📁 Project Structure

```
kfh_hospital/
├── hospital/                # Main application
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── admin.py           # Admin configurations
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   └── urls.py            # URL routing
├── kfh_project/           # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── static/                # Static files (CSS, JS, images)
├── staticfiles/           # Collected static files
├── templates/             # Global templates
├── venv/                  # Virtual environment
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Procfile               # Deployment configuration
├── build.sh               # Build script for deployment
└── README.md              # This file
```

## 🌐 Deployment

This project is configured for deployment on Render.

### Deploy to Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Render will automatically detect the `build.sh` script
5. Set environment variables in Render dashboard:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `PYTHON_VERSION=3.11.0`

The `Procfile` and `build.sh` are already configured for Render deployment.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 👥 Authors

- **kayi122** - *Initial work* - [kezacardine](https://github.com/kezacardine)
- **mbishflavien** - Collaborator - [mbishflavien](https://github.com/mbishflavien)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap for UI components
- The open-source community

---

**Note**: This is a development project. For production use, ensure you:
- Change `DEBUG=False` in production
- Use a production-grade database (PostgreSQL)
- Implement proper security measures
- Set up HTTPS
- Configure proper backup 
