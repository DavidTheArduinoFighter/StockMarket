FROM node:20.9.0-slim as api_server
WORKDIR /app
COPY . /app
RUN npm install
EXPOSE 4000
CMD ["node", "server.js"]

# FROM node:20.9.0-slim as api_server
# WORKDIR /app/json
# COPY ./node /app
# RUN npm install
# EXPOSE 4000
# USER node
# CMD ["node", "server.js"]