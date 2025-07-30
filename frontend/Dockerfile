FROM node:22-alpine
WORKDIR /app
COPY config/ .
RUN npm install
COPY web/ web/
CMD ["npm", "run", "dev", "--", "--host"]