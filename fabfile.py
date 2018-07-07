from fabric import Connection, Config

from instance.config import DATABASE

# sudo_pass = getpass.getpass("What's your sudo password?")
sudo_pass = 'optimus1234'
config = Config(overrides={'sudo': {'password': sudo_pass}})
conn = Connection(host='autobot', config=config)


def pull_repository():
    if conn.run('test -d teleplata', warn=True).failed:
        conn.run("git clone https://github.com/FUNNYDMAN/teleplata.git")


def install_postgres():
    conn.sudo("apt-get update")
    conn.sudo("apt-get install -y postgresql postgresql-contrib")


def configure_database():
    password = DATABASE['password']


def main():
    # install_postgres()
    pull_repository()


main()
