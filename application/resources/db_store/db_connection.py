from application.resources.db_store.utils import config
from mysql.connector import errorcode
import mysql.connector as connection
from application import app

db_values = config['mysqld']


class MySQLDBConnection:
    ds = None

    def __init__(self):
        app.logger.info('MySQLDBConnection initiated....')
        # TODO : Add proper Logging with logger module
        try:
            self.ds = connection.connect(**db_values)
        except connection.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                app.logger.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                app.logger.error("Database does not exist")
            else:
                app.logger.error(err)

    def get_cursor(self):
        return self.ds.cursor()

    def findBy(self, sql):
        self.cur = self.get_cursor()
        self.cur.execute(sql)
        return self.cur.fetchall()
