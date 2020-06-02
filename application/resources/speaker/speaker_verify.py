from application.resources.models.feature_extraction import extract_features
import _pickle as cPickle
from scipy.io.wavfile import read
import numpy as np
import os

# path to training data
train_audio_root_path = "/gais/user-files/audio/"
model_store_path = "/application/resources/stored_models/"
BASE_DIR = os.getcwd()
FULL_PATH = BASE_DIR + model_store_path

gmm_files = [os.path.join(FULL_PATH, fname) for fname in
             os.listdir(FULL_PATH) if fname.endswith('.gmm')]

# Load the Gaussian gender Models
models = [cPickle.load(open(fname, 'rb')) for fname in gmm_files]
speakers = [fname.split("/")[-1].split(".gmm")[0] for fname
            in gmm_files]


def verify_speaker(path: str, user_id: int):

    sr, audio = read(path)
    vector = extract_features(audio, sr)
    print(vector)
    log_likelihood = np.zeros(len(models))
    for i in range(len(models)):
        gmm = models[i]  # checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()

    deteced_id = np.argmax(log_likelihood)
    # print("\tdetected as - ", speakers[deteced_id])

    if speakers[deteced_id] == user_id:
        return "Speaker Verified"

    else:
        return "Speaker actual id is {}".format(speakers[deteced_id])
