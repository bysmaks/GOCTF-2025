FROM node:20-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

RUN npm install --save-dev @types/express @types/multer @types/adm-zip

RUN npm run build

RUN mkdir -p /protected
RUN echo "goctf{n3xt_m1ddl3w4r3_byp4ss_4nd_syml1nk_fun}" > /protected/flag.txt
RUN chmod 644 /protected/flag.txt
RUN chmod 755 /protected

RUN mkdir -p /app/public/uploads
RUN chmod 777 /app/public/uploads

RUN mkdir -p /app/tmp/uploads
RUN chmod 777 /app/tmp/uploads

EXPOSE 3002

RUN apk add --no-cache coreutils

ENV NODE_OPTIONS="--enable-source-maps --no-warnings"

RUN apk add --no-cache coreutils unzip

CMD ["npm", "start"] 