FROM python:3.12-slim
WORKDIR /app
RUN pip install pandas
COPY data/ ./data/
COPY data/raw_data ./data/raw_data
COPY DataSetCleaner.py /app/
COPY app.py .
ENTRYPOINT [ "python", "app.py" ]