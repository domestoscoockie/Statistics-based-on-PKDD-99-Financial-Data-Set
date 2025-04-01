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
    ├── PKDD/                          
    │   ├── dash_page/              
    │   ├── financial_db/              
    │   ├── static/                    
    │   ├── templates/                 
    │   └── users/                     
    ├── csv/                           
    │   ├── account.asc
    │   ├── card.asc
    │   ├── client.asc
    │   ├── disp.asc
    │   ├── district.asc
    │   ├── loan.asc
    │   └── order.asc
    ├── wait-for-it.sh     
    ├── app.py     
    ├── create_db_app.py           
    ├── docker-compose.yaml          
    ├── dockerfile               
    └── requirements.txt                 
          
```


---

###  Prerequisites

- Python 3.13
- Docker and Docker Compose
- PostgreSQL
- pip (Python package manager)

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
- [X] **`Task 4`**: <strike>Automated environment setup with Docker and wait-for-it.sh</strike>

Planned:
- [ ] **`Task 5`**: Enable https protocol and recaptcha
- [ ] **`Task 6`**: Synchronize testing and application building processes, implement exception handling
- [ ] **`Task 7`**: Enhance dashboard functionality and data visualization features
- [ ] **`Task 8`**: Implement installation by uv and optimize Docker containers

---
