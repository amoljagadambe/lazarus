from application.resources.db_store.db_connection import MySQLDBConnection
from application.resources.speaker.user_input import user_fields
import json
from flask_restplus import Resource

from application import api

speakersController = api.namespace('speaker', description='Speakers Controller')


@speakersController.route('/verify')
class SpeakersController(Resource):

    # @api.doc('example_field')
    # @api.expect(user_fields, validate=False)
    def post(self):
        conn = MySQLDBConnection()
        query = "SELECT id FROM tb_ag_user"
        data = conn.findBy(query)
        for u_id in data:
            print(type(u_id[0]))
            print(u_id[0])
        return json.dumps(data)
