FROM node:18

WORKDIR /app

# 依存を先にコピーしてキャッシュ活用
COPY package.json package-lock.json ./
RUN npm install
RUN npm install -g next

# アプリコードをコピー
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
