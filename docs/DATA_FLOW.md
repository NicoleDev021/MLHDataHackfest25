<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Madison Nicole Goodwin https://github.com/NicoleDev021

SPDX-License-Identifier: CC-BY-4.0
-->

"""
Personal Finance Coach - Data Flow Documentation
===============================================

This document explains how data flows through the Personal Finance Coach application.
Perfect for understanding how user information moves from Auth0 to the browser.

## 🔄 Complete Authentication Data Flow

### Step 1: User Initiates Login
```
User clicks "Login" button on home.html
    ↓
Browser sends GET request to /auth/login
    ↓
Flask routes.py login() function called
    ↓
Function redirects to Auth0 with callback URL
```

**Data at this stage:**
- No user data in our system yet
- Session is empty
- Auth0 receives our callback URL in the redirect

### Step 2: Auth0 Handles Authentication
```
User enters credentials on Auth0 page
    ↓
Auth0 validates credentials
    ↓
Auth0 generates authorization code
    ↓
Auth0 redirects to our /auth/callback with code
```

**Data at this stage:**
- Authorization code (temporary, expires quickly)
- No user profile data yet
- Session still empty

### Step 3: Token Exchange and User Data Retrieval
```
Flask receives callback request with auth code
    ↓
routes.py callback() function called
    ↓
oauth.auth0.authorize_access_token() exchanges code for token
    ↓
Token contains access_token, id_token, and userinfo
```

**Data structure from Auth0:**
```python
token = {
    'access_token': 'eyJhbGciOiJSUzI1NiIs...',
    'id_token': 'eyJhbGciOiJSUzI1NiIs...',
    'userinfo': {
        'sub': 'auth0|1234567890',
        'name': 'John Doe',
        'email': 'john@example.com',
        'picture': 'https://example.com/avatar.jpg',
        'email_verified': True,
        # ... other Auth0 fields
    },
    'expires_at': 1642123456
}
```

### Step 4: Data Extraction and Cleaning
```
callback() extracts userinfo from token
    ↓
Creates profile_data dictionary with only needed fields
    ↓
Sends to validate_user_profile() in validation.py
```

**Data transformation:**
```python
# Raw Auth0 userinfo (may contain many fields)
userinfo = {
    'sub': 'auth0|1234567890',
    'name': 'John Doe',
    'email': 'john@example.com',
    'picture': 'https://example.com/avatar.jpg',
    'email_verified': True,
    'updated_at': '2024-01-01T00:00:00.000Z',
    # ... many other fields we don't need
}

# Extracted profile_data (only what we need)
profile_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'picture': 'https://example.com/avatar.jpg'
}
```

### Step 5: Data Validation (validation.py)
```
validate_user_profile() called with profile_data
    ↓
Marshmallow UserProfileSchema validates each field
    ↓
Returns validated_profile or validation error
```

**Validation rules:**
```python
class UserProfileSchema(Schema):
    name = fields.Str(
        required=True,                    # Must be present
        validate=validate.Length(min=1, max=100)  # 1-100 characters
    )
    email = fields.Email(
        required=False,                   # Optional (Auth0 might not provide)
        allow_none=True                   # Can be None/null
    )
    picture = fields.Url(
        allow_none=True,                  # Optional profile picture
        required=False
    )
```

**Validation outcomes:**
- ✅ **Success**: Returns cleaned data
- ⚠️ **Warning**: Uses fallback data if validation fails (graceful degradation)
- ❌ **Error**: Logs error but doesn't break authentication

### Step 6: Session Storage
```
validated_profile stored in Flask session
    ↓
Full token also stored for potential API calls
    ↓
session.permanent = True (enables timeout)
```

**Session data structure:**
```python
session = {
    'user': {
        # Full OAuth token (for API calls)
        'access_token': 'eyJhbGciOiJSUzI1NiIs...',
        'id_token': 'eyJhbGciOiJSUzI1NiIs...',
        'userinfo': { ... },
        'expires_at': 1642123456
    },
    'profile': {
        # Cleaned user profile (for display)
        'name': 'John Doe',
        'email': 'john@example.com',
        'picture': 'https://example.com/avatar.jpg'
    }
}
```

### Step 7: Template Rendering and Display
```
User redirected to dashboard
    ↓
dashboard() route checks session['profile']
    ↓
Passes profile data to dashboard.html template
    ↓
Jinja2 renders HTML with user data
```

**Template data flow:**
```python
# In routes.py dashboard()
userinfo = {
    'name': profile.get('name', 'Unknown'),
    'email': profile.get('email', ''),
    'picture': profile.get('picture', '')
}

# Passed to template
return render_template('auth/dashboard.html', userinfo=userinfo)
```

```html
<!-- In dashboard.html -->
<h1>Welcome, {{ userinfo.name }}!</h1>
<p>Email: {{ userinfo.email }}</p>
<img src="{{ userinfo.picture }}" alt="Profile Picture">
```

## 🏠 Home Page Data Flow

### Route Handler Logic:
```python
@app.route("/")
def home():
    # Check if user is authenticated
    user_authenticated = session.get("user") is not None
    
    # Get username for display
    username = None
    if user_authenticated:
        username = session.get("profile", {}).get("name")
    
    # Pass data to template
    return render_template(
        "home.html",
        user_authenticated=user_authenticated,
        username=username
    )
```

### Template Conditional Logic:
```html
{% if user_authenticated %}
    <h1>Welcome {{ username }}!</h1>
    <!-- Show dashboard and logout buttons -->
{% else %}
    <h1>Welcome to Personal Finance Coach</h1>
    <!-- Show login button -->
{% endif %}
```

## 🔒 Session Management Data Flow

### Session Configuration:
```python
# In app/__init__.py
app.config.update(
    SESSION_COOKIE_SECURE=True,      # HTTPS only in production
    SESSION_COOKIE_HTTPONLY=True,    # No JavaScript access
    SESSION_COOKIE_SAMESITE="Lax",   # CSRF protection
    PERMANENT_SESSION_LIFETIME=3600  # 1 hour timeout
)
```

### Session Lifecycle:
1. **Login**: Session created with user data
2. **Requests**: Session data available in all routes
3. **Timeout**: Session expires after 1 hour of inactivity
4. **Logout**: Session completely cleared

## 🚪 Logout Data Flow

### Logout Process:
```
User clicks logout button
    ↓
/auth/logout route called
    ↓
session.clear() removes all user data
    ↓
User redirected to Auth0 logout URL
    ↓
Auth0 clears its session
    ↓
User redirected back to home page
```

### Auth0 Logout URL Construction:
```python
logout_url = f"https://{app.config['AUTH0_DOMAIN']}/v2/logout?" + urlencode({
    "returnTo": app.config["BASE_URL"],           # Where to redirect after logout
    "client_id": app.config["AUTH0_CLIENT_ID"]    # Identifies our application
}, quote_via=quote_plus)
```

## 🔍 Error Handling Data Flow

### Validation Error Handling:
```
validate_user_profile() fails
    ↓
Log warning message
    ↓
Create fallback profile data
    ↓
Continue with authentication (graceful degradation)
```

### Authentication Error Handling:
```
Auth0 returns error
    ↓
Log error details
    ↓
flash() user-friendly message
    ↓
Redirect to login page
```

### Flash Message Flow:
```python
# In Python route
flash("Authentication failed. Please try again.", "error")

# In template (base.html)
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-danger">{{ message }}</div>
    {% endfor %}
{% endwith %}
```

## 📊 Data Security Considerations

### Sensitive Data Handling:
- **Passwords**: Never stored (handled by Auth0)
- **Tokens**: Encrypted in session cookies
- **Profile**: Only basic info stored (name, email, picture)
- **Logs**: No sensitive data in log files

### Data Validation:
- **Input**: All user data validated with Marshmallow
- **Output**: All template data escaped by Jinja2
- **URLs**: All URLs validated as proper format

### Session Security:
- **Encryption**: Session data encrypted with SECRET_KEY
- **HTTPS**: Secure cookies in production
- **Timeout**: Automatic session expiration
- **Cleanup**: Complete session clearing on logout

This data flow ensures user information is handled securely and efficiently throughout the application!
"""
