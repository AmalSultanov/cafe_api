# CafeAPI - Food Ordering & Management System

A comprehensive FastAPI-based cafe management and ordering system that provides a robust backend for managing users, meals, categories, shopping carts, and orders. The API supports multi-platform user authentication (Telegram and Web), real-time event processing with Kafka, and includes a built-in admin dashboard for easy management.

---

## 🗂️ Contents

* [Project Structure](#-project-structure)
* [Entities Involved](#%EF%B8%8F-entities-involved)
* [Tech Stack](#-tech-stack)
* [How to Run the App](#-how-to-run-the-app)
* [Environment Variables](#%EF%B8%8F-environment-variables)
* [API Documentation](#-api-documentation)
  * [API Endpoints](#%EF%B8%8F-api-endpoints)
  * [Interactive API Docs & Access](#-interactive-api-docs--access)
* [Future Work](#-future-work)

---

## 📁 Project Structure

The project follows a clean architecture pattern with clear separation of concerns and event-driven design:

```
cafe_api/
│
├── src/
│   ├── admin/            # Admin dashboard config, models and custom endpoints for meals bulk insertion
│   ├── controllers/      # Versioned API route handlers
│   ├── core/             # Core configurations, dependencies, and utilities
│   ├── exceptions/       # Custom exception classes and global handlers
│   ├── message_broker/   # Event-driven architecture components
│   ├── models/           # SQLAlchemy database models with relationships
│   ├── repositories/     # Data access layer with interface abstractions
│   ├── schemas/          # Pydantic models for request/response validation
│   ├── services/         # Business logic layer with service interfaces
│   ├── __init__.py
│   └── main.py           # Application entry point
│
├── .env.example
├── .gitignore
└── README.md
```

---

### 🖼️ Entities Involved

The system uses PostgreSQL with the following main entities and relationships:

- **Users**: User profiles with phone-based auth
- **UserIdentities**: Multi-platform identity management (Telegram/Web) with provider-specific usernames
- **MealCategories**: Meal categorization with descriptions
- **Meals**: Menu items with pricing, descriptions, and images
- **Carts**: User shopping carts with total price calculation
- **CartItems**: Individual items in shopping carts with quantity and pricing
- **Orders**: Complete orders with delivery information and status tracking
- **OrderItems**: Items within orders with final quantity and pricing

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy** 
- **Alembic** 
- **JWT**
- **FastStream (Apache Kafka)**
- **FastAPI-Amis-Admin**
- **AWS S3**
- **Docker**

---

## 🚀 How to Run the App

### 🐳 Using Docker

1. **Clone the repository**

   ```bash
   git clone https://github.com/AmalSultanov/cafe_api.git
   cd freq_counter
   ```

2. **Create a `.env` file and set environment variables in any editor**

   Refer to the [⚙️ Environment Variables](#-environment-variables) section for clarification.

   ```bash
   cp .env.example .env
   nano .env
   ```

3. **Build and run using Docker Compose**

   ```bash
   docker compose up --build
   ```

4. The app will be available at [`http://127.0.0.1`](http://127.0.0.1). Interactive Swagger docs will be available at [`http://127.0.0.1/api/docs`](http://127.0.0.1/api/docs)

---

## ⚙️ Environment Variables

The application uses the following environment variables (check `.env.example`):

### FastAPI
- `FASTAPI_HOST` - Host for the FastAPI server (e.g., `127.0.0.1`)
- `FASTAPI_PORT` - Port number for FastAPI (e.g., `8000`)
- `FASTAPI_DEBUG` - Enable debug mode (`True` or `False`)
- `FASTAPI_VERSION` - Application version (e.g., `1.0.0`)

### PostgreSQL
- `POSTGRES_DB` - PostgreSQL database name (e.g., `cafe_db`)
- `POSTGRES_USER` - PostgreSQL username (e.g., `postgres`)
- `POSTGRES_PASSWORD` - PostgreSQL password (e.g., `postgres`)
- `POSTGRES_HOST` - Host for PostgreSQL (e.g., `localhost` or a Docker Compose service name)
- `POSTGRES_PORT` - Port number for PostgreSQL (e.g., `5432`)

### JWT
- `JWT_SECRET_KEY` - Secret key for signing access tokens
- `JWT_REFRESH_SECRET_KEY` - Secret key for signing refresh tokens
- `JWT_ALGORITHM` - JWT signing algorithm (e.g., `HS256`)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiration time in minutes (e.g., `15`)
- `JWT_REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiration time in days (e.g., `1`)

### Kafka
- `KAFKA_HOST` - Kafka broker host (e.g., `localhost`)
- `KAFKA_PORT` - Kafka broker port (e.g., `9092`)

### AWS S3
- `AWS_ACCESS_KEY_ID` - AWS access key ID
- `AWS_SECRET_ACCESS_KEY` - AWS secret access key
- `AWS_REGION` - AWS region (e.g., `us-east-1`)
- `AWS_S3_BUCKET_NAME` - S3 bucket name for storing meals images (e.g., `cafe-api-meals-bucket`)

You can customize these based on your working environment.

---

## 🧾 API Documentation

This backend provides the following main API groups:

- `/meal-categories/*` - Create, list, update, and delete meal categories  
- `/meal-categories/{category_id}/meals/*` - Manage meals within categories (CRUD operations)  
- `/users/*` - User registration, login, identity management, and profile operations
- `/users/{user_id}/cart/*` - Shopping cart creation, retrieval, and deletion  
- `/users/{user_id}/cart/items/*` - Add, update, remove and clear cart items  
- `/users/{user_id}/orders/*` - Create and manage user orders

### 🔗 API Endpoints

### Meal Categories

| Method   | Path                                    | Description               |
|----------|-----------------------------------------|---------------------------|
| `POST`   | `/api/v1/meal-categories`               | Create a category         |
| `GET`    | `/api/v1/meal-categories`               | List paginated categories |
| `GET`    | `/api/v1/meal-categories/{category_id}` | Get a category            |
| `PATCH`  | `/api/v1/meal-categories/{category_id}` | Update a category         |
| `DELETE` | `/api/v1/meal-categories/{category_id}` | Delete a category         |

### Meals

| Method   | Path                                                    | Description                      |
|----------|---------------------------------------------------------|----------------------------------|
| `POST`   | `/api/v1/meal-categories/{category_id}/meals`           | Create a meal                    |
| `GET`    | `/api/v1/meal-categories/{category_id}/meals`           | List paginated meals in category |
| `GET`    | `/api/v1/meal-categories/{category_id}/meals/{meal_id}` | Get meal details                 |
| `PUT`    | `/api/v1/meal-categories/{category_id}/meals/{meal_id}` | Fully update a meal              |
| `PATCH`  | `/api/v1/meal-categories/{category_id}/meals/{meal_id}` | Partially update a meal          |
| `DELETE` | `/api/v1/meal-categories/{category_id}/meals/{meal_id}` | Delete a meal                    |

### Users

| Method   | Path                                                                                            | Description                    |
|----------|-------------------------------------------------------------------------------------------------|--------------------------------|
| `POST`   | `/api/v1/users/register`                                                                        | Register a new user            |
| `POST`   | `/api/v1/users/log-in`                                                                          | Log in a user                  |
| `POST`   | `/api/v1/users/{user_id}/logout`                                                                | Log out a user                 |
| `GET`    | `/api/v1/users/me`                                                                              | Get current user info          |
| `GET`    | `/api/v1/users/check-identity?provider=provider_name&provider_id=provider_id&username=username` | Check identity existence in db |
| `GET`    | `/api/v1/users/by-provider?provider=provider_name&provider_id=provider_id&username=username`    | Get identity                   |
| `GET`    | `/api/v1/users`                                                                                 | List paginated users           |
| `GET`    | `/api/v1/users/{user_id}`                                                                       | Get user details               |
| `PUT`    | `/api/v1/users/{user_id}`                                                                       | Fully update a user            |
| `PATCH`  | `/api/v1/users/{user_id}`                                                                       | Partially update a user        |
| `DELETE` | `/api/v1/users/{user_id}`                                                                       | Delete a user                  |

### Shopping Cart

| Method   | Path                           | Description      |
|----------|--------------------------------|------------------|
| `POST`   | `/api/v1/users/{user_id}/cart` | Create a cart    |
| `GET`    | `/api/v1/users/{user_id}/cart` | Get cart details |
| `DELETE` | `/api/v1/users/{user_id}/cart` | Delete a cart    |

### Cart Items

| Method   | Path                                           | Description            |
|----------|------------------------------------------------|------------------------|
| `POST`   | `/api/v1/users/{user_id}/cart/items`           | Add an item to cart    |
| `GET`    | `/api/v1/users/{user_id}/cart/items`           | Get cart items         |
| `GET`    | `/api/v1/users/{user_id}/cart/items/{item_id}` | Get specific cart item |
| `PATCH`  | `/api/v1/users/{user_id}/cart/items/{item_id}` | Update a cart item     |
| `DELETE` | `/api/v1/users/{user_id}/cart/items/{item_id}` | Remove a cart item     |
| `DELETE` | `/api/v1/users/{user_id}/cart/items`           | Clear cart             |

### Orders

| Method   | Path                                        | Description             |
|----------|---------------------------------------------|-------------------------|
| `POST`   | `/api/v1/users/{user_id}/orders`            | Create order from cart  |
| `GET`    | `/api/v1/users/{user_id}/orders`            | Get user orders         |
| `GET`    | `/api/v1/users/{user_id}/orders/{order_id}` | Get a specific order    |
| `DELETE` | `/api/v1/users/{user_id}/orders/{order_id}` | Delete a specific order |
| `DELETE` | `/api/v1/users/{user_id}/orders`            | Get all orders          |

### 🧪 Interactive API Docs & Access

Once the server is running, access the various interfaces:

- **Swagger UI**: http://localhost/docs - Interactive API documentation
- **ReDoc**: http://localhost/redoc - Read-only API documentation
- **Admin Dashboard**: http://localhost/admin - Administrative interface
- **Health Check**: http://localhost/api/v1/health - Application health status

---

## 🔮 Future Work

### Planned Features
- **Payment Integration**: Click/PayMe integration for online payments
- **Delivery Tracking**: GPS-based delivery tracking system

### Technical Improvements
- **Comprehensive Testing**: Unit, integration, and end-to-end tests
- **Performance Optimization**: Database query optimization and caching
- **Monitoring & Logging**: Structured logging with ELK stack integration
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **API Rate Limiting**: Request throttling and abuse prevention
