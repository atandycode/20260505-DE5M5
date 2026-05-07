FROM python:3.12-slim
WORKDIR /app
RUN pip install pandas
COPY data/ ./data/
COPY app.py .
COPY . .
ENTRYPOINT [ "python", "app.py" ]