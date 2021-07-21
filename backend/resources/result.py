from flask_restx import Resource
from flask import request, jsonify, make_response, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from threading import Thread
from http import HTTPStatus

from models.file import FileModel, Task, Show
from models.score import ScoreModel
from models.user import UserModel
from schemas.submission import SubmissionSchema
from utils import submission_records_parser, get_AOE_month, get_AOE_today,  get_leaderboard_default
from calculate import metric_calculate_pipeline
from config import configs
import file_upload

formSchema = SubmissionSchema()


class Result(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        '''Get User submission info'''
        try:
            user_mail = get_jwt_identity()
            submission_records = FileModel.find_by_email(email=user_mail).all()
            submission_info = submission_records_parser(
                submission_records, configs, mode="individual")
            print(submission_info)
            return make_response(jsonify({"submission_info": submission_info}), HTTPStatus.OK)
        except Exception as e:
            return {"message": "Internal Server Error!"}, HTTPStatus.INTERNAL_SERVER_ERROR

    @classmethod
    @jwt_required()
    def post(cls):
        '''Upload user submission'''
        try:
            user_mail = get_jwt_identity()

            # check current submission counts
            daily_counts = FileModel.get_interval_upload_count_by_mail(
                email=user_mail, AOEtime=get_AOE_today(to_str=False))
            monthly_counts = FileModel.get_interval_upload_count_by_mail(
                email=user_mail, AOEtime=get_AOE_month(to_str=False))
            if (daily_counts >= configs["DAILY_SUBMIT_LIMIT"]) or (monthly_counts >= configs["MONTHLY_SUBMIT_LIMIT"]):
                return {"message": f"You have submitted {daily_counts} times today and {monthly_counts} times this month."}, HTTPStatus.FORBIDDEN

            # file validation
            file = request.files['file']

            if file.filename == "":
                return {"message": "No file selected."}, HTTPStatus.FORBIDDEN
            if not file_upload.zipfile_check(file):
                return {"message": "Wrong file format."}, HTTPStatus.FORBIDDEN

            # load form data
            formData = formSchema.load(request.form)

            # get file path
            upload_count = FileModel.get_upload_count_by_mail(
                email=user_mail) + 1
            folder = file_upload.create_folder(user_mail, str(upload_count))
            file_path = file_upload.get_full_path(folder, file.filename)

            # add column for db
            formData.update({"email": user_mail, "filePath": file_path})

            fileObj = FileModel(**formData)
            scoreObj = ScoreModel()
            fileObj.scores.append(scoreObj)
            fileObj.save_to_db()
            try:
                file.save(file_path)

                # start processing
                thread = Thread(target=metric_calculate_pipeline, kwargs={"file_path": file_path,
                                                                          "submitUUID": formData["submitUUID"]})
                thread.start()

                return {"message": "Upload Success!"}, HTTPStatus.OK
            except Exception as e:
                fileObj.delete_from_db()  # Rollback
                return {"message": "Internal Server Error!"}, HTTPStatus.INTERNAL_SERVER_ERROR
        except ValidationError as e:
            return {"message": "There's something worng with your input!"}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            print(e)
            return {"message": "Internal Server Error!"}, HTTPStatus.INTERNAL_SERVER_ERROR

    @classmethod
    @jwt_required()
    def patch(cls):
        '''Change user submission show on leaderboard or not'''
        try:
            user_mail = get_jwt_identity()
            data = request.get_json()

            submitID = data["submission_id"]
            submission_record = FileModel.find_by_submitID(submitUUID=submitID)

            assert submission_record.email == user_mail
            task_id = submission_record.task.value  # == mapping[task]

            if submission_record.showOnLeaderboard == Show.YES:
                # set the "show" of all the same task submission to "NO"
                FileModel.reset_same_task_show_attribute(
                    email=user_mail, task=Task(task_id))
                return {"message": "Remove from the leaderboard!", "submitID": submitID}, HTTPStatus.OK

            else:
                # set the "show" of all the same task submission to "NO"
                FileModel.reset_same_task_show_attribute(
                    email=user_mail, task=Task(task_id))
                FileModel.set_show_attribute_by_submitID(submitUUID=submitID)
                return {"message": "Shown on the leaderboard!", "submitID": submitID}, HTTPStatus.OK

        except Exception as e:
            print(e)
            return {"message": "Internal Server Error!"}, HTTPStatus.INTERNAL_SERVER_ERROR

class OwnUpload(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        '''Download previous upload file'''
        try:
            user_mail = get_jwt_identity()
            data = request.get_json()

            submitID = data["submission_id"]
            submission_record = FileModel.find_by_submitID(submitUUID=submitID)
            assert submission_record.email == user_mail
            download_path = submission_record.filePath 

            return send_file(download_path, as_attachment=True)
        except Exception as e:
            print(e)
            return {"message": "Internal Server Error!"}, HTTPStatus.INTERNAL_SERVER_ERROR


class LeaderBoard(Resource):
    @classmethod
    def get(cls):
        '''Get leaderboard data'''
        try:
            leaderboard_default_data = get_leaderboard_default()
            leaderboard_user_data = FileModel.find_show_on_leaderboard()
            submission_names = []
            for user_data in leaderboard_user_data:
                submission_names.append(
                    UserModel.find_by_email(email=user_data.email).name)
            submission_info = submission_records_parser(
                leaderboard_user_data, configs, mode="leaderboard")

            for single_info, name in zip(submission_info, submission_names):
                single_info.update({"name": name})

            leaderboard_default_data += submission_info

            return {"leaderboard": leaderboard_default_data}, HTTPStatus.OK

        except Exception as e:
            print(e)
            return {"message": "Something went wrong!"}, HTTPStatus.INTERNAL_SERVER_ERROR
