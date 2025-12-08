# Expense Tracker Web Application

A production-ready Django web application for tracking daily expenses with user authentication, categorization, and comprehensive filtering capabilities.

## 🚀 Features

- **User Authentication**: Secure sign-up, login, and logout functionality
- **Expense Management**: Full CRUD operations for expense tracking
- **Advanced Filtering**: Filter expenses by category, date range, and search terms
- **Multiple Categories**: Food, Transport, Shopping, Bills, Entertainment, Healthcare, Education, and Other
- **Responsive Design**: Bootstrap 5-based UI that works on all devices
- **Admin Dashboard**: Enhanced Django admin interface with custom features
- **RESTful API Ready**: Structured for easy API integration
- **Production Ready**: Docker support, environment-based configuration, and security best practices

## 📋 Requirements

- **Python 3.10, 3.11, or 3.12** (Python 3.14+ not yet supported by Django 5.0)
- PostgreSQL 13+ (for production)

## 📁 Project Structure

The project follows a well-organized structure:

- `deploy/` - Docker and deployment configurations
- `docs/` - Comprehensive documentation
- `scripts/` - Setup and utility scripts
- `expense_tracker/` - Django project settings
- `expenses/` - Main application code
- `static/` - CSS and JavaScript files
- `templates/` - HTML templates

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed information.

- Docker & Docker Compose (optional, for containerized deployment)

> ⚠️ **Important**: If you're getting template/admin errors, you may be using Python 3.14 which is incompatible with Django 5.0. Please see `PYTHON_VERSION_ISSUE.md` for details.

## 🛠️ Installation & Setup

### Local Development Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd expense_tracker
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**

   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Web App: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Docker Deployment

1. **Configure environment**

   ```bash
   cp .env.example .env
   # Update .env with production settings
   ```

2. **Build and run with Docker Compose**

   ```bash
   docker-compose up -d --build
   ```

3. **Run migrations**

   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create superuser**

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**
   - Web App: http://localhost
   - Admin: http://localhost/admin

### Detailed Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for a comprehensive overview of the project organization, including:

- Directory structure and purpose
- Configuration files explanation
- Environment-specific behavior
- Best practices for maintenance

```
expense_tracker/
├── deploy/                  # Deployment configurations
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── gunicorn_config.py
│   └── nginx.conf
├── scripts/                 # Utility scripts
│   ├── setup_dev.sh
│   ├── setup_dev.bat
│   └── ...
├── expense_tracker/         # Project configuration
│   ├── settings/           # Environment-specific settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── staging.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── expenses/               # Main application
│   ├── management/        # Custom management commands
│   │   └── commands/
│   │       ├── generate_test_data.py
│   │       ├── export_expenses.py
│   │       └── cleanup_old_expenses.py
│   ├── tests/              # Comprehensive test suite
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_forms.py
│   ├── models.py           # Data models
│   ├── views.py            # Class-based views
│   ├── forms.py            # Form definitions
│   ├── admin.py            # Admin configuration
│   └── urls.py
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── logs/                   # Application logs
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── gunicorn_config.py     # Gunicorn configuration
├── nginx.conf             # Nginx configuration
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── pytest.ini            # Pytest configuration
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🧪 Testing

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=expenses --cov-report=html

# Run specific test file
pytest expenses/tests/test_models.py

# Run with verbose output
pytest -v
```

## 🔧 Management Commands

### Generate Test Data

```bash
python manage.py generate_test_data --users=5 --expenses=50
```

### Export Expenses to CSV

```bash
python manage.py export_expenses --user=username --output=expenses.csv
```

### Cleanup Old Expenses

```bash
python manage.py cleanup_old_expenses --days=365 --dry-run
```

## 🔐 Security Features

- Environment-based configuration with `python-decouple`
- Separate settings for development/staging/production
- CSRF protection enabled
- Secure session cookies in production
- HTTPS redirect in production
- SQL injection protection through Django ORM
- XSS protection headers
- Password validation with multiple validators
- Secure static file serving with WhiteNoise

## 🚀 Production Deployment

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
DJANGO_ENVIRONMENT=production
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=expense_tracker_db
DB_USER=postgres
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432

```

### Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `SECRET_KEY` with a strong random value
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure PostgreSQL database
- [ ] Configure email settings for error notifications
- [ ] Run `collectstatic` to gather static files
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup strategy for database
- [ ] Set up monitoring and logging (e.g., Sentry)
- [ ] Review security headers

## 📊 Database Schema

### Expense Model

| Field       | Type          | Description                  |
| ----------- | ------------- | ---------------------------- |
| id          | AutoField     | Primary key                  |
| user        | ForeignKey    | User who created the expense |
| amount      | DecimalField  | Expense amount (positive)    |
| category    | CharField     | Expense category             |
| date        | DateField     | Date of expense              |
| description | TextField     | Optional description         |
| created_at  | DateTimeField | Record creation timestamp    |
| updated_at  | DateTimeField | Last update timestamp        |


## 📝 Best Practices Implemented

- **Settings Organization**: Environment-specific settings files
- **Class-Based Views**: Reusable and maintainable view code
- **Model Validation**: Custom validators and constraints
- **Comprehensive Testing**: Unit tests for models, views, and forms
- **Logging**: Structured logging for debugging and monitoring
- **Security**: Production-ready security configurations
- **Docker Support**: Easy deployment with containers
- **Type Hints**: Better code clarity (where applicable)
- **DRY Principle**: Reusable components and utilities

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.


## 🙏 Acknowledgments

- Django framework
- Bootstrap for UI components
- PostgreSQL database
- Gunicorn and Nginx for production serving
