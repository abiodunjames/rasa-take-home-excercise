FROM python:3.7
WORKDIR /app

# install requirements
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Add source code
ADD . /app


# setup database
RUN python manage.py db init
RUN python manage.py db migrate --message "initial database migration"

EXPOSE 5000

CMD ["python","manage.py", "run"]
