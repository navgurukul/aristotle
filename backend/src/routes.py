from flask_restplus import Resource

from backend.src import api

@api.route("/stages")
class StagesList(Resource):

    def get(self):
        return {'data': 'list of stages'}
