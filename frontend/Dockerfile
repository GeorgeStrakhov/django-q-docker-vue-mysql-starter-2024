# Stage 1: Build the Vue.js application and prep for running
FROM node:latest as build-stage

WORKDIR /app

COPY ./app/package*.json /app
COPY ./app/yarn*.lock /app

RUN npm install yarn

RUN yarn

COPY ./app /app

# declare and expose vars
ARG VITE_PROJECT_NAME
ENV VITE_PROJECT_NAME==${VITE_PROJECT_NAME}
ARG VITE_CONTACT_EMAIL
ENV VITE_CONTACT_EMAIL==${VITE_CONTACT_EMAIL}
ARG VITE_ACCOUNTS_EMAIL
ENV VITE_ACCOUNTS_EMAIL==${VITE_ACCOUNTS_EMAIL}

RUN yarn build

EXPOSE 5173

CMD ["yarn", "dev"]

# Stage 2: On production: Serve the app using Nginx
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
