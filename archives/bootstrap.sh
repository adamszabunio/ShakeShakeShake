# chmod a+x bootstrap.sh
sudo apt-get -y update
sudo apt install -y python3-pip
sudo python3 -m pip install pip boto pandas Flask sqlalchemy psycopg2 matplotlib -U
# echo export AIRFLOW_HOME=/vagrant/airflow >> /home/ubuntu/.bashrc
# export AIRFLOW_HOME=/vagrant/airflow
# python3 -m pip install airflow
# rm /usr/local/lib/python3.5/dist-packages/airflow/example_dags/example_twitter_dag.py
# airflow initdb
# airflow scheduler -D
# airflow webserver -p 8000 -D
