# Crowdsolve - Deployment Guide to Render

## Pre-Deployment Checklist

### 1. **Update Environment Variables**
Before pushing to GitHub, ensure `.env` file is NOT committed. It's already in `.gitignore`.

Create a `.env` file locally (for local testing):
```
DEBUG=False
SECRET_KEY=your-very-secret-key-here-change-this
ALLOWED_HOSTS=crowdsolve-production.onrender.com,localhost
DATABASE_URL=postgresql://user:password@localhost/crowdsolve_db
EMAIL_HOST_USER=your-email@brevo.com
EMAIL_HOST_PASSWORD=your-brevo-password
DEFAULT_FROM_EMAIL=noreply@crowdsolve.com
CSRF_TRUSTED_ORIGINS=https://crowdsolve-production.onrender.com
```

### 2. **Generate a Strong SECRET_KEY**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 3. **Prepare GitHub Repository**
```bash
# Initialize git repo if not done
git init
git add .
git commit -m "Initial Crowdsolve deployment setup"
git remote add origin https://github.com/yourusername/crowdsolve.git
git push -u origin main
```

---

## Step-by-Step Render Deployment

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your GitHub account

### Step 2: Create PostgreSQL Database
1. Dashboard → New → PostgreSQL
2. **Name**: `crowdsolve-db`
3. **Region**: Choose closest to your users
4. **Database**: `crowdsolve_db`
5. **User**: `postgres`
6. Click "Create Database"
7. **Copy the Internal Database URL** (you'll need this)

### Step 3: Deploy Web Service
1. Dashboard → New → Web Service
2. **Select Repository**: Choose `crowdsolve` repo
3. **Settings**:
   - **Name**: `crowdsolve-production`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: Python 3.11
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn Crowdsolve.wsgi:application`

4. **Environment Variables** - Add all these:
   ```
   DEBUG = False
   SECRET_KEY = (paste your generated secret key)
   ALLOWED_HOSTS = crowdsolve-production.onrender.com
   DATABASE_URL = (paste from PostgreSQL database URL)
   EMAIL_HOST = smtp-relay.brevo.com
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = (your Brevo email)
   EMAIL_HOST_PASSWORD = (your Brevo password)
   DEFAULT_FROM_EMAIL = noreply@yourdomain.com
   CSRF_TRUSTED_ORIGINS = https://crowdsolve-production.onrender.com
   ```

5. Click "Create Web Service"
6. Wait 5-10 minutes for deployment to complete

---

## Step 4: Verify Deployment

1. Go to your service URL: `https://crowdsolve-production.onrender.com`
2. Check logs: Dashboard → Service → Logs
3. Create superuser:
   ```bash
   # In Render shell (if available)
   python manage.py createsuperuser
   ```
4. Access admin: `https://your-app.onrender.com/admin`

---

## Common Issues & Solutions

### Issue 1: Build Failed - "No module named 'X'"
**Solution**: Add package to `requirements.txt` and push again

### Issue 2: Database Connection Error
**Solution**: 
- Check DATABASE_URL is correct
- Ensure database is in same region
- Run migrations: `python manage.py migrate`

### Issue 3: Static Files Not Loading
**Solution**: WhiteNoise is configured. Run:
```bash
python manage.py collectstatic --no-input
```

### Issue 4: Email Not Sending
**Solution**:
- Verify Brevo credentials
- Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- Test with: `python manage.py shell` → `from django.core.mail import send_mail`

---

## Ongoing Maintenance

### Deploy New Changes
```bash
git add .
git commit -m "Your changes"
git push origin main
```
Render will auto-deploy on push!

### View Logs
- Dashboard → Your Service → Logs

### Database Backups
- Render auto-backs up PostgreSQL daily
- Download backups from DB dashboard

### Scale Up (if needed)
- Change from Free → Paid plan
- Dashboard → Service → Settings → Plan

---

## Useful Commands

**SSH into Render Shell** (temporarily):
```bash
# In Render dashboard, click "Shell" on your web service
python manage.py shell
```

**Run Management Commands**:
```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input
```

---

## Security Checklist

✅ Changed SECRET_KEY  
✅ Set DEBUG = False  
✅ Updated ALLOWED_HOSTS  
✅ Enabled HTTPS (automatic)  
✅ Configured CSRF_TRUSTED_ORIGINS  
✅ .env file in .gitignore  
✅ Email credentials in environment variables  

---

## Performance Tips

1. **Enable Caching**: Add Redis add-on for session caching
2. **CDN**: Configure Cloudflare for static files
3. **Database**: Optimize queries and add indexes
4. **Monitor**: Use Render's built-in monitoring

---

## Support

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.2/howto/deployment/
- **Troubleshooting**: Check logs in Render dashboard

