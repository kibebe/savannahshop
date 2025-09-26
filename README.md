# SavannahShop Project

This project is a Django-based application built for the pilot assessment.  
It demonstrates a modular monolithic design using **apps** (rather than separate microservices, due to the nature of the assessment).

We have implemented CI/CD with **GitHub Actions** and local Kubernetes deployments using **Kind**.

---

## 🚀 Features

- Order management (create, list, retrieve, update, delete)
- Customer management
- Product catalog (upload, list, category price analysis)
- OpenID Connect (OIDC) authentication with Keycloak via `mozilla-django-oidc`

---

1. ### Start the Django Project

## Run the project locally

# Apply migrations

python manage.py migrate

# Create a Django superuser (will be linked to a Keycloak user)

python manage.py createsuperuser

### 2. Run Keycloak in Docker

# Start a Keycloak container locally:

docker run -d \
 --name keycloak \
 -p 8080:8080 \
 -e KEYCLOAK_ADMIN=admin \
 -e KEYCLOAK_ADMIN_PASSWORD=admin \
 quay.io/keycloak/keycloak:23.0.4 start-dev

Access the Keycloak admin console at:
👉 http://localhost:8080/

Login with:

Username: admin
Password: admin

### 3. Create a Realm

In the Keycloak admin console, create a new realm (e.g., savannahshop).

4. Create a Client in Keycloak

Inside the realm:

Client ID: savannahshop-client

Access Type: Confidential

Root URL: http://localhost:8000/

Valid Redirect URIs: http://localhost:8000/oidc/callback/\*

Web Origins: http://localhost:8000

Save the client and copy the Client Secret.
Update settings.py:

OIDC_RP_CLIENT_ID = "savannahshop-client"
OIDC_RP_CLIENT_SECRET = "<your-client-secret>"

5. Create a Keycloak User

In the Keycloak realm, create a test user (e.g., testuser).

Set a password under Credentials and disable Temporary.

This user will authenticate with your Django app through OIDC.

6. Run the Django App
   python manage.py runserver

Open: http://localhost:8000/oidc/authenticate/

Login with your Keycloak user

You’ll be redirected back to Django (/) and logged in 🎉

## 🌐 API Endpoints

### Root

- `GET /` → API root
- `GET /admin/` → Django admin panel

---

### Orders

- `GET /api/orders/` → List all orders
- `POST /api/orders/` → Create a new order
- `GET /api/orders/<id>/` → Retrieve order by ID
- `PUT /api/orders/<id>/` → Update an order
- `DELETE /api/orders/<id>/` → Delete an order

---

### Customers

- `GET /api/customers/` → Customer endpoints (extendable via `customers/urls.py`)

---

### Catalog

- `POST /api/catalog/products/upload/` → Upload product data
- `GET /api/catalog/products/` → List all products
- `GET /api/catalog/categories/<id>/average-price/` → Get average price for a category

---

### Authentication

- `GET /oidc/authenticate` → OIDC authentication endpoints (integrated with Keycloak)

---

## ⚙️ Deployment

- **CI/CD**: GitHub Actions pipeline builds and tests the project.
- **Local Kubernetes**: Uses Kind (Kubernetes in Docker) for local deployments.

---

## 📝 Notes

- We used **Django apps** instead of breaking down into microservices because the scope of this assessment required simplicity while still demonstrating modular design.
- The architecture still separates concerns (`orders`, `customers`, `catalog`) and can be evolved into microservices later if needed.

---
