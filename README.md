## Training the model

- To train the model, run the command: `cd inference && docker run  -v $(pwd):/app rasa/rasa:1.10.8-full train --domain domain.yml --data data --out models`

- Migrate database tables `docker-compose exec api_server python manage.py create_db`

- Add an admin user `docker-compose exec api_server python manage.py seed`
 It will create an admin user with `username=admin@test.com` and `password=123456`
