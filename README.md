# Social Network for Language Learning

This project is composed of several services written in Python and TypeScript. Each service can be launched separately.

## Services
- **Gateway** (`Gateway/`)
- **Registry** (`Registry/`)
- **User Service** (`user_service/`)
- **Communication Service** (`communication_service/`)
- **Admin Service** (`admin_service/`)
- **GPT Service** (`gpt_servis/`)
- **Angular Client** (`client/`)

## Quick start
1. Install Python 3.12 and Node.js (>=18).
2. For every Python service install dependencies:
   ```bash
   cd SERVICE && pip install -r requirements.txt
   ```
3. Copy `.env` files or adjust the variables for your environment. Default examples are provided inside the service directories.
4. Apply migrations for Django based services:
   ```bash
   python manage.py migrate
   ```
5. Run the services (each in its own terminal):
   ```bash
   # Registry
   cd Registry && python manage.py runserver 8001

   # Gateway
   cd Gateway && uvicorn main:app --port 8000

   # User service
   cd user_service && python manage.py runserver 8003

   # Communication service
   cd communication_service && python manage.py runserver 8002

   # Admin service
   cd admin_service && python manage.py runserver 8006

   # GPT service
   cd gpt_servis && uvicorn main:app --port 8005
   ```
6. Start the Angular client:
   ```bash
   cd client && npm install && npm start
   ```

Once all services are running you can open the client at `http://localhost:4200/`.
