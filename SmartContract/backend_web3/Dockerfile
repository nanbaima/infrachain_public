FROM public.ecr.aws/docker/library/node:latest
WORKDIR /usr/app
COPY package.json .
RUN npm install --quiet
COPY . .