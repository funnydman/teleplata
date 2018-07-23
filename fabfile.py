import logging

from fabric import task

# logger configs

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

# use this if you need to type root password
# sudo_pass = getpass.getpass("What's your sudo password?")
# config = Config(overrides={'sudo': {'password': sudo_pass}})
# conn = ConnectionCall(task={}, init_kwargs={'host': 'tele'})

database = DATABASE['database']
username = DATABASE['username']
password = DATABASE['password']

PACKAGES_TO_INSTALL = ("build-essential", "postgresql", "postgresql-contrib", "python3-pip", "python-dev", "virtualenv",
                       "nginx")

REPO_URL = 'https://github.com/FUNNYDMAN/teleplata.git'

# TODO get repo name from repo_url
REPO_NAME = 'teleplata'


@task()
def pull_repo(conn, branch='master'):
    """Clone repository if doesn't exist else pull changes."""
    if conn.run(f'test -d {REPO_NAME}', warn=True).failed:
        logger.info("Start cloning repository...")
        conn.run(f"git clone -b {branch} {REPO_URL}")
    else:
        with conn.cd(f"{REPO_NAME}"):
            logger.info("Pulling repository...")
            conn.run("git pull")


# TODO fix problem with sudo mode. Tasks doesn't work with conn.sudo
# Problem: a task trying to get root password from a console
@task
def install_packages(conn):
    """Install necessary packages."""
    conn.run("sudo apt-get update")
    conn.run(f"sudo apt-get install -y {' '.join(PACKAGES_TO_INSTALL)}")
    conn.run("sudo curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -")
    conn.run("sudo apt-get install -y nodejs")

    conn.run("sudo wget https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.xenial_amd64.deb")
    conn.run("sudo dpkg -i wkhtmltox_0.12.5-1.xenial_amd64.deb")
    conn.run("sudo apt-get -f install -y")


# inner = Collection('inner', pull_repo, install_packages)
# inner.configure({'sudo': 'funnydman'})


@task
def install_deps_for_elasticsearch(conn):
    conn.run("sudo apt-get update")
    conn.run("sudo apt-get install -y default-jre default-jdk")
    conn.run("sudo add-apt-repository ppa:webupd8team/java")
    conn.run("sudo apt-get update")
    conn.run("sudo apt-get install -y oracle-java8-installer")


@task
def build_statics(conn):
    """Build staticfiles."""
    logger.info("Start building staticfiles...")
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


@task
def configure_server(conn):
    """Configure the server."""
    conn.put('instance/configs/prod.py', f'{REPO_NAME}/instance/configs/prod.py')
    conn.put('instance/nginx.conf', '/etc/nginx/sites-available/tele.conf')
    conn.sudo('ln -s /etc/nginx/sites-available/tele.conf /etc/nginx/sites-enabled/', warn=True)
    conn.put('instance/teleplata.conf', '/etc/supervisor/conf.d/teleplata.conf')
    conn.sudo("sudo supervisorctl reload")
    conn.sudo('service nginx reload')


@task
def create_env(conn):
    """Create and configure virtualenv."""
    with conn.cd(f'{REPO_NAME}'):
        if conn.run('test -d venv', warn=True).failed:
            conn.run('virtualenv --python=$(which python3.6) venv')
            conn.run('source venv/bin/activate && pip install -r requirements.txt')


@task
def run_app(conn):
    """Run application."""
    with conn.cd(f'{REPO_NAME}'):
        conn.run('source venv/bin/activate && gunicorn main:"create_app()"')
