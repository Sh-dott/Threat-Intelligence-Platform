# Deploy to Vercel - Complete Guide

This guide will help you deploy both frontend and backend to Vercel from your GitHub repository.

## Prerequisites

- GitHub account with repository: https://github.com/Sh-dott/Threat-Intelligence-Platform
- Vercel account: https://vercel.com/shais-projects-3167cc9a

---

## Step 1: Deploy Frontend to Vercel

1. **Go to your Vercel Dashboard:**
   https://vercel.com/shais-projects-3167cc9a

2. **Click "Add New..." → "Project"**

3. **Import Git Repository:**
   - Select your GitHub repository: `Threat-Intelligence-Platform`
   - Click "Import"

4. **Configure Project:**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

5. **Environment Variables:**
   - Click "Add Environment Variable"
   - Name: `VITE_API_URL`
   - Value: `https://threat-intel-api.vercel.app` (we'll create this in Step 2)
   - Click "Add"

6. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your frontend will be live at: `https://threat-intelligence-platform.vercel.app`

---

## Step 2: Deploy Backend to Vercel

1. **Go back to Vercel Dashboard:**
   https://vercel.com/shais-projects-3167cc9a

2. **Click "Add New..." → "Project"**

3. **Import Same Repository Again:**
   - Select: `Threat-Intelligence-Platform`
   - Click "Import"

4. **Configure Project:**
   - **Project Name**: `threat-intel-api`
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

5. **Deploy:**
   - Click "Deploy"
   - Wait 3-5 minutes
   - Your backend will be live at: `https://threat-intel-api.vercel.app`

---

## Step 3: Update Frontend Environment Variable

1. **Go to your Frontend project in Vercel**
2. **Click "Settings" → "Environment Variables"**
3. **Edit `VITE_API_URL`:**
   - New Value: `https://threat-intel-api.vercel.app` (your actual backend URL)
4. **Redeploy Frontend:**
   - Go to "Deployments" tab
   - Click the three dots on the latest deployment
   - Click "Redeploy"

---

## Step 4: Test Your Deployment

1. **Test Backend:**
   Open: `https://threat-intel-api.vercel.app/`

   You should see:
   ```json
   {
     "name": "Threat Intelligence Platform API",
     "version": "1.0.0",
     "status": "operational"
   }
   ```

2. **Test Frontend:**
   Open: `https://threat-intelligence-platform.vercel.app/`

   You should see your Threat Intelligence Platform with articles loading!

---

## 🎉 Your URLs

**Frontend:** `https://threat-intelligence-platform.vercel.app/`
**Backend API:** `https://threat-intel-api.vercel.app/`
**API Docs:** `https://threat-intel-api.vercel.app/docs`

---

## Automatic Deployments

Both projects are now connected to your GitHub repository!

- **Every push to master** → Vercel automatically redeploys
- **Pull requests** → Vercel creates preview deployments

---

## Troubleshooting

### Backend Returns 404
- Check that Root Directory is set to `backend`
- Verify vercel.json exists in backend folder
- Check deployment logs

### Frontend Can't Connect to Backend
- Verify `VITE_API_URL` environment variable is correct
- Check browser console for CORS errors
- Ensure backend is deployed and accessible

### CORS Errors
- Backend CORS is already configured for Vercel domains
- Make sure you're using HTTPS (not HTTP)

---

## Custom Domain (Optional)

1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Follow Vercel's DNS configuration instructions

---

## Monitoring

- **View Logs**: Click on any deployment → "View Function Logs"
- **Analytics**: Available in project dashboard
- **Performance**: Vercel provides built-in performance metrics

---

## Cost

- **Hobby Plan**: FREE
  - Unlimited deployments
  - Automatic HTTPS
  - Global CDN
  - Serverless functions

- **Pro Plan**: $20/month (if you need more)
  - Better performance
  - More bandwidth
  - Team features

---

## Alternative: Deploy via Vercel CLI

If you prefer command line:

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy Frontend
cd frontend
vercel --prod

# Deploy Backend
cd ../backend
vercel --prod
```

---

**Your Threat Intelligence Platform is now live on Vercel!** 🚀
