FROM node:current-alpine
WORKDIR /app

ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

COPY package*.json ./
RUN npm install --omit=dev
COPY . .

RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
