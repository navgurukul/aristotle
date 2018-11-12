from flask_restplus import Resource

from backend.src import api

@api.route("/stages")
class StagesList(Resource):

    def get(self):
        return {'data': 'list of stages'}


@api.route("/stages/<stage_id>/level")
def LevelsList(Resource):

    def get(self, stage_id):
        return {'data': 'list of levels of given stage'}


@api.route("/stages/<stage_id>/level/<level_id>/random_questions")
def LevelRandomQuestionList(Resource):

    def get(self, stage_id, level_id):
        return {'data': 'list of random questions of given level'}
