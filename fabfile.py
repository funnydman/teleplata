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

REPO_URL = 'https://github.com/FUNNYDMAN/teleplata.git'

# TODO get repo name from repo_url
REPO_NAME = 'teleplata'


def pull_repository():
    if conn.run(f'test -d {REPO_NAME}', warn=True).failed:
        conn.run(f"git clone {REPO_URL}")


def install_packages():
    conn.sudo("apt-get update")
    conn.sudo(
        "apt-get install -y postgresql postgresql-contrib python3-pip python-dev virtualenv nginx")
    conn.sudo("curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -")
    conn.sudo("sudo apt-get install -y nodejs")


def build_staticfiles():
    with conn.cd(f'{REPO_NAME}/static'):
        if conn.run("test -d node_modules", warn=True).failed:
            conn.run("npm install")
        conn.run("npm run build")


def create_database():
    if conn.sudo(f'psql -c "CREATE DATABASE {database};" -U postgres', warn=True).ok:
        conn.sudo(
            f"""psql -c "CREATE USER {username} WITH password \'{password}\'" -U postgres""")
        conn.sudo(
            f'psql -c "GRANT ALL ON DATABASE {database} TO {username};" -U postgres')
        conn.sudo(f'psql -c "ALTER USER {username} CREATEDB;" -U postgres')


def configure_project():
    conn.put('instance/config.py', f'{REPO_NAME}/instance/config.py')
    conn.put('instance/nginx.conf', '/etc/nginx/sites-available/tele.conf')
    conn.sudo('ln -s /etc/nginx/sites-available/tele.conf /etc/nginx/sites-enabled/', warn=True)
    conn.put('instance/teleplata.conf', '/etc/supervisor/conf.d/teleplata.conf')
    conn.sudo("sudo supervisorctl reload")
    conn.sudo('service nginx reload')
    with conn.cd(f'{REPO_NAME}'):
        # create and configure virtualenv
        if conn.run('test -d venv', warn=True).failed:
            conn.run('virtualenv --python=$(which python3) venv')
            conn.run('source venv/bin/activate && pip install -r requirements.txt')


def run_application():
    with conn.cd(f'{REPO_NAME}'):
        conn.run('source venv/bin/activate && gunicorn main:"create_app()"')


def main():
    # pull_repository()
    # install_packages()
    # build_staticfiles()
    # create_database()
    configure_project()
    # run_application()


main()
