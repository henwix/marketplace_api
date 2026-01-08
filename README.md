# MARKETPLACE_API - API for the e-commerce platform, allowing users to sell and buy products

## Project technology stack and Features

* 🐍 [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/) for backend and API.
* 📜 [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html) for API documentation.
* 🐘 [PostgreSQL](https://www.postgresql.org/) &ndash; SQL database.
* 🚀 [Redis](https://redis.io/) for caching.
* 📝 [Celery](https://github.com/celery/celery) and [Celery Beat](https://github.com/celery/django-celery-beat) for task queuing and scheduling.
* 🖧 [Nginx](https://nginx.org/en/) &ndash; web and proxy server.
* 🐳 [Docker Compose](https://www.docker.com/) for development and production.
* ☁️ [AWS S3](https://aws.amazon.com/s3/) & [CloudFront](https://aws.amazon.com/cloudfront/) &ndash; cloud storage service and CDN.
* 💸 [Stripe](https://stripe.com/) for payments.
* 🤖 [Certbot](https://certbot.eff.org/) for SSL certificates.
* ✅ [Pytest](https://docs.pytest.org/en/stable/) for testing.
* 📫 Email based password and username recovery.
* 🔒 Secure password hashing by default.
* 🔑 JWT (JSON Web Token) authentication.

*<u>Note: the list above contains not all but the key items only</u>*

## Requirements

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [GNU Make](https://www.gnu.org/software/make/)

## TODOs

* [ ] Users
  * [x] Models
  * [x] CRUD
  * [x] CRUD tests
  * [ ] `set_email`, `set_email_confirm` endpoints
  * [ ] User creation: email validation using Celery
  * [ ] Avatars
* [ ] Sellers
  * [x] Models
  * [x] CRUD
  * [x] CRUD tests
  * [ ] Avatars and backgrounds
* [ ] Auth
  * [x] Lazy JWT auth
  * [ ] Login endpoint
  * [ ] OTP
  * [ ] oauth2
* [ ] Products
  * [ ] Models(Products, Variants, Reviews, Images for Variants and Reviews, Categories)
  * [x] CRUD for products
  * [x] Products searching, filtering, ordering
  * [ ] Searching by category
  * [ ] Products wishlist/favorites
* [ ] Cart
  * [ ] Models
  * [ ] CRUD
  * [ ] CRUD tests
* [ ] Buyer and Seller orders
* [ ] Payments with delivery addresses
