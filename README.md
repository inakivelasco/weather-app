# weather-app

## Some usefull commands
- **Run web →** `flask --app .\web\app.py run`
- **Test database →** `docker run -p 3306:3306 --name db-mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=weather_db mysql:lts`
- **Generate requirements.txt →** `pip freeze > web/requirements.txt`
- **Build and run full app →** `docker compose up --build`