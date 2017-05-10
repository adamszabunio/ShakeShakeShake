# chmod a+x bootstrap.sh

sudo apt-get -y update
sudo apt install -y python3-pip # need apache2???
# sudo apt-get -y install python3-tk
# sudo python3 -m pip install --upgrade pip
# sudo python3 -m pip install sqlalchemy psycopg2
sudo python3 -m pip install pip boto pandas Flask sqlalchemy psycopg2 matplotlib -U
