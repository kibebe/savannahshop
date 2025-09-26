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
