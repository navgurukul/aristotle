import json

from flask_restplus import Resource

from backend.src import api

@api.route("/stages")
class StagesList(Resource):

    def get(self):
        # read the list of stages from the JSON
        stages_file = open("data/stages.json")
        stages = json.loads(stages_file.read())
        stages = stages['stages']
        return {'data': stages}

@api.route("/stages/<stage_id>")
class Stage(Resource):

    def get(self, stage_id):
        # read the list of stages from JSON
        stages_file = open("data/stages.json")
        stages = json.loads(stages_file.read())
        stages = stages['stages']

        # search for the stage & return
        searchedStages = list(filter(lambda s: s['id'] == stage_id, stages))
        if len(searchedStages) == 0:
            return {'message': "Stage not found."}, 404
        else:
            return {'stage': searchedStages[0]}

@api.route("/stages/<stage_id>/level/<level_id>/random_questions")
class LevelRandomQuestionList(Resource):

    def get(self, stage_id, level_id):
        #TODO: @Abhishek/@Shivam: Yahan on basis of stage and level a random list of 10 questions needs to be generated
        #TODO: The stages are listed in `data/stages.json`. You can edit the stages and number of levels per stage from there.
        questions_file = open("data/questions.json")
        questions = json.loads(questions_file.read())
        questions = questions['questions']

        return questions
