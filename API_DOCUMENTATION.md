# Meditrack API - Complete Documentation

## Overview
This document explains all the advanced features added to the Meditrack REST API, including role-based permissions, JWT authentication, filtering, pagination, and API structure.

---

## Table of Contents
1. [API Architecture](#api-architecture)
2. [Authentication](#authentication)
3. [Role-Based Access Control](#role-based-access-control)
4. [API Endpoints](#api-endpoints)
5. [Filtering, Searching & Pagination](#filtering-searching--pagination)
6. [Testing the API](#testing-the-api)
7. [Deployment Considerations](#deployment-considerations)

---

## API Architecture

### Project Structure
```
meditrack/
├── meditrack/              # Main project settings
│   ├── settings.py        # DRF config, JWT settings, pagination
│   ├── urls.py            # Root URL router (includes all app APIs)
│   └── wsgi.py
├── appointments/          # Appointment management
│   ├── api_view.py        # ViewSet with filtering/ordering
│   ├── api_urls.py        # App-level router
│   ├── permissions.py     # Custom permission classes
│   └── serializers.py     # JSON serializers
├── doctors/               # Doctor management
├── medications/           # Medication tracking
├── records/               # Patient records
└── tests/                 # API test suite
```

### API Design Principles
- **Modular**: Each app has its own router, viewset, and permissions
- **RESTful**: Standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- **Stateless**: Token-based authentication (no sessions required for API)
- **Paginated**: Large lists return 10 items per page by default
- **Searchable**: Full-text search on relevant fields
- **Sortable**: Results can be ordered by any indexed field

---

## Authentication

### JWT Token Flow

#### 1. Get a Token (Login)
**Endpoint**: `POST /api/token/`

**Request**:
```json
{
  "username": "doctor_user",
  "password": "secure_password"
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Token Details**:
- `access`: Short-lived token (15 minutes), used for API requests
- `refresh`: Long-lived token (7 days), used to get new access tokens

#### 2. Use the Token in Requests
Add the Bearer token to every API request:

```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  http://127.0.0.1:8000/api/doctors/doctor/
```

**Header Format**:
```
Authorization: Bearer <your_access_token>
```

#### 3. Refresh an Expired Token
**Endpoint**: `POST /api/token/refresh/`

**Request**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Token Configuration
Set in `meditrack/settings.py`:
- `ACCESS_TOKEN_LIFETIME`: 15 minutes
- `REFRESH_TOKEN_LIFETIME`: 7 days
- `ROTATE_REFRESH_TOKENS`: Enabled for security
- `AUTH_HEADER_TYPES`: Bearer tokens

---

## Role-Based Access Control

### Available Roles

#### 1. Admin
- Full system access
- Can create, update, delete any record
- Can manage user roles and permissions
- Django: `is_staff = True` or in `admin` group

#### 2. Doctor
- Can view assigned patients' records and appointments
- Can create and update appointments
- Cannot delete records (only admin can)
- Can read all doctor and medication information
- Django: member of `doctor` group

#### 3. Receptionist
- Can create and list appointments
- Can view patient records for scheduling
- Cannot delete or modify patient medical data
- Cannot view sensitive medication information
- Django: member of `receptionist` group

#### 4. Patient
- Can only view their own records
- Can view their own appointments
- Can view their own medications
- Read-only access
- Django: member of `patient` group

### Setting Up Roles

#### Step 1: Create Groups in Django Admin
1. Go to `/admin/`
2. Navigate to **Authentication and Authorization** → **Groups**
3. Create these groups:
   - `admin`
   - `doctor`
   - `receptionist`
   - `patient`

#### Step 2: Assign Users to Groups
1. Go to **Authentication and Authorization** → **Users**
2. Edit a user
3. Add them to the appropriate group

#### Step 3: Custom Permission Classes
Permission classes check if a user belongs to the right group:

```python
# doctors/permissions.py
from rest_framework.permissions import BasePermission

class IsDoctorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['doctor', 'admin']).exists()

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='admin').exists() or request.user.is_staff
```

### Permission Matrix

| Endpoint | Admin | Doctor | Receptionist | Patient |
|----------|-------|--------|--------------|---------|
| GET /api/doctors/doctor/ | ✅ | ✅ | ❌ | ❌ |
| POST /api/doctors/doctor/ | ✅ | ❌ | ❌ | ❌ |
| GET /api/appointments/appointment/ | ✅ | ✅ Own | ✅ | ✅ Own |
| POST /api/appointments/appointment/ | ✅ | ✅ | ✅ | ❌ |
| DELETE /api/records/record/ | ✅ | ❌ | ❌ | ❌ |
| GET /api/medications/medication/ | ✅ | ✅ | ❌ | ✅ Own |

---

## API Endpoints

### Doctors API
**Base URL**: `/api/doctors/doctor/`

#### List All Doctors
```
GET /api/doctors/doctor/
```
Query Parameters:
- `search=cardiology` - Search by name, specialization
- `ordering=doctor_name` - Sort by name
- `page=1` - Pagination

Example:
```bash
curl -H "Authorization: Bearer <token>" \
  "http://127.0.0.1:8000/api/doctors/doctor/?search=cardiology&ordering=doctor_name"
```

#### Create Doctor (Admin Only)
```
POST /api/doctors/doctor/
Content-Type: application/json

{
  "doctor_name": "Dr. Smith",
  "specialization": "Cardiology",
  "availability": "Monday-Friday 9AM-5PM"
}
```

#### Retrieve Doctor
```
GET /api/doctors/doctor/{id}/
```

#### Update Doctor (Admin Only)
```
PUT /api/doctors/doctor/{id}/
PATCH /api/doctors/doctor/{id}/
```

#### Delete Doctor (Admin Only)
```
DELETE /api/doctors/doctor/{id}/
```

### Appointments API
**Base URL**: `/api/appointments/appointment/`

#### List Appointments
```
GET /api/appointments/appointment/?search=smith&ordering=-date&page=1
```

#### Create Appointment (Doctor/Receptionist)
```
POST /api/appointments/appointment/

{
  "patient_name": 1,
  "doctor_name": 1,
  "date": "2026-06-30",
  "time": "14:30:00",
  "status": "scheduled"
}
```

#### Update Appointment Status
```
PATCH /api/appointments/appointment/{id}/

{
  "status": "completed"
}
```

Status choices: `scheduled`, `confirmed`, `completed`, `canceled`

### Records API
**Base URL**: `/api/records/record/`

#### List Patient Records
```
GET /api/records/record/?search=john&ordering=patient_name
```

#### Create Patient Record (Doctor/Admin)
```
POST /api/records/record/

{
  "patient_name": "John Doe",
  "age": 35,
  "gender": "male",
  "contact": "555-1234",
  "address": "123 Main St",
  "blood_group": "O+"
}
```

### Medications API
**Base URL**: `/api/medications/medication/`

#### List Medications
```
GET /api/medications/medication/?search=aspirin&ordering=-start_date
```

#### Add Medication (Doctor Only)
```
POST /api/medications/medication/

{
  "patient_name": 1,
  "medication_name": "Aspirin",
  "dosage": "500mg",
  "frequency": "twice daily",
  "start_date": "2026-06-01",
  "end_date": "2026-06-30"
}
```

---

## Filtering, Searching & Pagination

### Global Settings
Configured in `meditrack/settings.py`:

```python
'DEFAULT_FILTER_BACKENDS': [
    'rest_framework.filters.SearchFilter',
    'rest_framework.filters.OrderingFilter',
],
'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
'PAGE_SIZE': 10,
```

### Search
Search by multiple fields simultaneously:

```
GET /api/appointments/appointment/?search=john
```

Searchable fields per endpoint:
- **Doctors**: `doctor_name`, `specialization`, `availability`
- **Appointments**: `patient_name__patient_name`, `doctor_name__doctor_name`, `status`
- **Medications**: `medication_name`, `dosage`, `frequency`, `patient_name__patient_name`
- **Records**: `patient_name`, `contact`, `address`, `blood_group`

### Ordering
Sort results ascending or descending:

```
GET /api/appointments/appointment/?ordering=-date  # Latest first
GET /api/doctors/doctor/?ordering=doctor_name      # A-Z
```

Orderable fields:
- **Doctors**: `doctor_name`, `id`
- **Appointments**: `date`, `time`, `status`, `id`
- **Medications**: `medication_name`, `start_date`, `end_date`, `id`
- **Records**: `patient_name`, `age`, `id`

### Pagination
Results are paginated with 10 items per page:

```json
{
  "count": 45,
  "next": "http://127.0.0.1:8000/api/doctors/doctor/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "doctor_name": "Dr. Smith",
      ...
    },
    ...
  ]
}
```

Navigate pages:
```
GET /api/doctors/doctor/?page=1
GET /api/doctors/doctor/?page=2
```

---

## Testing the API

### Method 1: Using cURL

#### Get Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_user","password":"your_pass"}'
```

#### Use Token
```bash
curl -H "Authorization: Bearer <access_token>" \
  http://127.0.0.1:8000/api/doctors/doctor/
```

#### Create Appointment
```bash
curl -X POST http://127.0.0.1:8000/api/appointments/appointment/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": 1,
    "doctor_name": 1,
    "date": "2026-06-30",
    "time": "14:00:00",
    "status": "scheduled"
  }'
```

### Method 2: Using Postman

1. Create a new collection "Meditrack API"
2. Add requests for each endpoint
3. Store token in Postman variable:
   - Get token, copy `access` value
   - Set env variable: `{{token}}`
4. Use in headers: `Authorization: Bearer {{token}}`

### Method 3: Browsable API
1. Log in at `/api-auth/login/`
2. Navigate to any endpoint
3. Use the HTML form to test requests

### Expected Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (no token) |
| 403 | Forbidden (permission denied) |
| 404 | Not Found (endpoint/resource) |
| 500 | Server Error |

---

## Deployment Considerations

### Production Checklist

1. **Secret Key**: Change `SECRET_KEY` in settings.py
   ```python
   SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
   ```

2. **Debug Mode**: Disable in production
   ```python
   DEBUG = False
   ```

3. **Allowed Hosts**: Specify production domain
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

4. **HTTPS**: Force SSL
   ```python
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

5. **Database**: Use production database
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.environ.get('DB_NAME'),
           'USER': os.environ.get('DB_USER'),
           'PASSWORD': os.environ.get('DB_PASSWORD'),
           'HOST': os.environ.get('DB_HOST'),
           'PORT': '5432',
       }
   }
   ```

6. **JWT Settings**: Adjust expiration for production
   ```python
   SIMPLE_JWT = {
       'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
       'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
   }
   ```

7. **CORS**: If frontend is separate
   ```bash
   pip install django-cors-headers
   ```
   ```python
   INSTALLED_APPS = [..., 'corsheaders']
   MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
   CORS_ALLOWED_ORIGINS = ['https://yourdomain.com']
   ```

### Running in Production
```bash
# Collect static files
python manage.py collectstatic

# Run migrations
python manage.py migrate

# Use gunicorn or uwsgi
gunicorn meditrack.wsgi:application --bind 0.0.0.0:8000
```

---

## Error Handling

### Common Errors and Fixes

#### 401 Unauthorized
- Token missing or invalid
- **Fix**: Include valid Bearer token in Authorization header

#### 403 Forbidden
- User lacks permission for this action
- **Fix**: Check user role and permissions

#### 400 Bad Request
- Invalid data in request body
- **Fix**: Check field names and data types match serializer

#### 404 Not Found
- Endpoint or resource doesn't exist
- **Fix**: Verify URL and resource ID

#### 500 Internal Server Error
- Server-side error
- **Fix**: Check Django logs: `python manage.py runserver 2>&1 | grep ERROR`

---

## Future Enhancements

1. **Notification System**: Send appointment reminders
2. **Audit Logging**: Track who changed what and when
3. **Advanced Permissions**: Permission per hospital department
4. **Analytics Dashboard**: Patient load, appointment trends
5. **Prescription Management**: Digital prescriptions with QR codes
6. **File Upload**: Medical reports and X-ray images
7. **Real-time Updates**: WebSocket for live appointment changes
8. **Mobile App**: Native iOS/Android client
9. **Integration**: Connect with hospital management systems
10. **Compliance**: HIPAA/GDPR audit trails

---

## Support & Troubleshooting

For API issues:
1. Enable debug logging in settings.py
2. Check Django logs
3. Verify token expiration
4. Test with cURL first before using in client app
5. Check user permissions and group membership

---

**Last Updated**: June 26, 2026  
**Version**: 1.0.0
