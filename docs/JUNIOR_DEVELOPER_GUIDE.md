"""
Personal Finance Coach - Junior Developer Guide
=============================================

This guide is specifically written for junior software developers and interns
to understand how to work with this Flask application effectively.

## 🎯 Learning Objectives

After reading this guide and exploring the codebase, you should understand:
- How Flask applications are structured using blueprints
- How OAuth2 authentication works with Auth0
- How templates and routing work together
- How to add new features to the application
- How to debug common issues

## 📚 Prerequisites

### What you should know:
- Basic Python programming
- HTML and CSS fundamentals
- Basic understanding of HTTP requests/responses
- Command line basics

### What you'll learn here:
- Flask web framework
- OAuth2 authentication flow
- Jinja2 templating
- Session management
- Environment-based configuration

## 🧭 How to Navigate the Codebase

### Start Here - Main Entry Points:
1. **`run.py`** - Application startup (READ THIS FIRST)
2. **`app/__init__.py`** - Application factory and configuration
3. **`app/auth/routes.py`** - Authentication logic
4. **`app/templates/`** - HTML templates

### Understanding the File Structure:
```
personal_finance_coach/
│
├── run.py                    # 🚀 START HERE - App entry point
├── requirements.txt          # 📦 Python dependencies
├── .env                     # 🔐 Environment variables (create this)
│
├── app/                     # 📁 Main application package
│   ├── __init__.py         # 🏭 Application factory (READ SECOND)
│   ├── config.py           # ⚙️  Configuration classes
│   ├── logging_config.py   # 📝 Logging setup
│   ├── validation.py       # ✅ Data validation
│   │
│   ├── auth/               # 🔐 Authentication module
│   │   ├── __init__.py     # Blueprint setup
│   │   ├── routes.py       # Auth routes (READ THIRD)
│   │   └── decorators.py   # Auth decorators
│   │
│   └── templates/          # 🎨 HTML templates
│       ├── base.html       # Master template
│       ├── home.html       # Landing page
│       └── auth/           # Auth-specific templates
│
├── logs/                   # 📊 Application logs
└── docs/                   # 📖 Documentation
```

## 🔧 Development Workflow

### 1. Setting Up Your Environment
```bash
# Clone the repository
git clone <repository-url>
cd personal_finance_coach

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example if available)
# Add your Auth0 credentials here
```

### 2. Understanding the .env File
```bash
# Required environment variables
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret
AUTH0_DOMAIN=your-domain.auth0.com
APP_SECRET_KEY=your-secret-key

# Optional - auto-set in Codespaces
CODESPACE_NAME=your-codespace-name
```

### 3. Running the Application
```bash
# Start the development server
python run.py

# Or with environment variables
FLASK_ENV=development FLASK_DEBUG=true python run.py
```

### 4. Accessing the Application
- **Local**: http://localhost:5000
- **Codespaces**: Check the Ports tab for forwarded URL

## 🕵️ Debugging Guide

### Common Issues and Solutions:

#### 1. "Missing Auth0 configuration" Error
**Problem**: Required Auth0 environment variables not set
**Solution**: 
- Check your `.env` file exists
- Verify all Auth0 variables are set
- Ensure no extra quotes around values

#### 2. "Authentication failed" Error
**Problem**: Auth0 configuration mismatch
**Solution**:
- Check Auth0 dashboard callback URLs
- Ensure URLs match your environment (localhost vs Codespaces)
- Verify Auth0 client ID and secret

#### 3. Template Not Found Error
**Problem**: Flask can't find HTML template
**Solution**:
- Check template path in `render_template()` call
- Ensure template exists in `app/templates/` directory
- Check for typos in template names

#### 4. Import Errors
**Problem**: Python can't find modules
**Solution**:
- Ensure virtual environment is activated
- Check PYTHONPATH includes current directory
- Verify all files have `__init__.py` in package directories

### Debugging Tools:

#### 1. Flask Debug Mode
```bash
# Enable debug mode for detailed error pages
FLASK_DEBUG=true python run.py
```

#### 2. Logging
```python
# Add logging to your code
import logging
logger = logging.getLogger(__name__)

# In your function
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

#### 3. Print Debugging (Quick and Dirty)
```python
# Add temporary print statements
def callback():
    token = oauth.auth0.authorize_access_token()
    print(f"DEBUG: Token received: {token}")  # Remove before committing!
```

#### 4. Browser Developer Tools
- **Network tab**: See HTTP requests/responses
- **Console tab**: JavaScript errors
- **Application tab**: Check cookies and session data

## 🛠️ Adding New Features

### Example: Adding a New Route

#### 1. Add Route to Blueprint
```python
# In app/auth/routes.py
@bp.route("/profile")
@requires_auth  # Ensure user is logged in
def profile():
    """Display user profile page."""
    profile = session.get("profile")
    return render_template("auth/profile.html", profile=profile)
```

#### 2. Create Template
```html
<!-- In app/templates/auth/profile.html -->
{% extends "base.html" %}

{% block title %}Profile - Personal Finance Coach{% endblock %}

{% block content %}
<h1>User Profile</h1>
<p>Name: {{ profile.name }}</p>
<p>Email: {{ profile.email }}</p>
{% endblock %}
```

#### 3. Add Navigation Link
```html
<!-- In app/templates/base.html or other templates -->
<a href="{{ url_for('auth.profile') }}">Profile</a>
```

### Example: Adding Form Validation

#### 1. Create Schema in validation.py
```python
class FinanceDataSchema(Schema):
    amount = fields.Decimal(required=True, validate=validate.Range(min=0))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    date = fields.Date(required=True)
```

#### 2. Use in Route
```python
@bp.route("/add-expense", methods=["GET", "POST"])
@requires_auth
def add_expense():
    if request.method == "POST":
        schema = FinanceDataSchema()
        try:
            validated_data = schema.load(request.form)
            # Process the validated data
            flash("Expense added successfully!", "success")
        except ValidationError as e:
            flash(f"Validation error: {e.messages}", "error")
    
    return render_template("auth/add_expense.html")
```

## 🔍 Code Reading Tips

### 1. Follow the Request Flow
When understanding a feature, trace the complete request flow:
```
User action (click button)
    ↓
HTML template (form submission)
    ↓
Flask route (Python function)
    ↓
Data processing/validation
    ↓
Template rendering
    ↓
HTML response to user
```

### 2. Understand Decorators
```python
@bp.route("/dashboard")    # Maps URL to function
@requires_auth            # Checks if user is logged in
def dashboard():          # The actual function
    pass
```

### 3. Template Inheritance
```html
<!-- base.html - Parent template -->
{% block content %}{% endblock %}

<!-- dashboard.html - Child template -->
{% extends "base.html" %}
{% block content %}
    <!-- This replaces the block in base.html -->
{% endblock %}
```

### 4. Configuration Pattern
```python
# Different configs for different environments
class DevelopmentConfig(Config):
    DEBUG = True          # Show detailed errors
    
class ProductionConfig(Config):
    DEBUG = False         # Hide errors from users
```

## 🎓 Learning Exercises

### Beginner Exercises:
1. **Add a new page**: Create a "About" page with your own template
2. **Modify styling**: Change colors or layout in templates
3. **Add logging**: Add log messages to understand program flow
4. **Environment variables**: Add a new config variable and use it

### Intermediate Exercises:
1. **Form handling**: Create a form that accepts user input
2. **Data validation**: Add validation for the form data
3. **Session data**: Store and retrieve custom data in user sessions
4. **Error handling**: Add custom error pages and handling

### Advanced Exercises:
1. **Database integration**: Add SQLite database for storing user data
2. **API endpoints**: Create JSON API endpoints for mobile apps
3. **Background tasks**: Add asynchronous task processing
4. **Testing**: Write unit tests for your new features

## 📖 Additional Resources

### Flask Documentation:
- [Flask Quickstart](https://flask.palletsprojects.com/quickstart/)
- [Flask Blueprints](https://flask.palletsprojects.com/blueprints/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/templates/)

### Auth0 Documentation:
- [Auth0 Python SDK](https://auth0.com/docs/quickstart/webapp/python)
- [OAuth2 Flow](https://auth0.com/docs/authorization/flows/authorization-code-flow)

### Python Packages Used:
- [Flask](https://flask.palletsprojects.com/)
- [Authlib](https://authlib.org/)
- [Marshmallow](https://marshmallow.readthedocs.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

## 🤝 Getting Help

### When You're Stuck:
1. **Read error messages carefully** - they usually tell you what's wrong
2. **Check the logs** - look in `logs/error.log` for detailed errors
3. **Use print debugging** - add print statements to see what's happening
4. **Search for similar errors** - Google the error message
5. **Ask for help** - don't struggle alone!

### Good Questions to Ask:
- "I'm getting this error: [error message]. I've tried [what you tried]."
- "I want to add [feature]. Which files should I look at?"
- "I don't understand how [concept] works. Can you explain it?"

### Questions to Avoid:
- "It doesn't work" (be specific about what's not working)
- "Can you fix this for me?" (try to understand the solution)

Remember: Every senior developer was once a junior developer. Don't be afraid to ask questions and make mistakes - that's how you learn! 🚀
"""
