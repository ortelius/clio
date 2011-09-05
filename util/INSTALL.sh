apt-get update
sudo apt-get install -y binutils gdal-bin postgresql-8.4-postgis postgresql-server-dev-8.4 python-psycopg2 python-setuptools libgeoip1 gdal-bin python-gdal git mercurial
sudo easy_install virtualenv

git clone git://github.com/ortelius/clio.git
virtualenv clio
cd clio
source bin/activate
pip install -r clio/requirements.txt

sudo su - postgres
createuser -P clio_admin
createdb -O clio_admin clio
pg_restore -O -d clio /home/ubuntu/clio/data/clio.backup
for tbl in `psql -qAt -c "select tablename from pg_tables where schemaname = 'public';" clio` ; do  psql -c "alter table $tbl owner to clio_admin" clio ; done
for tbl in `psql -qAt -c "select sequence_name from information_schema.sequences where sequence_schema = 'public';" clio` ; do  psql -c "alter table $tbl owner to clio_admin" clio ; done
for tbl in `psql -qAt -c "select table_name from information_schema.views where table_schema = 'public';" clio` ; do  psql -c "alter table $tbl owner to clio_admin" clio ; done

sudo apt-get install apache2 libapache2-mod-wsgi

Configure Apache/WSGI
a2dissite a2ensite a2enmod etc
log Perms
createsuperuser
