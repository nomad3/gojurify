# Document Template Management System

A Django-based document management system that allows users to create, manage, and collaborate on document templates with built-in logic rules and workflow automation using n8n.

## 🚀 Features

- **Document Template Management**
  - Create and edit document templates
  - Version control
  - Export to PDF, Word, and Google Docs
  - Collaborative editing

- **Logic Builder**
  - Create conditional rules for document generation
  - Dynamic content based on input data
  - Version-controlled logic rules

- **Intake Forms**
  - Generate custom forms based on templates
  - Data validation
  - Export form responses

- **User Management**
  - Custom user model with extended features
  - JWT authentication
  - Role-based access control
  - Collaboration invitations

- **API Integration**
  - RESTful API endpoints
  - JWT authentication
  - Comprehensive API documentation

- **Workflow Automation**
  - n8n integration for workflow automation
  - Customizable workflow triggers
  - External service integration

## 🛠️ Technology Stack

- **Backend**: Django 3.2
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Automation**: n8n
- **Container**: Docker & Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.9+
- PostgreSQL
- n8n

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/document-management-system.git
cd document-management-system
```

2. Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@db:5432/mydb
N8N_BASIC_AUTH_USER=youruser
N8N_BASIC_AUTH_PASSWORD=yourpassword
```

3. Build and run the containers:
```bash
docker-compose up --build
```

4. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## 🚦 Usage

1. Access the application:
   - Django Admin: `http://localhost:8000/admin`
   - API: `http://localhost:8000/api`
   - n8n Dashboard: `http://localhost:5678`

2. Create document templates through the admin interface or API

3. Set up logic rules using the Logic Builder

4. Generate intake forms and collect data

5. Export documents in various formats

## 📚 API Documentation

### Authentication
```bash
POST /api/token/
POST /api/token/refresh/
```

### Document Templates
```bash
GET    /api/document-templates/
POST   /api/document-templates/
GET    /api/document-templates/{id}/
PUT    /api/document-templates/{id}/
DELETE /api/document-templates/{id}/
```

### Export Endpoints
```bash
GET /api/document-templates/{id}/export/pdf/
GET /api/document-templates/{id}/export/word/
GET /api/document-templates/{id}/export/google-docs/
```

## 🔒 Security

- JWT authentication for API access
- Role-based access control
- Secure password storage
- CSRF protection
- Rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - *Initial work* - [YourGithub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django community
- n8n team
- All contributors

## 📞 Support

For support, email support@yourdomain.com or create an issue in the repository.
```

This README provides a comprehensive overview of your project, including:
- Features and capabilities
- Technology stack
- Installation instructions
- Usage guidelines
- API documentation
- Security measures
- Contributing guidelines
- License information

You should customize it further by:
1. Adding your specific repository URL
2. Including your name and contact information
3. Adding any specific deployment instructions
4. Updating the license information
5. Adding any project-specific configuration details
6. Including screenshots or diagrams if available