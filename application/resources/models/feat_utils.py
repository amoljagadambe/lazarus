import os
import librosa
import numpy
from scipy.signal import medfilt

POWER_SPECTRUM_FLOOR = 1e-100


def get_audio_and_silence_segment(audio_labels, frame_step):
    silence_flag = False
    audio_segments = []
    silence_segments = []
    current_audio_label = -1
    st_idx = -1

    for idx, label in enumerate(audio_labels):
        if label != current_audio_label:
            if st_idx == -1:  # start segment
                st_idx = idx
                current_audio_label = label
            else:
                # Set end index of current segment.
                end_idx = idx
                # Append current segment into speaker segments.
                if current_audio_label == silence_flag:
                    silence_segments.append([st_idx * frame_step, end_idx * frame_step])
                else:
                    audio_segments.append([st_idx * frame_step, end_idx * frame_step])
                # Set start index and label id of new audio segment
                st_idx = idx
                current_audio_label = label
        elif idx >= len(audio_labels) - 1:  # Check end silence value.
            end_idx = len(audio_labels)
            if end_idx - st_idx > 1:
                # Append current segment into speaker segments.
                if current_audio_label == silence_flag:
                    silence_segments.append([st_idx * frame_step, end_idx * frame_step])
                else:
                    audio_segments.append([st_idx * frame_step, end_idx * frame_step])
            break

    return audio_segments, silence_segments


def detect_audio_segment(energy_list, frame_step):
    sil_threshold = 0.0001  # 0.0005

    #  Filter speech interval with high energy frames
    speech_non_speech = energy_list >= sil_threshold
    speech_non_speech = medfilt(speech_non_speech, 3)

    audio_segments, silence_segments = get_audio_and_silence_segment(speech_non_speech, frame_step=frame_step)

    min_duration = 0.2
    audio_segments2 = []
    for s in audio_segments:
        if s[1] - s[0] > min_duration:
            # Append speech segment
            audio_segments2.append(s)
    audio_segments = audio_segments2
    return audio_segments, silence_segments


def read_audio_librosa(wav_path):
    return librosa.load(wav_path, sr=16000)


def mean_energy(frame):
    return numpy.sum(frame ** 2) / numpy.float64(len(frame))


def total_energy_list(signal, sample_rate, frame_win, frame_step):
    frame_win = int(frame_win)
    frame_step = int(frame_step)

    # Signal normalization
    signal = numpy.double(signal)
    _ = sample_rate

    sample_num = len(signal)  # total number of samples
    cur_pos = 0

    energy_list = []
    while cur_pos < sample_num - frame_win + 1:
        frame = signal[cur_pos : cur_pos + frame_win]
        cur_pos = cur_pos + frame_step
        energy_list.append(mean_energy(frame))

    return numpy.array(energy_list)


def audio_feat_with_librosa(signal, sample_rate, frame_len, frame_step):
    # Normalization of pcm data
    signal = numpy.double(signal)
    epsilon = 0.0000000001

    energy = librosa.feature.rmse(signal, frame_length=frame_len, hop_length=frame_step)
    mel_spectrogram = librosa.feature.melspectrogram(
        signal, sample_rate, n_fft=frame_len, hop_length=frame_step, n_mels=40, power=1.0
    )
    mel_filter_bank = librosa.power_to_db(mel_spectrogram)
    mfcc = librosa.feature.mfcc(S=mel_filter_bank, n_mfcc=19, dct_type=2)
    mel_filter_bank = mel_filter_bank / 10
    mel_filter_bank = mel_filter_bank.T
    mfcc[0, :] = numpy.log(energy + epsilon)
    mfcc = mfcc.T
    return energy, mel_filter_bank, mfcc


def feature_extraction(wav_path, frame_win, frame_step, vad_win):
    audio_data = read_audio_librosa(wav_path)
    wav_data = audio_data[0]
    sample_rate = audio_data[1]
    vad_energy = total_energy_list(wav_data, sample_rate, vad_win * sample_rate, vad_win * sample_rate)

    return vad_energy


def split_audio_librosa(wave_file, st_time, ed_time, dst_filename):
    """
    :param wave_file:       original audio file
    :param st_time:         star time to be trimmed     (miliseconds)
    :param ed_time:         end time to be trimmed      (miliseconds)
    :param dst_filename:    destination file name after trimming
    :return:                True if success, otherwise, False
    """
    if os.path.exists(dst_filename):
        os.remove(dst_filename)

    if not os.path.exists(wave_file):
        print("input file does not exist!")
        return False

    st_time = st_time / 1000
    ed_time = ed_time / 1000
    cvt_command = 'ffmpeg  -i \"{}\" -ss {:.2f} -to {:.2f} \"{}\" -y -loglevel panic'.format(
        wave_file, st_time, ed_time, dst_filename)
    try:
        os.system(cvt_command)
        return True
    except Exception as e:
        print(e)
        return False


def get_mfcc(wave_path):
    if not os.path.exists(wave_path):
        print("No such file: {}".format(os.path.basename(wave_path)))
        return []
    audio_data = read_audio_librosa(wave_path)
    wave_data = audio_data[0]
    sample_rate = audio_data[1]

    frame_len = int(0.25 * sample_rate)
    frame_step = int(0.01 * sample_rate)

    signal = numpy.double(wave_data)
    signal = signal / (2.0 ** 15)
    sig_mean = signal.mean()
    sig_max = (numpy.abs(signal)).max()
    signal = (signal - sig_mean) / (sig_max + 0.0000000001)

    # energy = librosa.feature.rmse(signal, frame_length=frame_len, hop_length=frame_step)
    mel_spectrogram = librosa.feature.melspectrogram(signal, sample_rate, n_fft=frame_len, hop_length=frame_step,
                                                     n_mels=40, power=1.0)
    mel_filter_bank = librosa.power_to_db(mel_spectrogram)
    mfcc = librosa.feature.mfcc(S=mel_filter_bank, n_mfcc=13, dct_type=2)
    # mel_filter_bank = mel_filter_bank/10
    # mel_filter_bank = mel_filter_bank.T
    # mfcc = mfcc[1:13]
    mfcc = mfcc.T

    return numpy.mean(mfcc, axis=0)


def speech_segments_with_vad(wav_path):

    frame_step = 0.025
    frame_size = 0.05
    vad_win = 0.1

    vad_energy = feature_extraction(wav_path, frame_size, frame_step, vad_win)
    audio_segs = detect_audio_segment(vad_energy, vad_win)
    speech_segments = audio_segs[0]
    if not speech_segments:
        return [0,0]
    # return speech_segments
    return [speech_segments[0][0], speech_segments[-1][1]]


def convert_file(src_file, dst_file):
    convert_cmd = 'ffmpeg -i \"{}\" -acodec pcm_s16le -ac 1 -ar 16000 \"{}\" -y -loglevel panic'.format(
        src_file,
        dst_file)
    try:
        os.system(convert_cmd)
        return True
    except Exception as error:
        print(error)
        return False

