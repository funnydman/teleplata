import logging

from fabric import task
# logger configs
from invoke import Collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('fabfile.log')
handler.setLevel(logging.INFO)

logger.addHandler(handler)
# end logger configs

try:
    from instance.configs.prod import DATABASE
except ImportError:
    logger.error('Failed to open file', exc_info=True)
    raise ImportError("Can't find instance config. Did you import it?")

# sudo_pass = getpass.getpass("What's your sudo password?")

database = DATABASE['database']
username = DATABASE['username']
password = DATABASE['password']

PACKAGES_TO_INSTALL = ("build-essential", "postgresql", "postgresql-contrib", "python3-pip", "python-dev", "virtualenv",
                       "nginx")

REPO_URL = 'https://github.com/FUNNYDMAN/teleplata.git'

# TODO get repo name from repo_url
REPO_NAME = 'teleplata'

hosts = ['tele']


@task(hosts=hosts)
def pull_repo(conn, branch='master'):
    """Clone repository if doesn't exist else pull changes."""
    if conn.run(f'test -d {REPO_NAME}', warn=True).failed:
        logger.info("Start cloning repository...")
        conn.run(f"git clone -b {branch} {REPO_URL}")
    else:
        with conn.cd(f"{REPO_NAME}"):
            logger.info("Pulling repository...")
            conn.run("git pull")


@task(hosts=hosts)
def install_packages(conn):
    """Install necessary packages."""
    conn.sudo("apt-get update")
    conn.sudo(f"apt-get install -y {' '.join(PACKAGES_TO_INSTALL)}")
    conn.run("curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -")
    conn.sudo("apt-get install -y nodejs")

    conn.run("wget https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.xenial_amd64.deb")
    conn.sudo("dpkg -i wkhtmltox_0.12.5-1.xenial_amd64.deb")
    conn.sudo("apt-get -f install -y")


@task(hosts=hosts)
def install_python(conn):
    conn.sudo("add-apt-repository ppa:deadsnakes/ppa")
    conn.sudo("apt-get update")
    conn.sudo("apt-get install -y python3.6")


@task(hosts=hosts)
def install(conn):
    install_packages(conn)
    install_python(conn)


@task(hosts=hosts)
def build_statics(conn):
    """Build staticfiles."""
    logger.info("Start building staticfiles...")
    with conn.cd(f'{REPO_NAME}/static'):
        if conn.run("test -d node_modules", warn=True).failed:
            conn.run("npm install && npm run build")


@task(hosts=hosts)
def create_database(conn):
    """Create and configure database."""
    # TODO update pg_hba.conf file
    if conn.sudo(f'psql -c "CREATE DATABASE {database};" -U postgres', warn=True).ok:
        conn.sudo(
            f"""psql -c "CREATE USER {username} WITH password \'{password}\'" -U postgres""")
        conn.sudo(
            f'psql -c "GRANT ALL ON DATABASE {database} TO {username};" -U postgres')
        conn.sudo(f'psql -c "ALTER USER {username} CREATEDB;" -U postgres')


@task(hosts=hosts)
def configure_server(conn):
    """Configure the server."""
    # this is crap put doesn't work when remote path need sudo
    conn.put('instance/configs/prod.py', f'{REPO_NAME}/instance/configs/prod.py')
    conn.sudo.put('instance/nginx.conf', '/etc/nginx/sites-available/tele.conf', preserve_mode=False)
    conn.sudo('ln -s /etc/nginx/sites-available/tele.conf /etc/nginx/sites-enabled/', warn=True)
    conn.sudo('service nginx reload')
    # absolute path
    conn.sudo('sudo systemctl enable instance/teleplata.service')
    conn.sudo('sudo systemctl start teleplata.service')
    conn.sudo('sudo systemctl status teleplata.service')
    conn.sudo('sudo systemctl daemon-reload')


@task(hosts=hosts)
def create_env(conn):
    """Create and configure virtualenv."""
    # install python3.6
    with conn.cd(f'{REPO_NAME}'):
        if conn.run('test -d venv', warn=True).failed:
            conn.run('virtualenv --python=$(which python3.6) venv')
            conn.run('source venv/bin/activate && pip install -r requirements.txt')


@task(hosts=hosts)
def run_app(conn):
    """Run application."""
    with conn.cd(f'{REPO_NAME}'):
        conn.run('source venv/bin/activate && gunicorn teleplata.main:"create_app()"')


ns = Collection(pull_repo, install, install_packages, install_python, build_statics, create_database,
                configure_server, create_env,
                run_app)
ns.configure({'sudo': {'password': 'password'}})
