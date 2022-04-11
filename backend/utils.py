import os
import datetime 
import uuid
import enum
import datetime
import magic
from dotenv import load_dotenv

def check_admin_credential(admin_email):
    load_dotenv()
    ADMIN_EMAIL_LIST = os.getenv(
        'ADMIN_EMAIL_LIST', default="")
    ADMIN_EMAIL_LIST = ADMIN_EMAIL_LIST.split(",")
    if admin_email in ADMIN_EMAIL_LIST:
        return True
    else:
        return False


def is_plaintext(file_path):
    f = magic.Magic(mime=True)
    return True if (f.from_file(file_path) == 'text/plain') else False

def is_csv(file_path):
    f = magic.Magic(mime=True)
    return True if (f.from_file(file_path) == 'application/csv' or f.from_file(file_path) == 'text/csv' or f.from_file(file_path) == 'text/plain') else False

def get_uuid():
    return str(uuid.uuid4())
    
def get_AOETime(to_str = True):
    aoe_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=12))
    if to_str:
        return aoe_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return aoe_time.replace(microsecond=0)

def get_AOE_today(to_str=True):
    aoe_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=12)).replace(hour=0,minute=0,second=0,microsecond=0)
    if to_str:
        return aoe_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return aoe_time

def get_AOE_week(to_str=True):
    # Sunday is the start
    aoe_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=12)).replace(hour=0,minute=0,second=0,microsecond=0) - datetime.timedelta(days=datetime.datetime.today().weekday() + 1)
    if to_str:
        return aoe_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return aoe_time

def admin_submission_records_parser(submission_records, configs):
    return submission_records_parser(submission_records, configs, mode="individual", competition_type="hidden")


def submission_records_parser(submission_records, configs, mode="individual", competition_type="public"):

    def __submission_records_parser(attribute, key_name):
        if attribute is None:
            return "-"
        elif attribute == "":
            return "-"
        elif isinstance(attribute, enum.Enum):
            return attribute.name
        elif isinstance(attribute, datetime.datetime):
            return attribute.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(attribute, float):
            if (("stoi" in key_name) or ("mtwv" in key_name) or ("map" in key_name) or ("per" in key_name) or ("acc" in key_name) or ("wer" in key_name) or ("f1" in key_name) or ("cer" in key_name) or ("eer" in key_name)):
                return round(attribute * 100, 2)
            elif ("der" in key_name):
                return round(attribute, 2)
            else:
                return attribute
        else:
            return attribute
    if mode == "individual":
        if competition_type == "public":
            config_mode = "INDIVIDUAL_SUBMISSION_INFO"
        elif competition_type == "hidden":
            config_mode = "INDIVIDUAL_HIDDEN_SUBMISSION_INFO"

    elif mode == "leaderboard":
        if competition_type == "public":
            config_mode = "LEADERBOARD_INFO"
        elif competition_type == "hidden":
            config_mode = "LEADERBOARD_HIDDEN_INFO"
    file_info_list = configs[config_mode]["FILE"]
    score_info_list = configs[config_mode]["SCORE"]

    submission_info = []
    for file_model in submission_records:
        single_info = {}
        score_model = file_model.scores[0]
        for file_info in file_info_list:
            single_info[file_info] = __submission_records_parser(file_model.__dict__[file_info], file_info)
        for score_info in score_info_list:
            single_info[score_info] = __submission_records_parser(score_model.__dict__[score_info], score_info)
        
        submission_info.append(single_info)
    return submission_info

def get_leaderboard_default():
    data = [{
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "FBANK",
            "modelURL":"-",
            "modelDesc": "classic feature",
            "stride":10,
            "inputFormat": "waveform",
            "corpus":"-",
            "paramDesc":"-",
            "paramShared": 0,
            "fineTunedParam":"-",
            "taskSpecParam":"-",
            "PR_per_public": 82.01,
            "KS_acc_public": 41.3826674,
            "IC_acc_public": 9.649354219,
            "SID_acc_public": 20.058174,
            "ER_acc_public": 48.23672168,
            "ERfold1_acc_public": "-",
            "ERfold2_acc_public": "-",
            "ERfold3_acc_public": "-",
            "ERfold4_acc_public": "-",
            "ERfold5_acc_public": "-",
            "ASR_wer_public": 23.18,
            "ASR_LM_wer_public": 15.21,
            "QbE_mtwv_public": 0.0058 * 100,
            "SF_f1_public": 69.64,
            "SF_cer_public": 52.94,
            "SV_eer_public": 9.56,
            "SD_der_public": 10.05,
            "ST_bleu_public": 2.32,
            "SE_pesq_public": 2.55,
            "SE_stoi_public": 93.6,
            "SS_sisdri_public": 9.2341,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "PASE+",
            "modelURL":"-",
            "modelDesc": "multi-task",
            "stride":10,
            "inputFormat": "waveform",
            "corpus": "LS 50 hr",
            "paramDesc":"-",
            "paramShared": 7.83e6,
            "PR_per_public": 58.87,
            "KS_acc_public": 82.54,
            "IC_acc_public": 29.82,
            "SID_acc_public": 37.99,
            "ER_acc_public": 57.86,
            "ERfold1_acc_public": 58.341014,
            "ERfold2_acc_public": 58.4555208,
            "ERfold3_acc_public": 57.34144,
            "ERfold4_acc_public": 57.22599626,
            "ERfold5_acc_public": 57.9371452,
            "ASR_wer_public": 25.11,
            "ASR_LM_wer_public": 16.62,
            "QbE_mtwv_public": 0.0072 * 100,
            "SF_f1_public": 62.14,
            "SF_cer_public": 60.17,
            "SV_eer_public": 11.61,
            "SD_der_public": 8.68,
            "ST_bleu_public": 3.16,
            "SE_pesq_public": 2.56,
            "SE_stoi_public": 93.9,
            "SS_sisdri_public": 9.87,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "APC",
            "modelURL":"-",
            "modelDesc": "F-G",
            "stride": 10,
            "inputFormat": "FBANK",
            "corpus": "LS 360 hr",
            "paramDesc":"-",
            "paramShared": 4.11e6,
            "PR_per_public": 41.98,
            "KS_acc_public": 91.01,
            "IC_acc_public": 74.69,
            "SID_acc_public": 60.42,
            "ER_acc_public": 59.33,
            "ERfold1_acc_public": 60.83,
            "ERfold2_acc_public": 59.53,
            "ERfold3_acc_public": 58.64,
            "ERfold4_acc_public": 58.97,
            "ERfold5_acc_public": 58.66,
            "ASR_wer_public": 21.28,
            "ASR_LM_wer_public": 14.74,
            "QbE_mtwv_public": 0.031 * 100,
            "SF_f1_public": 70.46,
            "SF_cer_public": 50.89,
            "SV_eer_public": 8.56,
            "SD_der_public": 10.53,
            "ST_bleu_public": 5.95,
            "SE_pesq_public": 2.5567,
            "SE_stoi_public": 93.4,
            "SS_sisdri_public": 8.92,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "VQ-APC",
            "modelURL":"-",
            "modelDesc": "F-G + VQ",
            "stride": 10,
            "inputFormat": "FBANK",
            "corpus": "LS 360 hr",
            "paramDesc":"-",
            "paramShared": 4.63e6,
            "PR_per_public": 41.08,
            "KS_acc_public": 91.11,
            "IC_acc_public": 74.48,
            "SID_acc_public": 60.15,
            "ER_acc_public": 59.66,
            "ERfold1_acc_public": 61.84,
            "ERfold2_acc_public": 56.99,
            "ERfold3_acc_public": 58.47,
            "ERfold4_acc_public": 59.75,
            "ERfold5_acc_public": 61.24,
            "ASR_wer_public": 21.20,
            "ASR_LM_wer_public": 15.21,
            "QbE_mtwv_public": 0.0251 * 100,
            "SF_f1_public": 68.53,
            "SF_cer_public": 52.91,
            "SV_eer_public": 8.72,
            "SD_der_public": 10.45,
            "ST_bleu_public": 4.23,
            "SE_pesq_public": 2.56,
            "SE_stoi_public": 93.4,
            "SS_sisdri_public": 8.44,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "NPC",
            "modelURL":"-",
            "modelDesc": "M-G + VQ",
            "stride": 10,
            "inputFormat": "FBANK",
            "corpus": "LS 360 hr",
            "paramDesc":"-",
            "paramShared": 19.38e6,
            "PR_per_public": 43.81,
            "KS_acc_public": 88.96,
            "IC_acc_public": 69.44,
            "SID_acc_public": 55.92,
            "ER_acc_public": 59.08,
            "ERfold1_acc_public": 59.54,
            "ERfold2_acc_public": 59.63,
            "ERfold3_acc_public": 58.73,
            "ERfold4_acc_public": 59.65,
            "ERfold5_acc_public": 57.86,
            "ASR_wer_public": 20.20,
            "ASR_LM_wer_public": 13.91,
            "QbE_mtwv_public": 0.0246 * 100,
            "SF_f1_public": 72.79,
            "SF_cer_public": 48.44,
            "SV_eer_public": 9.4,
            "SD_der_public": 9.34,
            "ST_bleu_public": 4.32,
            "SE_pesq_public": 2.5211,
            "SE_stoi_public": 93.1,
            "SS_sisdri_public": 8.04,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "Mockingjay",
            "modelURL":"-",
            "modelDesc": "time M-G",
            "stride": 10,
            "inputFormat": "FBANK",
            "corpus": "LS 360 hr",
            "paramDesc":"-",
            "paramShared": 85.12e6,
            "PR_per_public": 70.19,
            "KS_acc_public": 83.67,
            "IC_acc_public": 34.33,
            "SID_acc_public": 32.29,
            "ER_acc_public": 50.28,
            "ERfold1_acc_public": 49.95,
            "ERfold2_acc_public": 48.97,
            "ERfold3_acc_public": 49.87,
            "ERfold4_acc_public": 52.96,
            "ERfold5_acc_public": 49.64,
            "ASR_wer_public": 22.82,
            "ASR_LM_wer_public": 15.48,
            "QbE_mtwv_public": 6.6E-04 * 100,
            "SF_f1_public": 61.59,
            "SF_cer_public": 58.89,
            "SV_eer_public": 11.66,
            "SD_der_public": 10.54,
            "ST_bleu_public": 4.45,
            "SE_pesq_public": 2.5305,
            "SE_stoi_public": 93.4,
            "SS_sisdri_public": 9.29,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "TERA",
            "modelURL":"-",
            "modelDesc": "time/freq M-G",
            "stride": 10,
            "inputFormat": "FBANK",
            "corpus": "LS 960 hr",
            "paramDesc":"-",
            "paramShared": 21.33e6,
            "PR_per_public": 49.17,
            "KS_acc_public": 89.48,
            "IC_acc_public": 58.42,
            "SID_acc_public": 57.57,
            "ER_acc_public": 56.27,
            "ERfold1_acc_public": 56.31,
            "ERfold2_acc_public": 57.77,
            "ERfold3_acc_public": 54.39,
            "ERfold4_acc_public": 56.55,
            "ERfold5_acc_public": 56.33,
            "ASR_wer_public": 18.17,
            "ASR_LM_wer_public": 12.16,
            "QbE_mtwv_public": 0.0013 * 100,
            "SF_f1_public": 67.50,
            "SF_cer_public": 54.17,
            "SV_eer_public": 15.89,
            "SD_der_public": 9.96,
            "ST_bleu_public": 5.24,
            "SE_pesq_public": 2.5422,
            "SE_stoi_public": 93.6,
            "SS_sisdri_public": 10.19,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "modified CPC",
            "modelURL":"-",
            "modelDesc": "F-C",
            "stride": 10,
            "inputFormat": "waveform",
            "corpus": "LL 60k hr",
            "paramDesc":"-",
            "paramShared": 1.84e6,
            "PR_per_public": 42.54,
            "KS_acc_public": 91.88,
            "IC_acc_public": 64.09,
            "SID_acc_public": 39.63,
            "ER_acc_public": 60.96,
            "ERfold1_acc_public": 58.16,
            "ERfold2_acc_public": 62.76,
            "ERfold3_acc_public": 58.12,
            "ERfold4_acc_public": 64.99,
            "ERfold5_acc_public": 60.76,
            "ASR_wer_public": 20.18,
            "ASR_LM_wer_public": 13.53,
            "QbE_mtwv_public": 0.0326 * 100,
            "SF_f1_public": 71.19,
            "SF_cer_public": 49.91,
            "SV_eer_public": 12.86,
            "SD_der_public": 10.38,
            "ST_bleu_public": 4.82,
            "SE_pesq_public": 2.57,
            "SE_stoi_public": 93.7,
            "SS_sisdri_public": 10.4,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "wav2vec",
            "modelURL":"-",
            "modelDesc": "F-C",
            "stride": 10,
            "inputFormat": "waveform",
            "corpus": "LS 960 hr",
            "paramDesc":"-",
            "paramShared": 32.54e6,
            "PR_per_public": 31.58,
            "KS_acc_public": 95.59,
            "IC_acc_public": 84.92,
            "SID_acc_public": 56.56,
            "ER_acc_public": 59.79,
            "ERfold1_acc_public": 59.86,
            "ERfold2_acc_public": 63.25,
            "ERfold3_acc_public": 54.47,
            "ERfold4_acc_public": 59.55,
            "ERfold5_acc_public": 61.88,
            "ASR_wer_public": 15.86,
            "ASR_LM_wer_public": 11.00,
            "QbE_mtwv_public": 0.0485 * 100,
            "SF_f1_public": 76.37,
            "SF_cer_public": 43.71,
            "SV_eer_public": 7.99,
            "SD_der_public": 9.9,
            "ST_bleu_public": 6.61,
            "SE_pesq_public": 2.53,
            "SE_stoi_public": 93.8,
            "SS_sisdri_public": 9.3,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "vq-wav2vec",
            "modelURL":"-",
            "modelDesc": "F-C + VQ",
            "stride": 10,
            "inputFormat": "waveform",
            "corpus": "LS 960 hr",
            "paramDesc":"-",
            "paramShared": 34.15e6,
            "PR_per_public": 33.48,
            "KS_acc_public": 93.38,
            "IC_acc_public": 85.68,
            "SID_acc_public": 38.80,
            "ER_acc_public": 58.24,
            "ERfold1_acc_public": 60.28,
            "ERfold2_acc_public": 59.14,
            "ERfold3_acc_public": 56.13,
            "ERfold4_acc_public": 58.58,
            "ERfold5_acc_public": 57.05,
            "ASR_wer_public": 17.71,
            "ASR_LM_wer_public": 12.80,
            "QbE_mtwv_public": 0.0410 * 100,
            "SF_f1_public": 77.68,
            "SF_cer_public": 41.54,
            "SV_eer_public": 10.38,
            "SD_der_public": 9.93,
            "ST_bleu_public": 5.66,
            "SE_pesq_public": 2.48,
            "SE_stoi_public": 93.6,
            "SS_sisdri_public": 8.16,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "wav2vec 2.0 Base",
            "modelURL":"-",
            "modelDesc": "M-C + VQ",
            "stride": 20,
            "inputFormat": "waveform",
            "corpus": "LS 960 hr",
            "paramDesc":"-",
            "paramShared": 95.04e6,
            "PR_per_public": 5.74,
            "KS_acc_public": 96.23,
            "IC_acc_public": 92.35,
            "SID_acc_public": 75.18,
            "ER_acc_public": 63.43,
            "ERfold1_acc_public": 62.857145,
            "ERfold2_acc_public": 68.621701,
            "ERfold3_acc_public": 60.9904408,
            "ERfold4_acc_public": 63.530552,
            "ERfold5_acc_public": 61.1603558,
            "ASR_wer_public": 6.43,
            "ASR_LM_wer_public": 4.79,
            "QbE_mtwv_public": 0.0233 * 100,
            "SF_f1_public": 88.30,
            "SF_cer_public": 24.77,
            "SV_eer_public": 6.02,
            "SD_der_public": 6.08,
            "ST_bleu_public": 14.81,
            "SE_pesq_public": 2.55,
            "SE_stoi_public": 93.9,
            "SS_sisdri_public": 9.77,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "wav2vec 2.0 Large",
            "modelURL":"-",
            "modelDesc": "M-C + VQ",
            "stride": 20,
            "inputFormat": "waveform",
            "corpus": "LL 60k hr",
            "paramDesc":"-",
            "paramShared": 317.38e6,
            "PR_per_public": 4.75,
            "KS_acc_public": 96.66,
            "IC_acc_public": 95.28,
            "SID_acc_public": 86.14,
            "ER_acc_public": 65.64,
            "ERfold1_acc_public": 65.253454,
            "ERfold2_acc_public": 64.516127,
            "ERfold3_acc_public": 65.5951321,
            "ERfold4_acc_public": 66.53734445,
            "ERfold5_acc_public": 66.317486,
            "ASR_wer_public": 3.75,
            "ASR_LM_wer_public": 3.10,
            "QbE_mtwv_public": 0.0489 * 100,
            "SF_f1_public": 87.11,
            "SF_cer_public": 27.31,
            "SV_eer_public": 5.65,
            "SD_der_public": 5.62,
            "ST_bleu_public": 14.07,
            "SE_pesq_public": 2.52,
            "SE_stoi_public": 94,
            "SS_sisdri_public": 10.02,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "HuBERT Base",
            "modelURL":"-",
            "modelDesc": "M-P + VQ",
            "stride": 20,
            "inputFormat": "waveform",
            "corpus": "LS 960 hr",
            "paramDesc":"-",
            "paramShared": 94.68e6,
            "PR_per_public": 5.41,
            "KS_acc_public": 96.30,
            "IC_acc_public": 98.34,
            "SID_acc_public": 81.42,
            "ER_acc_public": 64.92,
            "ERfold1_acc_public": 62.39631,
            "ERfold2_acc_public": 66.568917,
            "ERfold3_acc_public": 65.24761,
            "ERfold4_acc_public": 65.179437,
            "ERfold5_acc_public": 65.18936,
            "ASR_wer_public": 6.42,
            "ASR_LM_wer_public": 4.79,
            "QbE_mtwv_public": 0.0736 * 100,
            "SF_f1_public": 88.53,
            "SF_cer_public": 25.20,
            "SV_eer_public": 5.11,
            "SD_der_public": 5.88,
            "ST_bleu_public": 15.53,
            "SE_pesq_public": 2.58,
            "SE_stoi_public": 93.90,
            "SS_sisdri_public": 9.36,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "HuBERT Large",
            "modelURL":"-",
            "modelDesc": "M-P + VQ",
            "stride": 20,
            "inputFormat": "waveform",
            "corpus": "LL 60k hr",
            "paramDesc":"-",
            "paramShared": 316.61e6,
            "PR_per_public": 3.53,
            "KS_acc_public": 95.29,
            "IC_acc_public": 98.76,
            "SID_acc_public": 90.33,
            "ER_acc_public": 67.62,
            "ERfold1_acc_public": 67.18894,
            "ERfold2_acc_public": 69.30596,
            "ERfold3_acc_public": 67.85404,
            "ERfold4_acc_public": 67.022305,
            "ERfold5_acc_public": 66.72038436,
            "ASR_wer_public": 3.62,
            "ASR_LM_wer_public": 2.94,
            "QbE_mtwv_public": 0.0353 * 100,
            "SF_f1_public": 89.81,
            "SF_cer_public": 21.76,
            "SV_eer_public": 5.98,
            "SD_der_public": 5.75,
            "ST_bleu_public": 20.01,
            "SE_pesq_public": 2.64,
            "SE_stoi_public": 94.2,
            "SS_sisdri_public": 10.45,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "DeCoAR 2.0",
            "modelURL":"-",
            "modelDesc": "M-G + VQ",
            "stride": 10,
            "inputFormat": "FBANK",
            "corpus": "LS 960 hr",
            "paramDesc":"-",
            "paramShared": 89.84e6,
            "PR_per_public": 14.93,
            "KS_acc_public": 94.48,
            "IC_acc_public": 90.80,
            "SID_acc_public": 74.42,
            "ER_acc_public": 62.47,
            "ERfold1_acc_public": 60.73732,
            "ERfold2_acc_public": 66.6666686,
            "ERfold3_acc_public": 62.55429,
            "ERfold4_acc_public": 62.4636292,
            "ERfold5_acc_public": 59.951651,
            "ASR_wer_public": 13.02,
            "ASR_LM_wer_public": 9.07,
            "QbE_mtwv_public": 0.0406 * 100,
            "SF_f1_public": 83.28,
            "SF_cer_public": 34.73,
            "SV_eer_public": 7.16,
            "SD_der_public": 6.59,
            "ST_bleu_public": 9.94,
            "SE_pesq_public": 2.47,
            "SE_stoi_public": 93.2,
            "SS_sisdri_public": 8.54,
        },
    ]
    return data

def get_hidden_leaderboard_default():
    data = [
        {
            "name":"paper",
            "aoeTimeUpload":"-",
            "task":"CONSTRAINED",
            "submitName": "distilHuBERT",
            "modelDesc": "-",
            "huggingfaceOrganizationName":"-",
            "huggingfaceRepoName": "-",
            "huggingfaceCommonHash": "-",
            "paramShared": 23.49e6,
            "PR_per_hidden_dev": 33.2599294261229,
            "SID_acc_hidden_dev": 75.4166662693023,
            "ER_acc_hidden_dev": 66.0273969173431,
            "ASR_wer_hidden_dev": 47.9182944525058,
            "QbE_map_hidden_dev": 46.7392504215240,
            "QbE_eer_hidden_dev": 19.4287180900573,
            "SV_eer_hidden_dev": 16.2837000000000,
            "SD_der_hidden_dev": 11.7146380245685,
            "ST_bleu_hidden_dev": 14.2200000000000,
            "SS_sisdri_hidden_dev": 6.7019136153688,
            "SE_stoi_hidden_dev": 84.5362458826972,
            "SE_pesq_hidden_dev": 1.5291748084665,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"-",
            "task":"CONSTRAINED",
            "submitName": "fbank",
            "modelDesc": "-",
            "huggingfaceOrganizationName":"-",
            "huggingfaceRepoName": "-",
            "huggingfaceCommonHash": "-",
            "paramShared": 0,
            "PR_per_hidden_dev": 81.0007694144490,
            "SID_acc_hidden_dev": 49.5833337306976,
            "ER_acc_hidden_dev": 47.1232891082763,
            "ASR_wer_hidden_dev": 73.5600000000000,
            "QbE_map_hidden_dev": 18.6019480228424,
            "QbE_eer_hidden_dev": 36.9490325450897,
            "SV_eer_hidden_dev": 25.5671000000000,
            "SD_der_hidden_dev": 15.7551825046539,
            "ST_bleu_hidden_dev": 3.2000000000000,
            "SS_sisdri_hidden_dev": 4.6555920745159,
            "SE_stoi_hidden_dev": 84.3318867671110,
            "SE_pesq_hidden_dev": 1.5100356920995,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "TERA",
            "modelURL":"-",
            "modelDesc": "time/freq M-G",
            "stride": 10,
            "inputFormat": "FBANK",
            "corpus": "LS 960 hr",
            "paramDesc":"-",
            "paramShared": 21.33e6,
            "PR_per_hidden_dev": 69.4117959194502,
            "SID_acc_hidden_dev": 72.9166686534881,
            "ER_acc_hidden_dev": 52.6027381420135,
            "ASR_wer_hidden_dev": 81.9400000000000,
            "QbE_map_hidden_dev": 14.8605868220329,
            "QbE_eer_hidden_dev": 35.0725859403610,
            "SV_eer_hidden_dev": 19.4055000000000,
            "SD_der_hidden_dev": 13.3535549044609,
            "ST_bleu_hidden_dev": 7.1100000000000,
            "SS_sisdri_hidden_dev": 6.3054000000000,
            "SE_stoi_hidden_dev": 85.0100000000000,
            "SE_pesq_hidden_dev": 1.5494000000000,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "wav2vec 2.0 Base",
            "modelURL":"-",
            "modelDesc": "M-C + VQ",
            "stride": 20,
            "inputFormat": "waveform",
            "corpus": "LS 960 hr",
            "paramDesc":"-",
            "paramShared": 95.04e6,
            "PR_per_hidden_dev": 22.5491496643761,
            "SID_acc_hidden_dev": 73.9166676998138,
            "ER_acc_hidden_dev": 61.0958933830261,
            "ASR_wer_hidden_dev": 38.1700000000000,
            "QbE_map_hidden_dev": 38.3381754159927,
            "QbE_eer_hidden_dev": 25.4089444875717,
            "SV_eer_hidden_dev": 17.3809000000000,
            "SD_der_hidden_dev": 11.9850382208824,
            "ST_bleu_hidden_dev": 18.3900000000000,
            "SS_sisdri_hidden_dev": 7.2907000000000,
            "SE_stoi_hidden_dev": 84.2200000000000,
            "SE_pesq_hidden_dev": 1.5284000000000,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "wav2vec 2.0 Large",
            "modelURL":"-",
            "modelDesc": "M-C + VQ",
            "stride": 20,
            "inputFormat": "waveform",
            "corpus": "LL 60k hr",
            "paramDesc":"-",
            "paramShared": 317.38e6,
            "PR_per_hidden_dev": 20.5539784033323,
            "SID_acc_hidden_dev": 79.8333346843719,
            "ER_acc_hidden_dev": 67.9452061653137,
            "ASR_wer_hidden_dev": 22.9798402859217,
            "QbE_map_hidden_dev": 43.0485993623733,
            "QbE_eer_hidden_dev": 20.4211279749870,
            "SV_eer_hidden_dev": 13.7470000000000,
            "SD_der_hidden_dev": 12.4591387808322,
            "ST_bleu_hidden_dev": 15.4100000000000,
            "SS_sisdri_hidden_dev": 4.6616677106810,
            "SE_stoi_hidden_dev": 83.8519392119655,
            "SE_pesq_hidden_dev": 1.4808455588838,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "HuBERT Base",
            "modelURL":"-",
            "modelDesc": "M-P + VQ",
            "stride": 20,
            "inputFormat": "waveform",
            "corpus": "LS 960 hr",
            "paramDesc":"-",
            "paramShared": 94.68e6,
            "PR_per_hidden_dev": 17.1725345573213,
            "SID_acc_hidden_dev": 72.0833361148834,
            "ER_acc_hidden_dev": 60.2739751338958,
            "ASR_wer_hidden_dev": 28.5500000000000,
            "QbE_map_hidden_dev": 51.0858535766601,
            "QbE_eer_hidden_dev": 17.8043216466903,
            "SV_eer_hidden_dev": 17.8800000000000,
            "SD_der_hidden_dev": 11.1848652362823,
            "ST_bleu_hidden_dev": 19.2700000000000,
            "SS_sisdri_hidden_dev": 7.3866000000000,
            "SE_stoi_hidden_dev": 84.7000000000000,
            "SE_pesq_hidden_dev": 1.5432000000000,
        },
        {
            "name":"strong baseline",
            "aoeTimeUpload":"-",
            "task":"CONSTRAINED",
            "submitName": "HuBERT Large",
            "modelDesc": "M-P + VQ",
            "huggingfaceOrganizationName":"-",
            "huggingfaceRepoName": "-",
            "huggingfaceCommonHash": "-",
            "paramShared": 316.61e6,
            "PR_per_hidden_dev": 16.32352551,
            "SID_acc_hidden_dev": 78.75000238,
            "ER_acc_hidden_dev": 65.4794514179229,
            "ASR_wer_hidden_dev": 21.4941824862216,
            "SV_eer_hidden_dev": 12.7294,
            "SD_der_hidden_dev": 10.48149392,
            "QbE_map_hidden_dev": 32.09455907,
            "QbE_eer_hidden_dev": 29.38648462,
            "ST_bleu_hidden_dev": 23.33,
            "SS_sisdri_hidden_dev": 8.082589958,
            "SE_pesq_hidden_dev": 1.567159144,
            "SE_stoi_hidden_dev": 85.20344653,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "modified CPC",
            "modelURL":"-",
            "modelDesc": "F-C",
            "stride": 10,
            "inputFormat": "waveform",
            "corpus": "LL 60k hr",
            "paramDesc":"-",
            "paramShared": 1.84e6,
            "PR_per_hidden_dev": 62.2244037038019,
            "SID_acc_hidden_dev": 68.4166669845581,
            "ER_acc_hidden_dev": 50.4109561443328,
            "ASR_wer_hidden_dev": 65.9400000000000,
            "QbE_map_hidden_dev": 36.8827581405639,
            "QbE_eer_hidden_dev": 24.5341509580612,
            "SV_eer_hidden_dev": 17.7121000000000,
            "SD_der_hidden_dev": 13.9006122946739,
            "ST_bleu_hidden_dev": 6.6000000000000,
            "SS_sisdri_hidden_dev": 4.2073171339110,
            "SE_stoi_hidden_dev": 83.7639588044780,
            "SE_pesq_hidden_dev": 1.5082369434730,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "APC",
            "modelURL":"-",
            "modelDesc": "F-G",
            "stride": 10,
            "inputFormat": "FBANK",
            "corpus": "LS 360 hr",
            "paramDesc":"-",
            "paramShared": 4.11e6,
            "PR_per_hidden_dev": 62.8571807593324,
            "SID_acc_hidden_dev": 61.4166676998138,
            "ER_acc_hidden_dev": 56.1643838882446,
            "ASR_wer_hidden_dev": 66.3821972561305,
            "QbE_map_hidden_dev": 28.5406559705734,
            "QbE_eer_hidden_dev": 28.5590171813964,
            "SV_eer_hidden_dev": 22.9366000000000,
            "SD_der_hidden_dev": 14.6572947502136,
            "ST_bleu_hidden_dev": 5.9500000000000,
            "SS_sisdri_hidden_dev": 4.6428000000000,
            "SE_stoi_hidden_dev": 84.2500000000000,
            "SE_pesq_hidden_dev": 1.5205000000000,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"Interspeech2021",
            "task":"CONSTRAINED",
            "submitName": "PASE+",
            "modelURL":"-",
            "modelDesc": "multi-task",
            "stride":10,
            "inputFormat": "waveform",
            "corpus": "LS 50 hr",
            "paramDesc":"-",
            "paramShared": 7.83e6,
            "PR_per_hidden_dev": 76.1401926189275,
            "SID_acc_hidden_dev": 82.6666653156280,
            "ER_acc_hidden_dev": 58.6301386356353,
            "ASR_wer_hidden_dev": 74.8908668291853,
            "QbE_map_hidden_dev": 14.4156306982040,
            "QbE_eer_hidden_dev": 34.8629355430603,
            "SV_eer_hidden_dev": 13.7288090999557,
            "SD_der_hidden_dev": 15.9957945346832,
            "ST_bleu_hidden_dev": 4.1100000000000,
            "SS_sisdri_hidden_dev": 4.8657000000000,
            "SE_stoi_hidden_dev": 84.6100000000000,
            "SE_pesq_hidden_dev": 1.5286000000000,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"-",
            "task":"CONSTRAINED",
            "submitName": "WavLM Base",
            "modelDesc": "-",
            "huggingfaceOrganizationName":"-",
            "huggingfaceRepoName": "-",
            "huggingfaceCommonHash": "-",
            "paramShared": 94.7e6,
            "PR_per_hidden_dev": 16.9748746385078,
            "SID_acc_hidden_dev": 69.3333327770233,
            "ER_acc_hidden_dev": 55.8904111385345,
            "ASR_wer_hidden_dev": 26.8284500111831,
            "QbE_map_hidden_dev": 58.9959025382995,
            "QbE_eer_hidden_dev": 16.1135792732238,
            "SV_eer_hidden_dev": 17.4611701147429,
            "SD_der_hidden_dev": 10.6141008436679,
            "ST_bleu_hidden_dev": 20.1800000000000,
            "SS_sisdri_hidden_dev": 9.9701000000000,
            "SE_stoi_hidden_dev": 85.1400000000000,
            "SE_pesq_hidden_dev": 1.5683000000000,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"-",
            "task":"CONSTRAINED",
            "submitName": "WavLM Base+",
            "modelDesc": "-",
            "huggingfaceOrganizationName":"-",
            "huggingfaceRepoName": "-",
            "huggingfaceCommonHash": "-",
            "paramShared": 94.7e6,
            "PR_per_hidden_dev": 13.7804780982197,
            "SID_acc_hidden_dev": 81.4999997615814,
            "ER_acc_hidden_dev": 59.7260296344757,
            "ASR_wer_hidden_dev": 23.2855221873599,
            "QbE_map_hidden_dev": 57.7453553676605,
            "QbE_eer_hidden_dev": 16.3951680064201,
            "SV_eer_hidden_dev": 14.9169465808559,
            "SD_der_hidden_dev": 10.0567698478698,
            "ST_bleu_hidden_dev": 23.0700000000000,
            "SS_sisdri_hidden_dev": 10.0709000000000,
            "SE_stoi_hidden_dev": 85.4500000000000,
            "SE_pesq_hidden_dev": 1.5751000000000,
        },
        {
            "name":"paper",
            "aoeTimeUpload":"-",
            "task":"CONSTRAINED",
            "submitName": "WavLM Large",
            "modelDesc": "-",
            "huggingfaceOrganizationName":"-",
            "huggingfaceRepoName": "-",
            "huggingfaceCommonHash": "-",
            "paramShared": 316.62e6,
            "PR_per_hidden_dev": 15.4333925870897,
            "SID_acc_hidden_dev": 92.5833344459533,
            "ER_acc_hidden_dev": 66.3013696670532,
            "ASR_wer_hidden_dev": 18.4824902723735,
            "QbE_map_hidden_dev": 51.1736690998077,
            "QbE_eer_hidden_dev": 17.6742762327194,
            "SV_eer_hidden_dev": 10.8291017309497,
            "SD_der_hidden_dev": 9.6898011863232,
            "ST_bleu_hidden_dev": 26.1000000000000,
            "SS_sisdri_hidden_dev": 10.4721000000000,
            "SE_stoi_hidden_dev": 85.0900000000000,
            "SE_pesq_hidden_dev": 1.5875000000000,
        },
        # {
        #     "name":"paper",
        #     "aoeTimeUpload":"Interspeech2021",
        #     "task":"CONSTRAINED",
        #     "submitName": "VQ-APC",
        #     "modelURL":"-",
        #     "modelDesc": "F-G + VQ",
        #     "stride": 10,
        #     "inputFormat": "FBANK",
        #     "corpus": "LS 360 hr",
        #     "paramDesc":"-",
        #     "paramShared": 4.63e6,
        # },
        # {
        #     "name":"paper",
        #     "aoeTimeUpload":"Interspeech2021",
        #     "task":"CONSTRAINED",
        #     "submitName": "NPC",
        #     "modelURL":"-",
        #     "modelDesc": "M-G + VQ",
        #     "stride": 10,
        #     "inputFormat": "FBANK",
        #     "corpus": "LS 360 hr",
        #     "paramDesc":"-",
        #     "paramShared": 19.38e6,
        # },
        # {
        #     "name":"paper",
        #     "aoeTimeUpload":"Interspeech2021",
        #     "task":"CONSTRAINED",
        #     "submitName": "Mockingjay",
        #     "modelURL":"-",
        #     "modelDesc": "time M-G",
        #     "stride": 10,
        #     "inputFormat": "FBANK",
        #     "corpus": "LS 360 hr",
        #     "paramDesc":"-",
        #     "paramShared": 85.12e6,
        # },
        # {
        #     "name":"paper",
        #     "aoeTimeUpload":"Interspeech2021",
        #     "task":"CONSTRAINED",
        #     "submitName": "wav2vec",
        #     "modelURL":"-",
        #     "modelDesc": "F-C",
        #     "stride": 10,
        #     "inputFormat": "waveform",
        #     "corpus": "LS 960 hr",
        #     "paramDesc":"-",
        #     "paramShared": 32.54e6,
        # },
        # {
        #     "name":"paper",
        #     "aoeTimeUpload":"Interspeech2021",
        #     "task":"CONSTRAINED",
        #     "submitName": "vq-wav2vec",
        #     "modelURL":"-",
        #     "modelDesc": "F-C + VQ",
        #     "stride": 10,
        #     "inputFormat": "waveform",
        #     "corpus": "LS 960 hr",
        #     "paramDesc":"-",
        #     "paramShared": 34.15e6,
        # },
    ]
    return data