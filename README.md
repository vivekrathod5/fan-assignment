# Ceiling Fan Control System

This project is a Ceiling Fan Control System developed using Django and Django REST Framework.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/vivekrathod5/fan-assignment.git
cd fan-assignment
```

### 2. Set Up Virtual Environment

```bash
# Install virtualenv if you haven't already
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Make sure to configure your database settings in `core/settings.py`. Then, run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create .env File

Create a .env file in the root directory of the project and add the following environment variables:
e.g. core/.env
```bash
DEBUG=True
DATABASE_ENGINE=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=

```

### 6. Run the Fixture Cammand

```bash
# To load the static data
python manage.py loaddata fans.json
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

You should now be able to access the API at `http://127.0.0.1:8000/`.

## API Endpoints
- `POST simulator/`: Fan simulator
- `POST consumption/`: Fan consumption interface
- `GET fan/consumption/`: Fan consumption data
