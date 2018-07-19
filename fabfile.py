import logging

from fabric import task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('fabfile.log')
handler.setLevel(logging.INFO)

logger.addHandler(handler)
try:
    from instance.configs.prod import DATABASE
except ImportError:
    logger.error('Failed to open file', exc_info=True)
    raise ImportError("Can't find instance config. Did you import it?")

database = DATABASE['database']
username = DATABASE['username']
password = DATABASE['password']

PACKAGES_TO_INSTALL = ("build-essential", "postgresql", "postgresql-contrib", "python3-pip", "python-dev", "virtualenv",
                       "nginx", "supervisor")

REPO_URL = 'https://github.com/FUNNYDMAN/teleplata.git'

# TODO get repo name from repo_url
REPO_NAME = 'teleplata'


@task
def pull_repo(conn):
    """Clone repository if doesn't exist else pull changes."""

    if conn.run(f'test -d {REPO_NAME}', warn=True).failed:
        logger.info("Start cloning repository...")
        conn.run(f"git clone {REPO_URL}")
    else:
        with conn.cd(f"{REPO_NAME}"):
            logger.info("Pulling repository...")
            conn.run("git pull")


# TODO fix problem with sudo mode. Tasks doesn't work with conn.sudo
# Problem: a task trying to get root password from a console
@task
def install_packages(conn):
    """Install necessary packages."""
    conn.sudo("apt-get update")
    conn.sudo(f"apt-get install -y {' '.join(PACKAGES_TO_INSTALL)}")
    conn.sudo("curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -")
    conn.sudo("apt-get install -y nodejs")


@task(pull_repo, install_packages)
def build_statics(conn):
    """Build staticfiles."""
    with conn.cd(f'{REPO_NAME}/static'):
        if conn.run("test -d node_modules", warn=True).failed:
            conn.run("npm install && npm run build")


@task
def create_database(conn):
    """Create and configure database."""
    if conn.sudo(f'psql -c "CREATE DATABASE {database};" -U postgres', warn=True).ok:
        conn.sudo(
            f"""psql -c "CREATE USER {username} WITH password \'{password}\'" -U postgres""")
        conn.sudo(
            f'psql -c "GRANT ALL ON DATABASE {database} TO {username};" -U postgres')
        conn.sudo(f'psql -c "ALTER USER {username} CREATEDB;" -U postgres')


@task(pull_repo)
def configure_server(conn):
    """Configure the server."""
    conn.put('instance/configs/prod.py', f'{REPO_NAME}/instance/configs/prod.py')
    conn.put('instance/nginx.conf', '/etc/nginx/sites-available/tele.conf')
    conn.sudo('ln -s /etc/nginx/sites-available/tele.conf /etc/nginx/sites-enabled/', warn=True)
    conn.put('instance/teleplata.conf', '/etc/supervisor/conf.d/teleplata.conf')
    conn.sudo("sudo supervisorctl reload")
    conn.sudo('service nginx reload')


@task(pull_repo)
def create_env(conn):
    """Create and configure virtualenv."""
    with conn.cd(f'{REPO_NAME}'):
        if conn.run('test -d venv', warn=True).failed:
            conn.run('virtualenv --python=$(which python3) venv')
            conn.run('source venv/bin/activate && pip install -r requirements.txt')


@task(pull_repo, install_packages, create_env, configure_server)
def run_app(conn):
    """Run application."""
    with conn.cd(f'{REPO_NAME}'):
        conn.run('source venv/bin/activate && gunicorn main:"create_app()"')


@task(pull_repo, install_packages, build_statics, create_database, configure_server, create_env, run_app)
def build(conn):
    conn.run("Configured")
