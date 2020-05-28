import json
from flask_restplus import Resource
from application.resources.db_store.db_connection import MySQLDBConnection
from application import api

speakersController = api.namespace('speaker', description='Speakers Controller')


@speakersController.route('/verify')
class SpeakersController(Resource):

    def post(self):
        conn = MySQLDBConnection()
        query = "SELECT email, phone FROM tb_ag_user"
        data = conn.findBy(query)
        return json.dumps(data)
