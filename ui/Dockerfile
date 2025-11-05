FROM node:24-alpine

WORKDIR /ui

COPY package.json package-lock.json ./

RUN npm install

# RUN npm i -g serve

COPY . .

# RUN npm run build

EXPOSE 5173

# CMD [ "serve", "-s", "dist" ]

CMD ["npm", "run", "dev"]