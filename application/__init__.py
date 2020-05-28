from apscheduler.schedulers.background import BackgroundScheduler
from application.resources.models.model_controller import sensor
from flask import Flask
from flask_cors import CORS
from flask_restx import Api

"""
init BackgroundScheduler job daemon 
parameter helps to close all thread 
after closing the application
"""
sched_data = BackgroundScheduler(daemon=True)
# in your case you could change seconds to hours
sched_data.add_job(sensor, 'interval', seconds=5)
sched_data.start()

app = Flask(__name__)
CORS(app)

api = Api(app, title='Lazarus Pit', version='1.0', description='Created by Amol Jagadambe',
          default='Lazarus API', default_label='Web Services', doc='/swagger-ui.html/',
          validate=False, contact_url='http://www.gais.co.in', contact_email='amol.jagadambe@gmail.com',
          license='Apache 2.0', license_url='http://www.apache.org/licenses/LICENSE-2.0',
          )

from application.resources import home
