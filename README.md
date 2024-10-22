# SpicaCMS

**SpicaCMS** is a robust and scalable Content Management System (CMS) designed to streamline the creation, management, and distribution of digital content. Leveraging modern technologies such as Next.js for the frontend and Django REST Framework for the backend, SpicaCMS offers a seamless experience for both content creators and administrators.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **User Authentication & Authorization**
  - JWT-based authentication.
  - Role-based access control with predefined groups: Administrators, Moderators, Authors, and Users.
  
- **Content Management**
  - Create and manage News, Articles, and Pages.
  - Rich text editing with CKEditor integration.
  - Automated content rewriting using AI prompts via OpenAI.
  
- **Media Management**
  - Upload and manage Images, Audio, and Video files.
  - Organize media into Galleries.
  
- **Automation & Scheduling**
  - Schedule automation tasks with Celery and Redis.
  - Define automation templates to scrape and process content from external sources.
  
- **Frontend Interface**
  - Responsive design built with Next.js and Tailwind CSS.
  - User-friendly dashboards and navigation.
  
- **API Documentation**
  - Interactive API docs generated with Swagger (drf_yasg).

## Technology Stack

- **Frontend**
  - [Next.js](https://nextjs.org/) - React framework for server-rendered applications.
  - [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework.
  - [TypeScript](https://www.typescriptlang.org/) - Typed superset of JavaScript.
  - [Axios](https://axios-http.com/) - Promise-based HTTP client.
  
- **Backend**
  - [Django](https://www.djangoproject.com/) - High-level Python web framework.
  - [Django REST Framework](https://www.django-rest-framework.org/) - Toolkit for building Web APIs.
  - [Celery](https://celeryproject.org/) - Asynchronous task queue.
  - [Redis](https://redis.io/) - In-memory data structure store for caching and message brokering.
  - [OpenAI API](https://openai.com/api/) - AI-powered content generation.
  
- **Database**
  - [PostgreSQL](https://www.postgresql.org/) - Powerful, open-source object-relational database system.
  
- **Other Tools**
  - [CKEditor](https://ckeditor.com/) - Rich text editor.
  - [Swagger](https://swagger.io/) - API documentation tool.

## Installation

### Prerequisites

- **Node.js** (v14 or later)
- **Python** (v3.8 or later)
- **PostgreSQL**
- **Redis**
- **Git**

### Clone the Repository
```bash
git clone https://github.com/yourusername/spicacms.git
cd spicacms
```


### Backend Setup

1. **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**

    Create a `.env` file in the `backend` directory with the following variables:

    ```env
    SECRET_KEY=your-secret-key
    DEBUG=1
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

    DATABASE_NAME=spica_db
    DATABASE_USER=spica_user
    DATABASE_PASSWORD=spica_pass
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

    OPENAI_API_KEY=your-openai-api-key
    ```

5. **Apply Migrations and Create Superuser:**

    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

6. **Run Celery Worker:**

    In a new terminal window/tab, activate the virtual environment and run:

    ```bash
    celery -A api_gateway worker --loglevel=info
    ```

7. **Start the Backend Server:**

    ```bash
    python manage.py runserver
    ```

### Frontend Setup

1. **Navigate to the frontend directory:**

    ```bash
    cd ../frontend
    ```

2. **Install dependencies:**

    ```bash
    npm install
    # or
    yarn install
    ```

3. **Configure Environment Variables:**

    Create a `.env.local` file in the `frontend` directory with the following variables:

    ```env
    NEXT_PUBLIC_API_BASE_URL=http://localhost:8004/api
    ```

4. **Run the Frontend Server:**

    ```bash
    npm run dev
    # or
    yarn dev
    ```

## Configuration

- **JWT Authentication:**
  - Access and refresh tokens are managed via the `rest_framework_simplejwt` package.
  - Token lifetimes can be adjusted in `backend/api_gateway/settings.py` under `SIMPLE_JWT`.

- **CORS Settings:**
  - Configured in `backend/api_gateway/settings.py` to allow requests from `http://localhost:3000`.

- **Celery Configuration:**
  - Broker and backend set to Redis (`redis://localhost:6379/0`).
  - Ensure Redis is running before starting Celery.

- **AI Content Generation:**
  - OpenAI API key must be set in the `.env` file.
  - Define AI prompts in the Automation Templates via the Django admin interface.

## Usage

1. **Access the Admin Interface:**

    Navigate to `http://localhost:8000/admin/` and log in with your superuser credentials.

2. **Manage Users & Permissions:**

    - Create user accounts and assign them to predefined groups: Administrators, Moderators, Authors, and Users.
    - Each group has specific permissions as defined in the `create_groups` management command.

3. **Create Content:**

    - Add News, Articles, and Pages through the admin interface.
    - Assign categories, tags, and attach media files as needed.

4. **Automate Content Processing:**

    - Define Automation Templates to scrape and process content from external sources.
    - Schedule tasks using CRON expressions to run automation at specified intervals.

5. **Interact with the Frontend:**

    - Visit `http://localhost:3000/` to view the frontend interface.
    - Navigate through News, Articles, and other sections as per your permissions.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**

2. **Create a Feature Branch:**

    ```bash
    git checkout -b feature/YourFeature
    ```

3. **Commit Your Changes:**

    ```bash
    git commit -m "Add some feature"
    ```

4. **Push to the Branch:**

    ```bash
    git push origin feature/YourFeature
    ```

5. **Open a Pull Request**

Please ensure your code adheres to the project's coding standards and includes relevant tests.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please contact [dev@spicanet.net](mailto:your.email@example.com).