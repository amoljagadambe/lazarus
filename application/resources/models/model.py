from application.resources.models.feature_extraction import extract_features
from application.resources.models.feat_utils import convert_file, speech_segments_with_vad
from application.resources.db_store.db_connection import MySQLDBConnection
import _pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GMM
import os

# path to training data
train_audio_root_path = "/gais/user-files/audio/"
model_store_path = "/application/resources/stored_models/"
BASE_DIR = os.getcwd()


# get the user_id for specific user file access
def get_user_id():
    conn = MySQLDBConnection()
    query = "SELECT id FROM tb_ag_user"
    data = conn.findBy(query)
    for user_id in data:
        yield user_id


def train_model():
    iter_user_id = get_user_id()
    for u_id in iter_user_id:
        list_sentence_file = []
        user_file_path = train_audio_root_path + str(u_id[0]) + '/sentence/'
        features = np.asarray(())
        for x in os.walk(user_file_path):
            list_sentence_file = x[2]
        for i in range(0, 21):
            file_name = list_sentence_file[i].split('.')
            src = user_file_path + list_sentence_file[i]
            destination = user_file_path + file_name + '_' + 'converted' + '.wav'
            is_converted = convert_file(src, destination)
            sp_seg = speech_segments_with_vad(destination)

            # read the audio
            sr, audio = read(destination)

            # extract 40 dimensional MFCC & delta MFCC features
            vector = extract_features(audio, sr)

            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))
            # when features of 5 files of speaker are concatenated, then do model training
            # -> if count == 5: --> edited below
            if i == 20:
                gmm = GMM(n_components=16, max_iter=200, covariance_type='diag', n_init=3)
                gmm.fit(features)

                # dumping the trained gaussian model
                picklefile = str(u_id[0]) + ".gmm"
                cPickle.dump(gmm, open(BASE_DIR + model_store_path + picklefile, 'wb'))
                print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
                print(len(features))

    return "modeling completed"


