FROM python:3

RUN pip3 install django daphne channels pillow numpy tensorflow pymongo django-cors-headers channels_redis

COPY . .

RUN python manage.py migrate

CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "fyp_backend.asgi:application"]
