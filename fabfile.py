from fabric import Connection

try:
    from instance.configs.prod import DATABASE
except ImportError:
    raise ImportError("Can't find instance config. Did you import it?")

REMOTE_HOST = 'tele'
REMOTE_USER = ''
REMOTE_PASS = ''

database = DATABASE['database']
username = DATABASE['username']
password = DATABASE['password']

PACKAGES_TO_INSTALL = ("build-essential", "postgresql", "postgresql-contrib", "python3-pip", "python-dev", "virtualenv",
                       "nginx", "supervisor")

# use this if you need to type root password
# sudo_pass = getpass.getpass("What's your sudo password?")
# config = Config(overrides={'sudo': {'password': REMOTE_PASS}})
# conn = Connection(host=REMOTE_HOST, config=config)
conn = Connection(host=REMOTE_HOST)

REPO_URL = 'https://github.com/FUNNYDMAN/teleplata.git'

# TODO get repo name from repo_url
REPO_NAME = 'teleplata'


def pull_repository():
    if conn.run(f'test -d {REPO_NAME}', warn=True).failed:
        conn.run(f"git clone {REPO_URL}")
    else:
        with conn.cd(f"{REPO_NAME}"):
            conn.run("git pull")


def install_packages():
    conn.sudo("apt-get update")
    conn.sudo(f"apt-get install -y {' '.join(PACKAGES_TO_INSTALL)}")
    conn.sudo("curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -")
    conn.sudo("sudo apt-get install -y nodejs")


def build_staticfiles():
    with conn.cd(f'{REPO_NAME}/static'):
        # if conn.run("test -d node_modules", warn=True).failed:
        conn.run("npm install && npm run build")
        # conn.run("npm run build")


def create_database():
    if conn.sudo(f'psql -c "CREATE DATABASE {database};" -U postgres', warn=True).ok:
        conn.sudo(
            f"""psql -c "CREATE USER {username} WITH password \'{password}\'" -U postgres""")
        conn.sudo(
            f'psql -c "GRANT ALL ON DATABASE {database} TO {username};" -U postgres')
        conn.sudo(f'psql -c "ALTER USER {username} CREATEDB;" -U postgres')


def configure_server():
    conn.put('instance/configs/prod.py', f'{REPO_NAME}/instance/configs/prod.py')
    conn.put('instance/nginx.conf', '/etc/nginx/sites-available/tele.conf')
    conn.sudo('ln -s /etc/nginx/sites-available/tele.conf /etc/nginx/sites-enabled/', warn=True)
    conn.put('instance/teleplata.conf', '/etc/supervisor/conf.d/teleplata.conf')
    conn.sudo("sudo supervisorctl reload")
    conn.sudo('service nginx reload')


def configure_project():
    with conn.cd(f'{REPO_NAME}'):
        # create and configure virtualenv
        if conn.run('test -d venv', warn=True).failed:
            conn.run('virtualenv --python=$(which python3) venv')
            conn.run('source venv/bin/activate && pip install -r requirements.txt')


def run_tox():
    conn.run("tox")


def run_application():
    with conn.cd(f'{REPO_NAME}'):
        conn.run('source venv/bin/activate && gunicorn main:"create_app()"')


def main():
    pull_repository()
    install_packages()
    build_staticfiles()
    create_database()
    configure_server()
    configure_project()
    run_application()


main()
