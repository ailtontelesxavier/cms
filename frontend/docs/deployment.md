# Deploy

## Build

```bash
cd frontend
npm run build
```

Output goes to `frontend/dist/`. The build assumes:

- `VITE_API_BASE_URL=/api/v1` in production (relative proxy path)
- Serve `dist/` from any static server, with SPA fallback to `index.html`

## Environment Variables

| Variable | Dev | Production |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000/api/v1` | `/api/v1` |

## Docker

```dockerfile
FROM node:24-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

```nginx
# nginx.conf — SPA fallback + API proxy
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
    }
}
```
