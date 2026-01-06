> *Part of a full-stack food ordering platform (see companion repository for backend/frontend).*

## 📁 Backend Repository README (Django)

```md
# Food Ordering Platform – Backend

The Django backend for a food ordering and prepayment platform designed to help small food vendors accept online card payments and operate more efficiently using pre-orders.

## Overview

This backend handles:
- Product and order management
- Payment processing integration
- Business logic and data persistence

The platform was built to solve a real-world problem faced by street food vendors who lose sales due to cash-only transactions and food wastage from unsold stock.

## Key Features

- REST API for frontend integration
- Order and product management
- PayFast payment gateway integration
- PostgreSQL database (Neon)
- Environment-based configuration

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL (Neon)

## Project Status

- 🟡 Work in progress
- Core system ~90% beta-ready

## Running the Backend Locally

### Prerequisites

- Python 3.x
- pip

### Setup

```bash
git clone <backend-repo-url>
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

The server will run on http://localhost:8000.


Environment Variables

Create a .env file in the backend root directory:

DATABASE_URL=your_neon_postgresql_url
PAYFAST_MERCHANT_ID=your_merchant_id
PAYFAST_MERCHANT_KEY=your_merchant_key

Sensitive credentials are excluded from version control.


What This Repo Demonstrates

Backend API design
Real-world payment integration
Secure configuration handling
Cloud-hosted database usage
Independent ownership of a production-style backend