# Medical Claims Review System

A secure, single-page web application for reviewing, annotating, and flagging medical claim records. Built as a simulation of ERISA Recovery's claim investigation tools used by analysts to identify underpaid claims.

## 🚀 Features

### Core Functionality
- **Claim Record List View**: HTMX-powered pagination with sortable columns
- **Real-time Search & Filtering**: Full-text search by claim ID, patient name, or insurer name
- **Claim Detail Modal**: Comprehensive view of claim information including CPT codes, diagnosis codes, and financial details
- **Annotation System**: Add, view, and delete annotations on claims with real-time updates
- **Flagging Mechanism**: Toggle claims for review with instant visual feedback
- **Advanced Filtering**: Filter by claim status (approved/denied/underpaid/pending) and flagged status

### Technical Features
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Interactive UI**: Alpine.js for reactive components
- **HTMX Integration**: Seamless AJAX interactions without page reloads
- **Secure Authentication**: User login with session management
- **Sample Data**: Realistic medical claims with CPT/ICD codes

## 🛠 Technology Stack

**Backend:**
- Django
- SQLite database
- Python 3.x

**Frontend:**
- HTML5 & CSS3
- Bootstrap
- Alpine.js
- HTMX
- Bootstrap Icons

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv

### Quick Start

1. **Clone or download the project files**

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Populate sample data**
   ```bash
   python manage.py populate_sample_data --claims 100
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser to: `http://127.0.0.1:8000`
   - Login with demo credentials (see below)

## 🔐 Demo Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Administrator |
| `analyst` | `analyst123` | Claims Analyst |

## 📖 Usage Guide

### Dashboard
- View high-level statistics of claims
- Quick navigation to claims list
- Status breakdown (total, flagged, approved, denied)

### Claims List
- **Search**: Use the search bar to find claims by ID, patient name, or insurer
- **Filter**: Use dropdown filters for status and flagged state
- **Pagination**: Navigate through large datasets with HTMX-powered pagination
- **Flag Claims**: Click the flag button to mark claims for review
- **View Details**: Click "View" to open the detailed claim modal

### Claim Details Modal
- **Patient Information**: Name, service date, provider details
- **Financial Details**: Billed amount, paid amount, underpaid amount
- **Insurance Information**: Insurer name, status, denial reasons
- **Medical Codes**: CPT codes (procedures) and ICD codes (diagnoses)
- **Annotations**: Add, view, and delete notes on claims
- **Flag Status**: Toggle review flag directly from detail view

### Annotations
- **Add**: Type in the annotation box and click "Add"
- **View**: All annotations display with user and timestamp
- **Delete**: Remove your own annotations with the trash button

## 🎯 Key Features Demonstrated

### HTMX Integration
- Search results update without page refresh
- Pagination loads new data seamlessly  
- Modal content loaded dynamically
- Form submissions update UI instantly
- Flag toggles with immediate visual feedback

### Alpine.js Reactivity
- Flag button state changes reactively
- Real-time UI updates for interactive elements
- Smooth user experience with minimal JavaScript

### Django Backend
- RESTful URL patterns
- Model relationships (Claims ↔ Annotations)
- Secure authentication and authorization
- Efficient database queries with filtering/pagination

## 📁 Project Structure

```
medical_claims/
├── claims/                     # Django app
│   ├── management/
│   │   └── commands/
│   │       └── populate_sample_data.py
│   ├── migrations/
│   ├── models.py              # Claim and Annotation models
│   ├── views.py               # API endpoints and views
│   ├── urls.py                # URL routing
│   └── admin.py               # Django admin configuration
├── templates/
│   ├── base.html              # Base template with frameworks
│   └── claims/
│       ├── index.html         # Dashboard
│       ├── login.html         # Authentication
│       ├── claim_list.html    # Claims list view
│       └── partials/          # HTMX partial templates
├── medical_claims/            # Django project settings
├── requirements.txt
└── README.md
```

## 🔧 Development

### Adding New Features
1. Models: Update `claims/models.py`
2. Views: Add endpoints in `claims/views.py`
3. Templates: Create/update templates in `templates/claims/`
4. URLs: Register routes in `claims/urls.py`

### Database Management
- **Reset data**: Delete `db.sqlite3` and run migrations
- **New sample data**: `python manage.py populate_sample_data --claims N`
- **Admin interface**: Visit `/admin/` with admin credentials

### Customization
- **Styling**: Modify CSS in `templates/base.html`
- **Sample data**: Update `populate_sample_data.py` command
- **Business logic**: Extend models and views as needed

## 🐛 Troubleshooting

**Common Issues:**
- **Port already in use**: Change port with `python manage.py runserver 8001`
- **Database locked**: Stop server and try again
- **Permission errors**: Ensure virtual environment is activated
- **Static files**: Run `python manage.py collectstatic` if needed

**Performance:**
- Default pagination: 20 claims per page
- Search is case-insensitive and partial-match
- Database indexes on commonly queried fields

## 📝 Sample Data Details

The application includes realistic medical claims data:
- **75 sample claims** (configurable)
- **Real CPT codes** (procedure codes)
- **Real ICD-10 codes** (diagnosis codes)
- **Realistic denial reasons**
- **Various claim statuses** with appropriate financial amounts
- **Sample annotations** from different users

## 🔒 Security Features

- User authentication required for all features
- Session management with timeout
- CSRF protection on all forms
- XSS protection headers
- Secure user permission checks
- SQL injection protection via Django ORM

## 🌟 Future Enhancements

Potential areas for expansion:
- Advanced reporting and analytics
- Bulk claim operations
- Email notifications for flagged claims
- Audit trail for claim changes
- Export functionality (PDF, Excel)
- Advanced search with date ranges
- User role-based permissions
- Integration with external APIs

---

*This application demonstrates modern web development practices with Django, HTMX, and Alpine.js for building responsive, interactive medical data management systems.* 
