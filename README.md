## Weather data API

#### To run:

- Clone repo
- Alter `app/.env` variable `TARGET_SITE` to your desired site
- `docker compose up -d --build` to start web app and database
- `docker exec -it weather-scraper-web-1 bash` to attach shell to web container
- In web container run `flask shell`
- In flask shell run `init_database()`
- If needed, run `start_schedule()` to fetch new data every 30 minutes, though this is intensive on the target website
	- Run `stop_schedule()` to stop
- Visit or request data from the `/weather` URL to get weather data

Note this is intended as a demo/ learning project, as such the intended domain to scrap is not provided.