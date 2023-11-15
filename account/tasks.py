from config.celery import app
from .utils import send_code


@app.task
def send_code_celery(email, activation_code):
    send_code(email, activation_code)

# python3 -m celery -A config worker -l info