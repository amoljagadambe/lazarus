from flask_restx import fields
from application import api

user_fields = api.model('Speakers Verification', {
    'user_id': fields.Integer(required=True),
    'audio_location': fields.String(required=True)
})

