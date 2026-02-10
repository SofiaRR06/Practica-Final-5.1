FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]