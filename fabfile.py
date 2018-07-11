from fabric import Connection, Config

from instance.config import DATABASE

REMOTE_HOST = 'tele'
REMOTE_USER = ''
REMOTE_PASS = ''

database = DATABASE['database']
username = DATABASE['username']
password = DATABASE['password']

# sudo_pass = getpass.getpass("What's your sudo password?")
config = Config(overrides={'sudo': {'password': REMOTE_PASS}})
conn = Connection(host=REMOTE_HOST, config=config)

PROJECT_DIR = conn.run('pwd')

VENV_DIR = f'{PROJECT_DIR}/venv'

REPO_URL = 'https://github.com/FUNNYDMAN/teleplata.git'


def pull_repository():
    if conn.run('test -d teleplata', warn=True).failed:
        conn.run(f"git clone {REPO_URL}")


def install_packages():
    conn.sudo("apt-get update")
    conn.sudo(
        "apt-get install -y postgresql postgresql-contrib python3-pip python-dev virtualenv nginx")


def create_database():
    # conn.sudo(f'sudo -i -u postgres createdb {database}')
    # conn.sudo(f'psql -c "CREATE DATABASE {database};" -U postgres')
    conn.sudo(
        f"""psql -c "CREATE USER {username} WITH password \'{password}\'" -U postgres""")
    conn.sudo(
        f'psql -c "GRANT ALL ON DATABASE {database} TO {username};" -U postgres')
    conn.sudo(f'psql -c "ALTER USER {username} CREATEDB;" -U postgres')


def configure_project():
    # conn.put('instance/config.py', 'teleplata/instance/config.py')
    # conn.put('instance/nginx.conf', '/etc/nginx/sites-available/tele.conf')
    # conn.sudo('ln -s /etc/nginx/sites-available/tele.conf /etc/nginx/sites-enabled/')
    conn.sudo('service nginx restart')
    # with conn.cd('teleplata'):
    #     # create virtualenv
    #     conn.run('virtualenv --python=$(which python3) venv')
    #     conn.run('source venv/bin/activate && pip install -r requirements.txt')
    #     conn.run("flask run")


def run_application():
    with conn.cd('teleplata'):
        conn.run('source venv/bin/activate && gunicorn main:"create_app()"')


def main():
    configure_project()
    run_application()
    # pull_repository()
    # install_packages()
    # create_database()


main()
