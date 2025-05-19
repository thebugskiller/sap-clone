# CRUD System with File Upload

This project is a basic CRUD (Create, Read, Update, Delete) system with file upload capabilities, built using FastAPI and React.

## Features
- CRUD operations for items
- File upload support for PNG, JPEG, and BMP formats
- Modern React frontend
- FastAPI backend with automatic API documentation

## Project Structure
```
.
├── backend/         # FastAPI backend
└── frontend/        # React frontend
```

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm start
   ```

## API Documentation
Once the backend server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment
The application is configured for deployment on Railway. 