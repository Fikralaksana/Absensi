## Requirements
1. Python 3.10.6
2. pip 22.2.2
3. virtualenv `python -m pip install virtualenv`
4. 
## Install
1. `git clone https://github.com/Fikralaksana/Absensi.git`
2. `cd Absensi`
3. `python -m virtualenv env`
4. `source env/bin/activate`
5. `pip install -r requirements.txt`
6. `alembic revision --autogenerate -m "init"`
7. `alembic upgrade head`

## Debug
1. `flask --app absensi --debug run`
