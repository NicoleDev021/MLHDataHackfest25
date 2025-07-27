"""
Personal Finance Coach - Architecture Documentation
==================================================

This document explains how all components of the Personal Finance Coach application 
work together. Perfect for junior software interns to understand the system design.

## 🏗️ Overall Architecture

The application follows a modular Flask blueprint architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                             │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP Requests
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  FLASK APPLICATION                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │    Auth     │    │   Templates │    │   Static    │     │
│  │  Blueprint  │    │   (Jinja2)  │    │   Files     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────┬───────────────────────────────────────┘
                      │ OAuth2 Requests
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    AUTH0 SERVICE                            │
└─────────────────────────────────────────────────────────────┘
```

## 📁 File Structure & Responsibilities

### Core Application Files
```
personal_finance_coach/
├── run.py                    # 🚀 Entry point - starts the Flask server
├── app/
│   ├── __init__.py          # 🏭 Application factory - creates Flask app
│   ├── config.py            # ⚙️  Configuration management
│   ├── logging_config.py    # 📝 Logging setup and file management
│   ├── validation.py        # ✅ Data validation using Marshmallow
│   └── auth/                # 🔐 Authentication module
│       ├── __init__.py      # Blueprint registration
│       ├── routes.py        # Auth routes (login, logout, callback)
│       └── decorators.py    # Authentication decorators
└── templates/               # 🎨 HTML templates with Jinja2
    ├── base.html           # Master template layout
    ├── home.html           # Landing page
    └── auth/               # Authentication-specific templates
```

## 🔄 Application Startup Flow

Here's what happens when you run `python run.py`:

1. **run.py** 
   - Reads FLASK_ENV environment variable
   - Calls create_app() function from app/__init__.py
   - Starts Flask development server on port 5000

2. **app/__init__.py (create_app function)**
   - Loads environment variables from .env file
   - Selects configuration class based on environment
   - Initializes URL configuration for Codespaces/localhost
   - Sets up secure session configuration
   - Validates Auth0 environment variables
   - Registers OAuth2 client with Auth0
   - Sets up error handlers (404, 500, 403)
   - Registers authentication blueprint
   - Returns configured Flask app

3. **Ready to accept requests!**

## 🔐 Authentication Flow (Step-by-Step)

### User Login Process:
```
1. User clicks "Login" button
   ↓
2. Browser → /auth/login (routes.py)
   ↓
3. Flask → Auth0 authorization URL (with callback URL)
   ↓
4. User → Auth0 login page (external)
   ↓
5. Auth0 → /auth/callback (with authorization code)
   ↓
6. Flask exchanges code for access token
   ↓
7. Flask gets user profile from Auth0
   ↓
8. Flask validates user data (validation.py)
   ↓
9. Flask stores user in session
   ↓
10. User redirected to dashboard
```

### Session Management:
- User data stored in Flask session (encrypted cookies)
- Session expires after 1 hour (configurable)
- Session cleared on logout
- Auth0 also handles logout to clear external session

## ⚙️ Configuration System

The configuration system adapts to different environments:

### Environment Detection:
1. **Local Development**: Uses http://localhost:5000
2. **GitHub Codespaces**: Auto-detects CODESPACE_NAME environment variable
3. **Production**: Uses secure HTTPS URLs

### Configuration Classes:
- **Config**: Base configuration with Auth0 settings
- **DevelopmentConfig**: Debug mode, insecure cookies for localhost
- **ProductionConfig**: Security hardened, HTTPS required
- **TestingConfig**: Optimized for automated tests

### URL Generation Logic:
```python
# In config.py
def _get_base_url():
    codespace_name = os.getenv("CODESPACE_NAME")
    if codespace_name:
        return f"https://{codespace_name}-5000.app.github.dev"
    else:
        return "http://localhost:5000"
```

## 🎨 Template System

### Template Hierarchy:
```
base.html (Master template)
├── Contains Bootstrap CSS/JS
├── Navigation bar
├── Flash message system
└── Content blocks for child templates

home.html (Landing page)
├── Extends base.html
├── Shows login/logout buttons based on auth status
└── Displays user name if authenticated

auth/dashboard.html (User dashboard)
├── Extends base.html
├── Protected route (requires login)
└── Shows user profile information
```

### Jinja2 Template Features:
- **Template Inheritance**: `{% extends "base.html" %}`
- **Content Blocks**: `{% block content %}...{% endblock %}`
- **Conditional Display**: `{% if user_authenticated %}...{% endif %}`
- **URL Generation**: `{{ url_for('auth.login') }}`
- **Flash Messages**: Bootstrap alert integration

## 🛡️ Security Features

### Session Security:
- Secure cookies in production (HTTPS only)
- HttpOnly cookies (prevent XSS)
- SameSite=Lax (CSRF protection)
- 1-hour session timeout

### Input Validation:
- Marshmallow schemas validate all user data
- Email format validation
- URL format validation for profile pictures
- Graceful handling of validation errors

### Error Handling:
- Custom error pages (404, 500, 403)
- Comprehensive logging of errors
- User-friendly error messages
- No sensitive data in error responses

## 📊 Data Flow

### User Profile Data Flow:
```
Auth0 UserInfo
    ↓
validation.py (Marshmallow schema)
    ↓
Cleaned/validated data
    ↓
Flask session storage
    ↓
Template rendering
    ↓
HTML displayed to user
```

### Request Processing Flow:
```
HTTP Request
    ↓
Flask routing
    ↓
Authentication check (decorators.py)
    ↓
Route handler (routes.py)
    ↓
Template rendering
    ↓
HTTP Response
```

## 🔧 Development Tools Integration

### Code Quality:
- **Black**: Code formatting
- **Flake8**: Style guide enforcement  
- **Pylint**: Code analysis and linting
- **isort**: Import sorting

### Security Tools:
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checking
- **CodeQL**: GitHub security analysis

## 🚀 Deployment Considerations

### Environment Variables Required:
```
# Auth0 Configuration
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret  
AUTH0_DOMAIN=your-domain.auth0.com
APP_SECRET_KEY=your-secret-key

# Optional for Codespaces
CODESPACE_NAME=auto-set-by-github
```

### URLs to Configure in Auth0:
- Callback URL: `{BASE_URL}/auth/callback`
- Logout URL: `{BASE_URL}`
- Web Origins: `{BASE_URL}`

## 🎯 Key Concepts for Interns

### Flask Application Factory Pattern:
Instead of creating the Flask app globally, we use a factory function that:
- Accepts configuration parameters
- Returns a configured Flask instance
- Allows multiple app instances for testing
- Separates configuration from application logic

### Blueprint Pattern:
Blueprints organize related routes and functionality:
- `auth` blueprint handles all authentication routes
- Blueprints can be registered with URL prefixes
- Promotes modular, maintainable code
- Easy to test individual components

### OAuth2 Flow:
OAuth2 is a secure way to handle authentication:
- User never enters password in our app
- Auth0 handles password security
- We receive user profile data after successful login
- Tokens can be revoked by the user at any time

### Environment-Based Configuration:
The app adapts behavior based on where it's running:
- Development: Helpful debugging, less security
- Production: Maximum security, minimal debugging
- Testing: Isolated environment for automated tests

This architecture ensures the application is secure, maintainable, and scalable!
"""
