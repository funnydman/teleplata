# teleplata
> SITE FOR SELLING CIRCUITS AND COMPONENTS FOR TVs

[![Build Status](https://travis-ci.org/FUNNYDMAN/teleplata.svg?branch=master)](https://travis-ci.org/FUNNYDMAN/teleplata)
[![Coverage Status](https://coveralls.io/repos/github/FUNNYDMAN/teleplata/badge.svg?branch=master)](https://coveralls.io/github/FUNNYDMAN/teleplata?branch=master)
[![Requirements Status](https://requires.io/github/FUNNYDMAN/teleplata/requirements.svg?branch=master)](https://requires.io/github/FUNNYDMAN/teleplata/requirements/?branch=master)




## Getting Started
1. Install ansible package
```bash
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```
2. Specify your variables in ```ansible/group_vars/webservers/web.yml``` file

3. Run ansible with dev configuration

```bash
ansible-playbook ansible/site.yml -i ansible/dev
```

4. Run webpack to collect static


```bash
# go to static directory and execute

npm install
npm run dev
```

5. Run application
```bash
flask run
```

## Screenshots
![teleplata screenshot](static/img/teleplata.png)