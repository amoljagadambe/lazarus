from application.resources.speaker.speaker_verify import verify_speaker
from application.resources.speaker.user_input import user_fields
from flask_restx import Resource
from flask import request
import json


from application import api

speakersController = api.namespace('speaker', description='Speakers Controller')


@speakersController.route('/verify')
class SpeakersController(Resource):

    @api.expect(user_fields, validate=False)
    def post(self):
        json_data = request.get_json(force=True)
        file_path = json_data['audio_location']
        user_id = json_data['user_id']
        print(file_path)
        verfied_status = verify_speaker(file_path, user_id)
        return json.dumps(verfied_status)
