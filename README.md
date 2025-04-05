<div align="left">
    <div style="display: inline-block;">
        <h2 style="display: inline-block; vertical-align: middle; margin-top: 0;">STATISTICS-BASED-ON-PKDD-99-FINANCIAL-DATA-SET</h2>
    </div>
</div>

##  Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Project Roadmap](#project-roadmap)

---

##  Overview

This project is a web application built with Flask, SQLAlchemy, and Dash that visualizes and provides access to the PKDD'99 Discovery Challenge Financial Data Set. It features user authentication, data visualization dashboards, and the ability to download cleaned datasets.

Key Features:
- Interactive data visualization dashboard
- User authentication system
- Secure data download functionality
- Automated environment setup using Docker
- PostgreSQL database integration

---

##  Project Structure

```sh
└── Statistics-based-on-PKDD-99-Financial-Data-Set/
    ├── PKDD/                          # Main application package
    │   ├── dash_page/                 # Dash visualization components
    │   │   ├── dash_charts.py         # Charts and dashboard layout
    │   │   └── sql_queries.py         # Database queries for visualizations
    │   ├── financial_db/              # Database models and operations for Dash part of app
    │   │   ├── data_manipulation.py   # Data cleaning and processing
    │   │   └── financial_models.py    # SQLAlchemy models
    │   ├── static/                    
    │   │   └── cleaned_csvs/          # Processed data files
    │   │   └── cleaned_csvs.zip       # Data for users ready to download 
    │   ├── templates/                 # Flask HTML templates
    │   │   ├── ...                    
    │   └── users/                     # User authentication module
    │       ├── forms.py               # Flask-WTF forms
    │       ├── routes.py              # User-related routes
    │       └── users_models.py        # User database models                  
    ├── docker-init/                   # Docker initialization
    │   └── Dockerfile                 # Dockerfile for create_db_app.py database creation
    ├── csv/                           # Original PKDD'99 dataset
    │   ├── ...                
    ├── app.py                        # Flask application main file 
    ├── create_db_app.py              # Database initialization script
    ├── docker-compose.yaml           # Main app Docker Compose 
    ├── docker-compose.app.yaml       # init Docker Compose 
    ├── Dockerfile                    # Main application container
    ├── gunicorn.conf.py              # Gunicorn WSGI server config
    ├── init.sql                      # Simple database creation script
    ├── nginx.conf                    # Nginx reverse proxy config
    ├── requirements.txt    
```


---

###  Prerequisites

- Docker and Docker Compose

Note: All other dependencies (Python, PostgreSQL, etc.) are automatically handled by Docker containers.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/Statistics-based-on-PKDD-99-Financial-Data-Set.git
cd Statistics-based-on-PKDD-99-Financial-Data-Set
```

2. Build and run with Docker Compose:
```bash
docker-compose --profile init up db-init
```
```bash
docker-compose -f docker-compose.app.yaml up
```

---

##  Project Roadmap

Completed:
- [X] **`Task 1`**: <strike>Data cleaning and initial database setup with dash application foundation</strike>
- [X] **`Task 2`**: <strike>Created interconnected pages and user authentication database</strike>
- [X] **`Task 3`**: <strike>Implemented secure data download for authenticated users</strike>
- [X] **`Task 4`**: <strike>Automated environment setup with Docker</strike>

Planned:
- [ ] **`Task 5`**: Enable https protocol and recaptcha
- [ ] **`Task 6`**: Synchronize testing and application building processes, implement exception handling
- [ ] **`Task 7`**: Enhance dashboard functionality and data visualization features
- [ ] **`Task 8`**: Implement installation by uv and optimize Docker containers

---
