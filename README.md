# report-text-extraction

## API Documentation

- Swagger -> [http://localhost:5000/docs](http://localhost:5000/docs)

## Kick-Start without Docker

- Install python (3.9.x) -> [https://www.python.org/downloads/](https://www.python.org/downloads/)

```powershell
# install pipenv
pip3 install --user pipenv

# navigate to project dir
cd report-text-extraction

# install dependencies
pipenv install --ignore-pipfile

# activate Pipenv shell
pipenv shell

# configure server
set flask_env=development
set flask_app=app.py

# run api server
flask run
```
Open your browser with this URL: [http://localhost:5000/docs](http://localhost:5000/docs)

## Running application with Docker

To run the application with Docker, install the [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on your development machine.

#### Development build

```powershell
# Run the application in dev mode in Docker
# Use --build option to rebuild the container after any changes on environment (ie. installing modules)
docker-compose up [--build]
```

Open your browser with this URL: [http://localhost:5000/docs](http://localhost:5000/docs)

#### Production build

```powershell
# Run the application in production mode in Docker
docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up --build
```
#### Tag and push your production build into Docker registry


```powershell
# We currently build the image with 'latest' as <VERSION> tag 
docker tag bizres-text-extractor:prod <REGISTRY_URL>/bizres-text-extractor:<VERSION>

# Push the image to registry
docker push <REGISTRY_URL>/bizres-text-extractor:latest
```