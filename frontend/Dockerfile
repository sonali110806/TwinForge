FROM node:20-bookworm-slim

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN rm -rf node_modules package-lock.json && npm install

COPY frontend ./

EXPOSE 8080

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
