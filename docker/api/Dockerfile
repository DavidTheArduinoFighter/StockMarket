FROM node:20.9.0-slim as api_server
WORKDIR /app
COPY . /app
RUN npm install
EXPOSE 4000
CMD node server.js