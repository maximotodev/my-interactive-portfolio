# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

Category 2: Driving User Engagement & Analytics
These features show that you think like a product owner, not just a programmer. You care about user interaction and measuring success. 3. Add "Likes" or "Claps" to Projects
The Concept: Allow anonymous users to "like" or "applaud" a project. The total count is displayed on the project card.
Why It's a Great Feature: It's a simple, interactive feature that makes your portfolio feel more alive. It also requires you to solve a classic web problem: how to prevent a single user from liking a project a thousand times.
Implementation Plan:
Add a Counter Field: Add likes = models.IntegerField(default=0) to your Project model.
Create a "Like" Endpoint: In api/urls.py, add a path like path('projects/<int:pk>/like/', like_project_view).
Write the View: The view will get the project, increment its likes count using an F() expression for race-condition safety (project.likes = F('likes') + 1), and save it.
Rate Limiting: Use Django REST Framework's built-in throttling to limit likes from a single IP address (e.g., 5 likes per project per day).
Category 3: AI/ML Performance and Scalability
This is the most advanced tier and will firmly establish you as an AI Engineer who can build production-grade systems. 4. Store AI Embeddings in the Database with pgvector (The Ultimate Upgrade)
The Concept: Currently, your AI assistant and Skill Matcher generate embeddings for all your projects every single time a user asks a question. This is slow and inefficient. The professional solution is to pre-calculate these embeddings once and store them directly in the database.
Why It's a Great Feature: This is the industry standard for building scalable semantic search and RAG systems. It demonstrates that you understand how to build performant, production-ready AI applications, not just demos. Supabase and Neon both support the pgvector extension out of the box.
Implementation Plan:
Enable pgvector: In your Supabase dashboard, go to Database -> Extensions and enable vector.
Install Libraries: pip install pgvector django-pgvector.
Add a VectorField: In your Project and Post models:
code
Python
from pgvector.django import VectorField

class Project(models.Model): # ... other fields
embedding = VectorField(dimensions=384, blank=True, null=True) # 384 for all-MiniLM-L6-v2
Generate Embeddings on Save: Use a Django signal. When a Project is created or updated, call the Hugging Face API to get its embedding and save it to the new embedding field.
Refactor Your Search: Your AI's "retrieval" step is no longer a slow API call. It becomes a lightning-fast database query using nearest-neighbor search:
code
Python
from pgvector.django import L2Distance

query_embedding = get_embedding_for_user_question()

# Find the 5 most similar projects instantly

similar_projects = Project.objects.annotate(
distance=L2Distance('embedding', query_embedding)
).order_by('distance')[:5]
