import json
import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "codegen")))

from flask_restplus import Resource
from CodeGen import CodeGenerator
from . import api

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
        codeGen = CodeGenerator()
        level = int(level_id)/5.0
        codeGen.setDifficultyLevel(level)
        codeGen.setConceptArray([stage_id])

        results = []
        for i in range(10):
            results.append({ "text": "<br>".join(codeGen.generateCode()) , "answer" : 1 })

        return results
