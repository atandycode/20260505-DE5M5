FROM postgres
WORKDIR /app
RUN pip install psycopg2-binary
COPY app.py .
ENTRYPOINT [ "python", "app.py" ]