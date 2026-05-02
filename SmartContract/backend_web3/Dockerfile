FROM public.ecr.aws/docker/library/node:20-bookworm-slim
WORKDIR /usr/app
COPY package.json package-lock.json ./
RUN npm ci --quiet
COPY . .
