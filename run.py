from application import app
from dotenv import load_dotenv
import os

env_path = '{0}\\.env'.format(os.getcwd())
load_dotenv(dotenv_path=env_path)

if __name__ == '__main__':
    app.run()
