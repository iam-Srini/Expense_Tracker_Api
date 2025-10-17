# Expense Tracker API

A robust RESTful API for managing personal expenses with secure authentication and comprehensive expense tracking features.

## 🚀 Features

- **User Authentication** - JWT-based secure authentication system
- **Expense Management** - Full CRUD operations for expenses
- **Monthly Summaries** - Category-wise expense breakdowns
- **RESTful Design** - Clean and intuitive API endpoints
- **Secure** - Password hashing and token-based authentication

## 📚 API Documentation

**Base URL:**
```
https://y=
```

### Authentication

All protected endpoints require a Bearer Token in the request header:
```
Authorization: Bearer <access_token>
```

- **Access tokens**: Expire after 30 minutes
- **Refresh tokens**: Expire after 7 days

## 🔐 Authentication Endpoints

### Login
**POST** `/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "YourPassword@123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Refresh Token
**POST** `/refresh`

**Request:**
```json
{
  "refresh_token": "your_refresh_token"
}
```

**Response:**
```json
{
  "access_token": "new_access_token",
  "token_type": "bearer"
}
```

## 👥 User Management

### Create User
**POST** `/users/`

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "StrongPass@123"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-10-15T14:00:00Z"
}
```

### Get User by ID
**GET** `/users/{user_id}`  
*Requires authentication*

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-10-15T14:00:00Z"
}
```

### Update User
**PUT** `/users/{user_id}`  
*Requires authentication*

**Request:**
```json
{
  "name": "John R. Doe",
  "email": "john.rod@example.com",
  "password": "NewStrongPass@123"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John R. Doe",
  "email": "john.rod@example.com",
  "created_at": "2025-10-15T14:00:00Z"
}
```

### Delete User
**DELETE** `/users/{user_id}`  
*Requires authentication*

**Response:**
```
204 No Content
```

## 💰 Expense Management

### Create Expense
**POST** `/expenses/`  
*Requires authentication*

**Request:**
```json
{
  "amount": 25.50,
  "description": "Lunch with client",
  "expense_date": "2025-10-14",
  "category": "Food"
}
```

**Response:**
```json
{
  "id": 1,
  "amount": 25.5,
  "description": "Lunch with client",
  "expense_date": "2025-10-14",
  "category": "Food",
  "user_id": 1
}
```

### Get Expense by ID
**GET** `/expenses/{expense_id}`  
*Requires authentication*

**Response:**
```json
{
  "id": 1,
  "amount": 25.5,
  "description": "Lunch with client",
  "expense_date": "2025-10-14",
  "category": "Food",
  "user_id": 1
}
```

### Update Expense
**PUT** `/expenses/{expense_id}`  
*Requires authentication*

**Request:**
```json
{
  "amount": 30.00,
  "description": "Team Lunch",
  "category": "Food & Drinks"
}
```

**Response:**
```json
{
  "id": 1,
  "amount": 30.0,
  "description": "Team Lunch",
  "expense_date": "2025-10-14",
  "category": "Food & Drinks",
  "user_id": 1
}
```

### Delete Expense
**DELETE** `/expenses/{expense_id}`  
*Requires authentication*

**Response:**
```
204 No Content
```

## 📊 Reports

### Monthly Expense Summary
**GET** `/summary/{year}/{month}`  
*Requires authentication*

**Response:**
```json
{
  "year": 2025,
  "month": 10,
  "summary": [
    {
      "category": "Food",
      "total_amount": 250.50
    },
    {
      "category": "Transport",
      "total_amount": 75.00
    }
  ]
}
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- FastAPI
- Uvicorn
- Database (SQLite/PostgreSQL/MySQL)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker-api.git
   cd expense-tracker-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file:
   ```env
   DATABASE_URL=sqlite:///./expenses.db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📖 API Testing

### Using cURL Examples

#### User Registration
```bash
curl -X POST "https://your-api-domain.com/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "StrongPass@123"
  }'
```

#### User Login
```bash
curl -X POST "https://your-api-domain.com/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "StrongPass@123"
  }'
```

#### Create Expense (Authenticated)
```bash
curl -X POST "https://your-api-domain.com/expenses/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "amount": 25.50,
    "description": "Lunch with client",
    "expense_date": "2025-10-14",
    "category": "Food"
  }'
```

#### Get Monthly Summary
```bash
curl -X GET "https://your-api-domain.com/summary/2025/10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🐛 Error Handling

The API uses standard HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## 🗄️ Database Schema

### Users Table
- `id` (Integer, Primary Key)
- `name` (String)
- `email` (String, Unique)
- `password` (String, Hashed)
- `created_at` (DateTime)

### Expenses Table
- `id` (Integer, Primary Key)
- `amount` (Float)
- `description` (String)
- `expense_date` (Date)
- `category` (String)
- `user_id` (Integer, Foreign Key)

## 🔒 Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Token expiration and refresh mechanism
- Input validation and sanitization
- CORS protection

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you have any questions or run into issues, please open an issue on GitHub or contact the development team.

---
