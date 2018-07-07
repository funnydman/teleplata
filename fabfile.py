from fabric import Connection, Config

from instance.config import DATABASE

# sudo_pass = getpass.getpass("What's your sudo password?")
sudo_pass = 'optimus1234'
config = Config(overrides={'sudo': {'password': sudo_pass}})
conn = Connection(host='autobot', config=config)

PROJECT_DIR = conn.run('pwd')

VENV_DIR = f'{PROJECT_DIR}/venv'

REPO_URL = 'https://github.com/FUNNYDMAN/teleplata.git'

database = DATABASE['database']


def pull_repository():
    if conn.run('test -d teleplata', warn=True).failed:
        conn.run(f"git clone {REPO_URL}")


def install_packages():
    conn.sudo("apt-get update")
    conn.sudo(
        "apt-get install -y postgresql postgresql-contrib python3-pip python-dev virtualenv")


def create_database():
    res = conn.sudo(f'sudo -i -u postgres createdb {database}')


def configure_project():
    with conn.cd('teleplata'):
        conn.run('source venv/bin/activate && pip install -r requirements.txt')
    conn.put('instance/config.py',
             '/home/optimus/teleplata/instance/config.py')


def main():
    # install_packages()
    # pull_repository()
    # create_database()
    configure_project()


main()
