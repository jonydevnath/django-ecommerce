# E-Commerce Platform - Django & React

> 🎓 A comprehensive e-commerce application built with Django REST Framework and React, following professional development practices.

## 📋 Project Overview

This is a full-stack e-commerce platform built as part of a 12-week learning journey. The project demonstrates:

- **Backend**: Django + Django REST Framework
- **Frontend**: React (Coming in Week 8)
- **Async Processing**: Celery + Redis
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Deployment**: Render (Backend) + Vercel (Frontend)

## 🎯 Learning Objectives

### Core Competencies
- ✅ Django MVT architecture and request lifecycle
- ✅ ORM mastery (relations, optimization, aggregations)
- ✅ RESTful API design with DRF
- ✅ JWT authentication & authorization
- ✅ Asynchronous task processing with Celery
- ✅ Full-stack integration (Django + React)
- ✅ Production deployment & DevOps

### Interview Readiness
This project is designed to make you job-ready with:
- Real-world e-commerce domain logic
- Production-grade code structure
- Performance optimization techniques
- Security best practices
- Professional Git workflow

## 🏗️ Project Structure

```
ecom/
├── venv/                    # Virtual environment
├── config/                  # Django project settings (will create)
├── apps/
│   ├── users/              # User authentication & profiles
│   ├── products/           # Product catalog
│   └── orders/             # Order management
├── .gitignore
├── README.md
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- PostgreSQL (for production)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ecom
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Start development server**
```bash
python manage.py runserver
```
## 👨‍💻 Development Practices

- **Code Quality**: Following PEP 8, Django best practices
- **Version Control**: Feature branches, meaningful commits
- **Documentation**: In-code comments, README, API docs
- **Testing**: Unit tests, integration tests (coming soon)

## 🎯 Interview Highlights

> "This project demonstrates my ability to build production-ready e-commerce platforms using Django, implement secure authentication with JWT, optimize database queries, handle asynchronous tasks with Celery, and deploy full-stack applications to cloud platforms."

## 📝 License

This project is for educational purposes.

---

**Built with 💻 by Jony Dev Nath** | Following the 12-week E-commerce Roadmap
