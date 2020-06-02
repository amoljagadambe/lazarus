import _pickle as cPickle
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