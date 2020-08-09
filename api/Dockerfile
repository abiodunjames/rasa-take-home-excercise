FROM python:3.7
ADD . /app
WORKDIR /app
# install requirements
RUN pip install -r requirements.txt

# setup database
RUN python manage.py db init
RUN python manage.py db migrate --message "initial database migration"

CMD python manage.py run
