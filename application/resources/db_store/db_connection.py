from application.resources.db_store.utils import config
from mysql.connector import connection
from application import app

db_values = config['mysqld']


class MySQLDBConnection:
    ds = None

    def __init__(self):
        app.logger.info('MySQLDBConnection initiated....')
        # TODO : Add proper Logging with logger module
        self.ds = connection.MySQLConnection(**db_values)

    def get_data_source(self):
        return self.ds
