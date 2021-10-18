# report-text-extraction

## API Documentation

- Swagger -> [http://localhost:5000/docs](http://localhost:5000/docs)

## Kick Start

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

# install pycld2 0.42
pipenv install https://github.com/aboSamoor/pycld2/zipball/e3ac86ed4d4902e912691c1531d0c5645382a726

# configure server
set flask_env=development
set flask_app=app.py

# run api server
flask run
```
