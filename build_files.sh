# build_files.sh
pip install -r requirements.txt
python3.11 manage.py collectstatic
#here you must be give python3.9