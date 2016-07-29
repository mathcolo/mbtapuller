# mbtapuller


## Goals
- Provide a user-facing real-time train tracker
- Collect real-time subway data for extended analysis
- Learn about data analytics and storage

## Requirements
- Python 2.7
- requests
- flask
- sqlalchemy
- geopy
- pytz
- vcrpy
- mysql-python

## Installation

Clone the repository:

- `git clone https://github.com/nettube/mbtapuller.git && cd mbtapuller`

- Put your MBTA API key in `secrets.py`

For an automatic setup using Docker:

- `docker-compose up`

For a manual setup:

- Optionally customize `Database.py` with MySQL details (SQLite is assumed otherwise)

- `pip install requests flask sqlalchemy geopy vcrpy pytz mysql-python`

- `python initial_setup.py` (auto-creates mbta.db in the same directory)

- `python app.py` (or `USE_MYSQL=1 python app.py` for MySQL)
