README.md Content
Generated markdown

# Interactive Developer Portfolio

Welcome to the repository for my personal interactive portfolio web application. This project is a full-stack showcase of my skills in modern web development, backend architecture, and AI/ML integration. It serves as a dynamic, live resume and a testament to my ability to build complex, feature-rich applications from the ground up.

**Live Frontend:** [`[maximotodev.vercel.app]`](https://[maximotodev.vercel.app])
**Live Backend API:** [`[https://my-portfolio-backend-z88p.onrender.com/api/`](https://[https://my-portfolio-backend-z88p.onrender.com/api/])

---

## 🌟 Key Features

This isn't just a static page; it's a fully interactive web application with a suite of modern features:

- **Dynamic Project & Certification Showcase:** All project and certification data is served from a PostgreSQL database via a RESTful API, managed through a secure Django admin panel.
- **AI-Powered Skill Matcher:** An intelligent search feature that allows visitors (like recruiters or clients) to paste a job description or list of keywords. A backend AI model then semantically filters and ranks my projects to highlight the most relevant ones.
- **Live Nostr Integration:** My portfolio pulls my latest profile information (username, bio, picture) and my most recent public note directly from the decentralized Nostr network, demonstrating my engagement with Web3 and decentralized social media.
- **Bitcoin Integration:** A "Tip Me" feature that generates a unique, persistent Bitcoin address via a backend wallet, allowing visitors to send an on-chain tip.
- **Live GitHub Stats:** The application fetches my latest GitHub stats (followers, stars, repo count) via the GitHub API, ensuring the data is always up-to-date.
- **Robust Backend & Database:** A powerful and secure backend built with Django, connected to a production-grade PostgreSQL database.

---

## 🛠️ Tech Stack & Architecture

This project is architected with a clean separation between the frontend and backend, a common practice for modern, scalable web applications.

### Backend (`/backend`)

- **Framework:** Django & Django Rest Framework
- **Language:** Python
- **Database:** PostgreSQL
- **AI/ML:** `sentence-transformers` for semantic search embeddings.
- **Bitcoin:** `bitcoinlib` for wallet creation and address generation.
- **Nostr:** `pynostr` for fetching profile data and notes from relays.
- **Deployment:** Deployed as a Web Service on **Render**.

### Frontend (`/frontend`)

- **Framework:** React (with Vite)
- **Language:** JavaScript (JSX)
- **Styling:** TailwindCSS for a utility-first, responsive design.
- **State Management:** React Hooks (`useState`, `useEffect`)
- **API Communication:** Axios
- **Deployment:** Deployed as a Static Site on **Vercel**.

### Architecture Diagram

Use code with caution.
Markdown
[ Vercel Frontend ] <--- (HTTPS API Calls) ---> [ Render Backend API (Django/Gunicorn) ]
| |
| v
+-------------------------------------------------> [ Render PostgreSQL Database ]
| |
| v
+-------------------------------------------------> [ External APIs: GitHub, Nostr ]
Generated code

---

## 🚀 Local Development Setup

To run this project on your local machine, follow these steps.

### Prerequisites

- Python 3.10+
- Node.js v18+
- PostgreSQL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/maximotodev/my-interactive-portfolio.git
cd my-interactive-portfolio
Use code with caution.
2. Backend Setup
Generated bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your local environment variables
# Create a .env file and copy the contents of .env.example
cp .env.example .env

# Edit the .env file with your local database URL, GitHub token, etc.
# NANO_EDITOR=nano nano .env

# Set up the PostgreSQL database and user
# (Ensure PostgreSQL is running)
# > createdb portfolio_db
# > createuser --interactive

# Run database migrations
python manage.py migrate

# Create a superuser to access the admin panel
python manage.py createsuperuser

# Run the backend server
python manage.py runserver
Use code with caution.
Bash
The backend API will be available at http://127.0.0.1:8000. You can log into the admin panel at http://127.0.0.1:8000/admin/ to add your projects and certifications.
3. Frontend Setup
Generated bash
# Open a new terminal window and navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Run the frontend development server
npm run dev
Use code with caution.
Bash
The frontend will be available at http://localhost:5173.
☁️ Deployment
This project is deployed across multiple platforms to leverage the best tools for each part of the stack:
The Django backend and PostgreSQL database are hosted on Render. The build.sh script handles production builds, migrations, and data loading from fixtures.
The React frontend is hosted on Vercel. It is configured to make API calls to the live Render backend URL via the VITE_API_BASE_URL environment variable.
Continuous deployment is enabled. Any push to the main branch will automatically trigger a new deployment on both Render and Vercel.
💡 Future Improvements
Re-enable the AI Skill Matcher on a hosting plan with more memory.
Implement a full test suite for both backend and frontend.
Add a "Contact Me" form that sends an email via an API.
Enhance the UI with more animations using Framer Motion.
Created by maximotodev.
```
