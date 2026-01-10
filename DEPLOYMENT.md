# Metro Project - Deployment Guide

## Issues Fixed

1. **Dockerfile**: 
   - Added entrypoint.sh execution
   - Fixed WORKDIR and COPY paths
   - Added postgresql-client for database checks

2. **docker-compose.yml**:
   - Removed volume mount that was overwriting app files
   - Added static files volume
   - Added restart policies
   - Added DATABASE_URL environment variable

3. **settings.py**:
   - Switched from SQLite to PostgreSQL
   - Added environment variable support
   - Fixed ALLOWED_HOSTS for production
   - Added STATIC_ROOT configuration

4. **nginx.conf**:
   - Completed missing configuration
   - Added upstream configuration
   - Added static files location
   - Added proper MIME types

5. **entrypoint.sh**:
   - Added proper database health check
   - Reordered migration commands

## Deployment Steps

### 1. First, ensure you can SSH into your server

Run this command to add your SSH key via DigitalOcean console:
```bash
# Access your droplet via DigitalOcean web console, then run:
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIC2u7J1EjfSZ0wrEfvejLjAz830KhzKG/hoyra84p2Oi hardik@Hardiks-MacBook-Air.local" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 2. Install Docker on your server

```bash
# SSH into your server
ssh -i ~/.ssh/id_ed25519 root@64.227.154.16

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

### 3. Deploy your application

```bash
# On your local machine, push code to GitHub
git add .
git commit -m "Fixed Docker configuration"
git push origin main

# On your server, clone the repository
cd /opt
git clone https://github.com/HardikChhabra14/Metro-Project.git
cd Metro-Project

# Create .env file
nano .env
# Copy contents from your local .env file

# Make entrypoint executable
chmod +x entrypoint.sh

# Build and start containers
docker-compose up -d --build

# Check if containers are running
docker-compose ps

# View logs
docker-compose logs -f web
```

### 4. Create Django superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Configure DNS

Point your domain `metrohardik.me` to your server IP `64.227.154.16`:
- A record: metrohardik.me -> 64.227.154.16
- A record: www.metrohardik.me -> 64.227.154.16

### 6. (Optional) Setup SSL with Let's Encrypt

```bash
# Install certbot
apt install certbot python3-certbot-nginx -y

# Stop nginx container temporarily
docker-compose stop nginx

# Get SSL certificate
certbot certonly --standalone -d metrohardik.me -d www.metrohardik.me

# Update nginx config to use SSL (manual step)
# Then restart
docker-compose up -d nginx
```

## Useful Commands

```bash
# View logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx

# Restart services
docker-compose restart web
docker-compose restart nginx

# Stop all services
docker-compose down

# Start services
docker-compose up -d

# Rebuild after code changes
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Access Django shell
docker-compose exec web python manage.py shell

# Access database
docker-compose exec db psql -U metrouser -d metrodb
```

## Security Notes

1. Change `POSTGRES_PASSWORD` in docker-compose.yml and .env
2. Change `SECRET_KEY` in .env
3. Set `DEBUG=False` in production
4. Never commit .env file to GitHub
5. Consider using environment variables in GitHub Secrets for CI/CD

## Troubleshooting

### Cannot connect to database
```bash
docker-compose logs db
docker-compose exec web python manage.py migrate
```

### Static files not loading
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

### Permission issues
```bash
docker-compose exec web ls -la /app
chmod +x entrypoint.sh
```

### Container keeps restarting
```bash
docker-compose logs web
docker-compose exec web python manage.py check
```
