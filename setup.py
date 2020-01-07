import os

os.system("virtualenv .")
os.system("source bin/activate")
os.system("pip install -r requirements.txt")
os.system("cat bin/postactivate")
os.system("export $(cat .env)")