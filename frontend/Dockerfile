FROM --platform=amd64 node:21 as builder

WORKDIR /app

COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM --platform=amd64 node:21-alpine
LABEL org.opencontainers.image.source=https://github.com/helsingborg-stad/F-AI
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