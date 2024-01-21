ARG target_host

FROM node:21-alpine3.18 as build_frontend

WORKDIR /app
ENV VITE_API_HOST $target_host

COPY ./frontend .
RUN npm install && npm run build

FROM python:3.11.7-alpine3.19
EXPOSE 80/tcp

WORKDIR /app

COPY ./insurance ./insurance
COPY --from=build_frontend /app/dist ./insurance/static
COPY ./requirements.txt .
COPY ./data/database.db .

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "insurance.main:app", "--workers", "4", "--worker-class", "insurance.workers.CstmUvicornWorker", "--bind","0.0.0.0:80"]




