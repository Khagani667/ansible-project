# Ansible Project

## Overview
The project depicts deploying a Flask web application with a MySQL backend using **Ansible roles**, **Docker**, and **Ansible Vault** for sensitive credentials.

---

## Directory Structure
```
ansible-project/
├─ roles/
│ ├─ database/
│ │ ├─ tasks/main.yml
│ ├─ webapp/
│ │ ├─ tasks/main.yml
│ │ ├─ files/app.py
│ │ ├─ files/Dockerfile
├─ playbook.yml
├─ inventory.ini
├── group_vars
│   └── all
│   └── vault.yml
└─ README.md
```

---

## Prerequisites

- Ansible installed on your control machine.
- Python3 on the target server.
- SSH access to the target server.
- Docker installed on the target server (handled automatically by role).
- MySQL server installed on the target server (handled automatically by role).

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone git@github.com:Khagani667/ansible-project.git
cd your-project


### 2. Set Up Ansible Vault
Vault stores sensitive credentials in a secure way.

```bash
mkdir -p group_vars/all
ansible-vault create group_vars/all/vault.yml
```

Example content inside `vault.yml`:
```yaml
db_password: VerySolidPassword667
```

### 3. Configure Inventory
Edit `hosts.ini` to include your target server:
```ini
[app]
ubuntu ansible_host=$ip_of_hosting_machine ansible_user=root ansible_ssh_private_key_file=~/.ssh/id_ed25519
```

---

### 4. Run the Playbook
Deploy the MySQL database, web application, and Docker container:

```bash
ansible-playbook -i inventory.ini playbook.yml --ask-vault-pass
```

Step-by-step example:
```bash
# Run playbook with vault password prompt
ansible-playbook -i inventory.ini playbook.yml --ask-vault-pass

# When prompted, enter your vault password to decrypt db credentials
Vault password: *****************
```

That will ensure:

1. Install MySQL, create database `myappdb` and user `myappuser`.
2. Copy `app.py` and `Dockerfile` to the target server.
3. Build the Docker image for the Flask app.
4. Run the container with environment variables from the Vault.

---

### 5. Verify Deployment
Check the web application with `curl`:

```bash
curl -X POST http://$ip_of_hosting_machine:3000/login \
-H "Content-Type: application/json" \
-d '{"username":"admin","password":"admin"}'
```

Expected response:
```json
{"status": "success", "message": "Login successful!"}
```

Visit `http://$ip_of_hosting_machine:3000/` for the homepage.

---

### 6. Debugging Tips
- If `500 Internal Server Error` occurs:
  - Ensure the database user and password match the Vault.
  - Verify MySQL is listening on `0.0.0.0` (check `/etc/mysql/mysql.conf.d/mysqld.cnf`).
  - Check Docker container logs:
    ```bash
    sudo docker logs webapp
    ```

- Test MySQL connection from inside the container:
```bash
sudo docker exec -it webapp python
>>> import mysql.connector
>>> mysql.connector.connect(
...     host="$ip_of_hosting_machine",
...     user="myappuser",
...     password="VerySolidPassword667",
...     database="myappdb"
... )
```

---
