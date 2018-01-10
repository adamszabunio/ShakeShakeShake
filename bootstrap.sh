# chmod a+x bootstrap.sh
sudo apt-get -y update
sudo apt install -y python3-pip
sudo python3 -m pip install pip boto pandas Flask sqlalchemy psycopg2 matplotlib -U
# miniconda
#apt-get update -q
su - ubuntu

echo installing miniconda
miniconda=Miniconda3-latest-Linux-x86_64.sh
cd /vagrant
if [[ ! -f $miniconda ]]; then
    wget --quiet http://repo.continuum.io/miniconda/$miniconda
fi
chmod +x $miniconda
./$miniconda -b -p /home/vagrant/miniconda

echo 'export PATH="/home/vagrant/miniconda/bin:$PATH"' >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc
chown -R ubuntu:ubuntu /home/vagrant/miniconda
/home/vagrant/miniconda/bin/conda install conda-build anaconda-client anaconda-build -y -q

# Geopandas
/home/vagrant/miniconda/bin/conda config --add channels conda-forge
/home/vagrant/miniconda/bin/conda install -y geopandas

# echo export AIRFLOW_HOME=/vagrant/airflow >> /home/ubuntu/.bashrc
# export AIRFLOW_HOME=/vagrant/airflow
# python3 -m pip install airflow
# rm /usr/local/lib/python3.5/dist-packages/airflow/example_dags/example_twitter_dag.py
# airflow initdb
# airflow scheduler -D
# airflow webserver -p 8000 -D
