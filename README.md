Django rest framework Download Expert
This module shows a simple way to serve files for download in django rest framework using Apache module Xsendfile.

It also has an additional feature of serving downloads only to users belonging to a particular group. This feature might be useful for developers trying to give certain features to a group of users only.For example, a site where users belong to either a 'Premium' or 'Free' group. Apache modules like mod_ratelimit can be installed to limit download speed for users belonging to 'Free' group.

Prerequisite: A server installed with an O.S(preferably a linux environment)

TL;DR
Installation
Go to your terminal and run the following commands:
sudo apt install python3-venv
sudo apt install apache2 libapache2-mod-wsgi-py3
Create a directory where you wish to keep your project and move into the directory:
mkdir ~/myproject
cd ~/myproject
git clone https://github.com/nishant-boro/django-rest-framework-download-expert.git .
Within the myproject directory, create a Python virtual environment by typing:
python3 -m venv venv
This will create a directory called venv within your myproject directory. Inside, it will install a local version of Python and a local version of pip. We can use this to install and configure an isolated Python environment for our project.

Activate the virtual environment:
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Configuring Apache:
mkdir ~/myproject/static
sudo nano /etc/apache2/sites-available/000-default.conf
Add the following lines:

<VirtualHost *:80>
    . . .

    Alias /static /home/user/myproject/static
    <Directory /home/user/myproject/static>
        Require all granted
    </Directory>

    <Directory /home/user/myproject/api>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess myproject python-home=/home/user/myproject/venv python-path=/home/user/myproject
    WSGIProcessGroup myproject
    WSGIScriptAlias / /home/user/myproject/api/wsgi.py

</VirtualHost>
Modify settings.py:
mkdir ~/myproject/myfiles
nano myproject/settings.py
Add your secret Key and then find the ALLOWED_HOSTS line. Inside the square brackets, enter your server's public IP address, domain name or both. Each value should be wrapped in quotes and separated by a comma like a normal Python list:

SECRET_KEY = '' // Add your secret key here
ALLOWED_HOSTS = ["server_domain_name or IP"]
Also add the following lines at the end of the file:

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
Next, include the path to your directory containing the file(s) which needs to be served for download:

SERVE_FILES_FROM = '/home/user/myproject/myfiles' // just an example path
Migrate database:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
Setting permissions:
chmod 664 ~/myproject/db.sqlite3
sudo chown www-data:www-data ~/myproject/db.sqlite3
sudo chown www-data:www-data ~/myproject
sudo ufw allow 'Apache Full'
sudo systemctl restart apache2
Open the apache2.conf file:
sudo nano /etc/apache2/apache2.conf
Add the following line at the end of the file:

WSGIPassAuthorization On
Testing the application:
Copy the file(s) you wanna serve for download to the directory myfiles. Next, go to django admin('www.yoursite.com/admin') and add two new groups named 'Premium' and 'Free'. Also create some users and add them to either of the groups 'Premium' or 'Free'. Now each user belongs to either of the group.

Before we test our application, we must configure our authorization plugin. I have used Django rest-framework Social Oauth2 for testing this application. Head over to their github repo(https://github.com/RealmTeam/django-rest-framework-social-oauth2), complete the installation section, and come back here with the client id and client secret keys.

Next, we use CURL/Postman to test our application:

Let's get the token for one of the users we created in django admin:
   curl -X POST -d "client_id=<client_id>&client_secret=<client_secret>&grant_type=password&username=<user_name>&password=<password>" http://yoursite.com/auth/token

2) Grab the access token and send a GET request to your site in the following format:

http://yoursite.com/downloads/p/?name=<file-name>&type=<file-type> // if the user belongs to premium group
http://yoursite.com/downloads/f/?name=<file-name>&type=<file-type> // if the user belongs to free group
Attach an authorization header: Key: Authorization, Value: Bearer <token-value>

Here's how I did this in postman:

postman.gif

in case of problem when certboting the conf file with daemon duplicate name solution here: https://stackoverflow.com/questions/39317200/name-duplicates-previous-wsgi-daemon-definition
