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

Here is a roadmap of potential improvements, categorized into Polished UX/UI Enhancements and Next-Level Feature Integrations.
Tier 1: Polished UX/UI Enhancements (High Impact, Low Effort)
These are small changes that make a huge difference in how professional and "premium" your portfolio feels.

1. Skeleton Loaders for a Faster Feel
   Instead of a generic spinner when the main page loads, implement skeleton loaders. These are greyed-out placeholders that mimic the shape of the content that's about to appear. It makes the site feel significantly faster and more modern.
   How: Create a <ProjectCardSkeleton /> component. When your ProjectList component is in its isLoading state, render an array of these skeletons instead of a single spinner. This gives the user a preview of the layout before the data arrives.
2. Staggered Animations for Lists
   Your FadeIn component is great. You can make it even better by applying a staggered delay when rendering lists of items (like projects or certifications). Instead of everything fading in at once, each card will appear one after another.
   How: In your .map() function for rendering project cards, pass the index to the FadeIn component's delay prop: <FadeIn delay={index \* 100}>. This will make the first card appear after 0ms, the second after 100ms, the third after 200ms, and so on, creating a beautiful cascading effect.
3. Refined Hover States and Transitions
   Add subtle but satisfying effects when a user interacts with clickable elements.
   How: On your project cards, add a group class in TailwindCSS. Then, on elements inside the card (like the title), add group-hover:text-purple-500. This allows you to change the color of the title when the user hovers anywhere on the card, not just on the text itself. Add transition-transform hover:scale-[1.02] to the cards to make them "lift" slightly on hover.
   Tier 2: Next-Level Feature Integrations (Showcasing Advanced Skills)
   These are bigger features that demonstrate your ability to build complex, end-to-end systems.
4. AI Assistant 2.0: Conversational Memory
   The biggest limitation of the current AI is that it's stateless—it forgets everything after each message. The next evolution is to give it a memory.
   The Concept: The AI will remember the last 2-3 exchanges and use that history as additional context for its next response. This allows for natural, follow-up conversations.
   How (Backend): Modify the career_chat view to accept an optional chat_history array in the POST request. Prepend this history to the context you feed the LLM.
   How (Frontend): In the ChatAssistant component, before making an API call, grab the last 4 messages from your messages state, format them simply (e.g., "User: ...\nAssistant: ..."), and send them along with the new question.
5. A "Live Status" Dashboard Page
   You have several real-time data sources (GitHub, Nostr, Bitcoin Mempool). Instead of just having them on the homepage, create a dedicated /dashboard page that presents this information in a beautiful, auto-refreshing interface.
   The Concept: A single page that acts as a "mission control" for your digital footprint.
   How:
   Create a new Route and Page component in React.
   Use a grid layout to display your GithubStats, GithubContributions, MempoolStats, and LatestNostrNote components.
   Set up timers (setInterval) in each component to re-fetch its data every 1-5 minutes, creating a truly "live" feel. This demonstrates your ability to handle asynchronous data fetching and state updates.
6. Backend Caching with Redis
   The warning in your logs (Accessing the database during app initialization is discouraged) is a good reminder about performance. While the superuser script is the main cause, you can significantly speed up your API by caching external requests.
   The Concept: Store the results of slow API calls (like to GitHub or Nostr) in a fast in-memory database like Redis. The first time a user requests your GitHub stats, you fetch them from GitHub. For the next hour, you fetch them instantly from your Redis cache.
   How:
   Add a free Redis instance from the Render Add-ons marketplace to your backend.
   Install django-redis in your requirements.txt.
   Configure Django's caching backend in settings.py to use the Redis URL provided by Render.
   Your existing caching logic (from django.core.cache import cache) will now automatically use this powerful new backend instead of the in-memory cache, making it persistent and much more effective. This is a huge professional skill to demonstrate.

Roadmap Recommendation
Start with the Tagging System. It's a foundational feature that improves your portfolio's structure and demonstrates core backend skills.

Then, implement Storing AI Embeddings. This is the single most impressive feature you can add. It builds on your existing AI work and elevates it to a professional, production-grade architecture.

Finally, add the "Likes" feature. This is a fun, user-facing feature that rounds out your skill set.
