[![Build Status](https://travis-ci.org/FUNNYDMAN/teleplata.svg?branch=master)](https://travis-ci.org/FUNNYDMAN/teleplata)
[![Coverage Status](https://coveralls.io/repos/github/FUNNYDMAN/teleplata/badge.svg?branch=master)](https://coveralls.io/github/FUNNYDMAN/teleplata?branch=master)
[![Requirements Status](https://requires.io/github/FUNNYDMAN/teleplata/requirements.svg?branch=master)](https://requires.io/github/FUNNYDMAN/teleplata/requirements/?branch=master)

# teleplata
> Site for selling circuits for tv


## Getting Started
1. Create and configure database

```bash
# change user to postgres and run psql tool
sudo -su postgres psql
```
Create database and user
```sql
CREATE DATABASE databasename;
CREATE USER username WITH password 'password'
GRANT ALL ON DATABASE databasename TO username;
ALTER USER username CREATEDB;
```

![teleplata screenshot](static/img/teleplata.png)