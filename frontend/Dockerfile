FROM --platform=arm64 node:24 as builder

WORKDIR /app

COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:24-alpine
WORKDIR /app

# Only copy needed files
COPY package*.json ./
RUN npm install --omit=dev

COPY --from=builder /app/build ./build
COPY --from=builder /app/static ./static
COPY --from=builder /app/.svelte-kit ./svelte-kit
COPY --from=builder /app/svelte.config.js ./
COPY --from=builder /app/src ./src

# Expose default SvelteKit port
EXPOSE 3000

CMD ["node", "build"]