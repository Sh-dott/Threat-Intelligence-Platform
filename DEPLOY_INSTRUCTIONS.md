# Deployment Instructions

## Frontend - GitHub Pages

The frontend is configured to automatically deploy to GitHub Pages when you push to the master branch.

### Setup Steps:

1. **Enable GitHub Pages in your repository:**
   - Go to: https://github.com/Sh-dott/Threat-Intelligence-Platform/settings/pages
   - Under "Build and deployment"
   - Source: **GitHub Actions**
   - Click Save

2. **Add API URL Secret:**
   - Go to: https://github.com/Sh-dott/Threat-Intelligence-Platform/settings/secrets/actions
   - Click "New repository secret"
   - Name: `API_URL`
   - Value: `https://your-app-name.herokuapp.com` (you'll get this after deploying backend)
   - Click "Add secret"

3. **Trigger Deployment:**
   - Push changes to master branch
   - Or go to Actions tab and manually trigger the workflow
   - Your site will be live at: **https://sh-dott.github.io/Threat-Intelligence-Platform/**

---

## Backend - Heroku

### Prerequisites:
- Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
- Login: `heroku login`

### Deployment Steps:

1. **Create Heroku App:**
   ```bash
   cd backend
   heroku create your-threat-intel-api
   ```

   Note: Replace `your-threat-intel-api` with your preferred app name.
   Heroku will give you a URL like: `https://your-threat-intel-api.herokuapp.com`

2. **Set Python Buildpack:**
   ```bash
   heroku buildpacks:set heroku/python
   ```

3. **Deploy to Heroku:**
   ```bash
   git subtree push --prefix backend heroku master
   ```

   Or if you prefer, create a separate git repo for the backend:
   ```bash
   cd backend
   git init
   git add .
   git commit -m "Initial backend commit"
   heroku git:remote -a your-threat-intel-api
   git push heroku master
   ```

4. **Verify Deployment:**
   ```bash
   heroku open
   ```

   Or visit: `https://your-threat-intel-api.herokuapp.com`

5. **View Logs:**
   ```bash
   heroku logs --tail
   ```

### Update GitHub Pages Secret:

Once your Heroku app is deployed, update the GitHub Actions secret:
- Go to: https://github.com/Sh-dott/Threat-Intelligence-Platform/settings/secrets/actions
- Edit `API_URL` secret
- Value: `https://your-threat-intel-api.herokuapp.com`
- Re-run the GitHub Actions workflow

---

## Testing the Deployment

1. **Backend:** https://your-threat-intel-api.herokuapp.com/health
2. **Frontend:** https://sh-dott.github.io/Threat-Intelligence-Platform/

---

## Troubleshooting

### Backend Issues:
```bash
heroku logs --tail
heroku ps
heroku restart
```

### Frontend Issues:
- Check GitHub Actions tab for build errors
- Ensure API_URL secret is set correctly
- Check browser console for CORS errors

---

## Updating Deployments

**Frontend:**
- Just push to master branch
- GitHub Actions will auto-deploy

**Backend:**
- Push changes to Heroku:
  ```bash
  git subtree push --prefix backend heroku master
  ```

---

## Cost

- **GitHub Pages:** Free
- **Heroku:** Free tier available (but may sleep after 30 min of inactivity)
  - Consider upgrading to Hobby tier ($7/month) for 24/7 uptime
  - Or use Render.com as free alternative

---

## Alternative: Deploy Backend to Render (Free)

If Heroku doesn't work or you want a free alternative:

1. Go to https://render.com
2. Sign up / Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - Name: `threat-intel-api`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Deploy
7. Update GitHub Actions `API_URL` secret with your Render URL

---

**Your Threat Intelligence Platform will be live!** 🚀
