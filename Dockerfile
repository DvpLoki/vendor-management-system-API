FROM  python:3.12.3-alpine3.19
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip  install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]