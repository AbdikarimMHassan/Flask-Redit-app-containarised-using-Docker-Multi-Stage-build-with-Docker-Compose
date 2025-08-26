# 🚀 Flask + Redis with Docker Compose, Multi-Stage Builds, Nginx & AWS ECR

This project containerises a small **Flask + Redis** app, using **Docker best practices** to demonstrate real-world DevOps workflows. The app itself tracks visits and pins markers on a map, but the focus here is on how it’s packaged, deployed, and scaled.  

---

## 🔑 DevOps Highlights

### 🐳 Service Orchestration with Docker Compose
- **Multiple services defined**: Flask app, Redis, and Nginx reverse proxy.  
- **Automatic networking**: services discover each other by name (e.g. `REDIS_HOST=redis`).  
- **Single command spin-up**: `docker compose up` starts the full stack, no manual linking required.  



### ⚡ Multi-Stage Build with Wheels
- **Build stage**: pre-downloads Python dependencies (`flask`, `redis`) into wheels.  
- **Prod stage**: installs only those wheels, leaving behind no caches or build tools.  
- **Benefits**:  
  - **Smaller image size** → quicker deployments and container startup.  
  - **Faster builds** → reuses prebuilt wheels.  
  - **Clean separation** → dependencies built once, reused in multiple environments.  

---

### ☁️ AWS ECR Integration
- Built the final Docker image locally and **pushed to a private Amazon ECR repository**.  
- `docker-compose.yml` can be switched to **pull the image directly from ECR**, ensuring production parity.  
- **IAM authentication required** → only authorised users/services can pull images.  
- **Cloud-ready workflow** → same image runs locally and in AWS ECS/EKS.  

```

### 🌐 Nginx Reverse Proxy & Local Load Balancing
- Nginx sits in front of Flask containers, proxying traffic on port `5002`.  
- Useful for **local development** to simulate load balancing (`docker compose up --scale web=3`).  
- In production, this role is typically replaced by **AWS Application Load Balancer (ALB)** for auto-scaling and managed TLS.  

---

## 📂 Project Structure
---
├── count.py # Flask app (visit tracker + Redis backend)
├── templates/ # Jinja2 templates
├── static/ # CSS/JS assets
├── Dockerfile # Multi-stage build (build + prod)
├── docker-compose.yml # Orchestrates Flask, Redis, Nginx
├── nginx.conf # Reverse proxy config
└── README.md
## ⚙️ Running the Stack

### Local Build + Run
```bash
docker compose up -d --build


Resetting the Counter (Optional)

If ENABLE_RESET=true is set in the environment, visit:





