# Step-by-Step Deployment Guide — IrisAI

This guide provides complete step-by-step instructions to deploy the **IrisAI — Iris Flower Classification** full-stack application to production.

- **Backend (FastAPI REST API)**: Deployed to [Render](https://render.com) or [Railway](https://railway.app).
- **Frontend (React + Vite Dashboard)**: Deployed to [Vercel](https://vercel.com) or [Netlify](https://netlify.com).
- **GitHub Repository**: `https://github.com/ayanmca2026/iris-flower-classification`

---

## PART 1: Deploying the FastAPI Backend to Render

### Step 1: Create a Render Account & Connect GitHub
1. Go to [https://dashboard.render.com/](https://dashboard.render.com/) and log in (or sign up using GitHub).
2. Click the **"New +"** button in the top right and select **"Web Service"**.
3. Select **"Build and deploy from a Git repository"** and click **Next**.
4. Connect your GitHub account and search for the repository: `ayanmca2026/iris-flower-classification`. Click **Connect**.

### Step 2: Configure Web Service Settings
Fill in the deployment configuration fields:

| Configuration Field | Value to Enter |
| :--- | :--- |
| **Name** | `irisai-backend` (or your preferred name) |
| **Language** | `Python 3` |
| **Branch** | `main` |
| **Root Directory** | `backend` *(CRITICAL: Type `backend` here)* |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | **Free** |

### Step 3: Add Environment Variables on Render
Scroll down to the **"Environment Variables"** section and click **"Add Environment Variable"**:

- **Key**: `FRONTEND_URL`
- **Value**: `https://your-app-name.vercel.app` *(You can update this after deploying the frontend on Vercel)*

### Step 4: Deploy Backend
Click **"Create Web Service"**.
Render will build and start your FastAPI service. Once completed, Render will issue your backend URL:
`https://irisai-backend.onrender.com`

#### Verify Backend Deployment:
Open in your browser:
- `https://irisai-backend.onrender.com/health` → Should return `{"status": "healthy", ...}`
- `https://irisai-backend.onrender.com/docs` → Interactive Swagger API documentation.

---

## PART 2: Deploying the React Frontend to Vercel

### Step 1: Log in to Vercel
1. Go to [https://vercel.com/dashboard](https://vercel.com/dashboard) and log in with your GitHub account.
2. Click **"Add New..."** → **"Project"**.

### Step 2: Import GitHub Repository
1. Find `ayanmca2026/iris-flower-classification` in your repository list and click **"Import"**.

### Step 3: Configure Project Settings
In the project configuration panel:

1. **Framework Preset**: Select **Vite**.
2. **Root Directory**: Click **"Edit"** next to Root Directory and select `frontend`.
3. **Build Command**: `npm run build` *(Auto-filled)*
4. **Output Directory**: `dist` *(Auto-filled)*

### Step 4: Add Environment Variables on Vercel
Expand the **"Environment Variables"** section:

- **Key**: `VITE_API_URL`
- **Value**: `https://irisai-backend.onrender.com` *(Use your actual Render backend URL from Part 1)*

### Step 5: Deploy Frontend
Click **"Deploy"**.
Vercel will install npm dependencies and compile your React Vite production build. Within ~30 seconds, Vercel will grant your live URL:
`https://iris-flower-classification.vercel.app`

---

## PART 3: Connect & Test Full-Stack Integration

1. Copy your Vercel frontend URL (e.g. `https://iris-flower-classification.vercel.app`).
2. Go back to Render Dashboard → `irisai-backend` → **Environment Variables**.
3. Update `FRONTEND_URL` to `https://iris-flower-classification.vercel.app` and click **Save Changes**. (Render will automatically redeploy the backend with updated CORS headers).
4. Open `https://iris-flower-classification.vercel.app` in your web browser.
5. Enter sample flower measurements (e.g., Sepal Length: `5.1`, Sepal Width: `3.5`, Petal Length: `1.4`, Petal Width: `0.2`) and click **"Predict Species"**.
6. Verify live species prediction, confidence percentage, and probability progress bars!

---

## Alternative: Deploy Backend to Railway

If you prefer **Railway** instead of Render:

1. Go to [https://railway.app/](https://railway.app/) and create a new project from your GitHub repo `iris-flower-classification`.
2. Set Root Directory to `backend`.
3. Railway automatically detects `requirements.txt` and uses:
   `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set Environment Variable `FRONTEND_URL` = `https://your-vercel-domain.vercel.app`.
5. Copy the generated Railway domain and set `VITE_API_URL` on Vercel.
