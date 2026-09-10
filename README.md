# Strong-hold
App that detects port-scans and flood attackes

## Technologies and options:
- lightweight, open source, secure, free and can be personalized
- Use python for core, mysql for database and Flask framework for Monitoring site
- Easy setup
- A flask webapp to monitor whole things happening (instead of using Terminal)
- ML model using IsolatedForest from sklearn

## Setup:
- First make sure you have [python3](https://www.python.org/downloads/)
- Make sure you have installed mysql, Bestway to do it is using [docker](https://www.docker.com/), use `docker pull mysql:8`
- clone this project with `git clone https://github.com/arshia2012/Strong-hold` or just download it here and extract it
- Change Directory to project folder
- Install the requirements.txt file `pip install -r requirement.txt`
- Go to .env.example file, fill the `DB_PASS` with whatever you like, remember it and then change the file from .env.example to .env
- Then run mysql `docker run -d --name mysql-stronghold -e MYSQL_ROOT_PASSWORD=Your_password_here -p 3306:3306 mysql:8`, remember to write your password exactly what you write in .env
- **Don't turn mysql off (Keyboard interrupt), when you are using it or doing the setup**
- Run `python3 config.py` then `python3 setup_db.py` And after that `python3 db_connector.py`
- For test, run `python3 event_logger.py` and `python3 stats_logger.py` too
- Run `python3 argus.py` and wait for at least 1 hour, in this 1 hour, turn all things on and **Attack the ip address argus is running on with port scan and flood** and Make sure, thats your ip, **This project is for legal usage only**
- Then, after at least one hour, you can turn the arugus off by `ctl+c` and Run `python3 train_model.py`
- After it finished it's work, Stronghold is ready for work, Run `python3 argus.py` first and for Webapp monitoring, run `python3 app.py`
- After you turned the Webapp on, go to *http://localhost:5000* and here you can see data that argus get in web

## Screenshots of result example:
- Terminal View:
<img width="1118" height="375" alt="image" src="https://github.com/user-attachments/assets/04ce532a-90bf-4e46-b4f8-34b33e930da7" />
Webapp View:
<img width="1643" height="263" alt="Screenshot 2026-09-10 190257" src="https://github.com/user-attachments/assets/1b336fa9-9767-4c8d-9cc3-6fc0905e5b19" />


## Notes:
- This is an Educational app, so **There are false positives** in The project
- Before taking action to the attacker ip, make sure it isn't a false posetive
- You can make sure By giving the ip to AI and ask if this ip is for a company (*Most false positives are because google or Microsoft IP*)
- **Use this App for Educational and Legal use only**
