import random
from sys import getrecursionlimit, setrecursionlimit
from functools import reduce

setrecursionlimit(100)
# TODO need to work on the glevel
# TODO need to work on the difficulty level

class CodeGenerator:
    ARITHMETIC_OPERATORS = ["+", "-", "*", "/"]
    MODULUS_OPERATOR = "%"
    CONDITIONAL_OPERATORS = ["==", "!=", "<", ">", ">=", "<="]
    BOOLEAN_VALUES = ["True", "False"]
    VARIABLES_ARRAY = ["caboVerde", "costaRica", "dominicanRepublic", "elSalvador", "guineaBissau",
                        "holySee", "koreaSouth", "newZealand", "palestinianTerritories", "sanMarino", 
                        "solomonIslands", "sriLanka", "timorLeste", "unitedKingdom", "southSudan"]
    INDEX_VARIABLES_NAMES = ["ctr", "index", "i", "n"]

    CONCEPT_ARRAYS = []

    variable_map = []
    difficulty_level = 1

    def __init__(self):
        self.CONCEPT_ARRAYS = [ "PRINT", \
                    "INTEGER", "FLOAT", "STRING", "BOOLEAN",  "LIST", \
                    "CONDITION", \
                    "ARITHMETIC_OPERATORS", "MODULUS_OPERATOR", "CONDITIONAL_OPERATOR", \
                    "BRACKET", "AND", "OR", "NOT", \
                    "VARIABLE", "WHILE", \
                    "IF", "IFELSE", "IFELIFSE" ]
        self.sanitiseConceptArrays()

    def sanitiseConceptArrays(self):
        data = [
            {
                "ifThere": ["WHILE"],
                "shouldBeThere": ["CONDITIONAL_OPERATOR", "IF"]
            }, {
                "ifThere": ["IF"],
                "shouldBeThere": ["CONDITIONAL_OPERATOR"]
            }, {
                "ifThere": ["ARITHMETIC_OPERATORS"],
                "shouldBeThere": ["NUMBER"]
            }, {
                "ifThere": ["INTEGER", "FLOAT"],
                "shouldBeThere": ["NUMBER"]
            }, {
                "ifThere": ["CONDITIONAL_OPERATOR", "CONDITION"],
                "shouldBeThere": ["CONDITION", "NUMBER", "BOOLEAN", "BRACKET"]
            }, {
                "ifThere": ["NUMBER"],
                "shouldBeThere": ["FLOAT", "INTEGER"]
            }, {
                "ifThere": ["BOOLEAN_OPERATORS"],
                "shouldBeThere": ["AND", "OR", "NOT", "BOOLEAN", "CONDITION", "BRACKET"]
            }
        ]
        for d in data:
            for m in d["ifThere"]:
                if m in self.CONCEPT_ARRAYS:
                    for n in d["shouldBeThere"]:
                        if n not in self.CONCEPT_ARRAYS:
                            self.CONCEPT_ARRAYS.append(n)
        
        if "VARIABLE" not in self.CONCEPT_ARRAYS:
            self.CONCEPT_ARRAYS.append("VARIABLE")

        if "PRINT" not in self.CONCEPT_ARRAYS:
            self.CONCEPT_ARRAYS.append("PRINT")

    def setConceptArray(self, concept_array):
        self.CONCEPT_ARRAYS = concept_array
        self.sanitiseConceptArrays()
        print(self.CONCEPT_ARRAYS)

    def setDifficultyLevel(self, level=1):
        self.difficulty_level = level

    def makeBoolean(self):
        return random.choice(self.BOOLEAN_VALUES)

    def makeString(self):
        return '"' + random.choice(self.VARIABLES_ARRAY) + '"'

    def selectWeightedRandom(self, container, weights):
        total_weight = float(sum(weights))
        rel_weight = [w / total_weight for w in weights]

        # Probability for each element
        probs = [sum(rel_weight[:i + 1]) for i in range(len(rel_weight))]

        slot = random.random()*1
        for (i, element) in enumerate(container):
            if slot <= probs[i]:
                break

        return element


    def prepareForWeightedSelection(self, selectionList):
        cases = []
        weights = []
        for obj in selectionList:
            cases.append(obj['name'])
            weights.append(obj['weight'])

        return self.selectWeightedRandom(cases, weights)

    def validCases(self, cases):
        ncases = []

        for case in cases:
            if "concept" in case.keys():
                if case['concept'] in self.CONCEPT_ARRAYS:
                    ncases.append(case)

            if case['name'] in self.CONCEPT_ARRAYS:
                ncases.append(case)
        
        return ncases

    def makeList(self, level=3, casesWithWeights = [{"name": "NUMBER", "weight": 3},
                            {"name": "STRING", "weight": 2},
                            {"name": "BOOLEAN", "weight": 1}]):

        if self.difficulty_level > 0.5:
            casesWithWeights.append({"name": 'LIST', "weight": 2})
            
        casesWithWeights = self.validCases(casesWithWeights)

        rcase = self.prepareForWeightedSelection(casesWithWeights)

        new_case = '['
        num_elements = int(random.random()*5+0.7)

        if num_elements == 0:
            return "[]"

        for i in range(num_elements):
            if rcase == 'NUMBER':
                new_case = new_case + self.makeNumber() + ', '
            elif rcase == 'STRING':
                new_case = new_case + self.makeString() + ', '
            elif rcase == 'BOOLEAN':
                bool_val = str(self.makeBoolean())
                new_case = new_case + bool_val + ', '
            elif rcase == 'LIST':
                newCasesWithWeights = []
                for i in casesWithWeights:
                    if i['name'] != "LIST":
                        newCasesWithWeights.append(i)

                list_type = self.prepareForWeightedSelection(newCasesWithWeights)
                new_case = new_case + self.makeList(level=level-2, casesWithWeights=[{"name": list_type, "weight": 1}]) + ', '
                # ast.literal_eval(makeList(level=level-2)) + ', '

        new_case = new_case[:-2]
        new_case += ']'
        return new_case

    def makeConstant(self, level=2):
        casesWithWeights = [{"name": "NUMBER", "weight": 3},
                            {"name": "STRING", "weight": 2},
                            {"name": "BOOLEAN", "weight": 1}]
        
        if self.difficulty_level > 0.4:
            casesWithWeights.append({"name": "LIST", "weight": 2})

        casesWithWeights = self.validCases(casesWithWeights)

        rcase = self.prepareForWeightedSelection(casesWithWeights)

        if rcase == 'NUMBER':
            new_case = self.makeNumber()
        elif rcase == 'STRING':
            new_case = self.makeString()
        elif rcase == 'BOOLEAN':
            bool_val = str(self.makeBoolean())
            new_case = bool_val
        elif rcase == 'LIST':
            new_case = self.makeList(2)

        return new_case

    def makeVarAssignment(self):
        # BREAK NUMBER CASE INTO INTEGER AND FLOAT
        # USE VARIABLE PROPERLY AGAIN AND AGAIN IN THE CODE 
        casesWithWeights = [{"name": ["VARNAME", "=", 'NUMBER'], "weight": 4, "concept": "NUMBER"},
                            {"name": ["VARNAME", "=", 'STRING'], "weight": 2, "concept": "STRING"},
                            {"name": ["VARNAME", "=", 'BOOLEAN'], "weight": 1, "concept": "BOOLEAN"}]
        
        if self.difficulty_level > 0.2:
            casesWithWeights.append({"name": ["VARNAME", "=", 'LIST'], "weight": 1, "concept": "LIST"})
        
        elif self.difficulty_level > 0.4:
            casesWithWeights.append({"name": ["VARNAME", "=", 'CONDITION'], "weight": 2, "concept": "CONDITION"})

        casesWithWeights = self.validCases(casesWithWeights)
        rcase = self.prepareForWeightedSelection(casesWithWeights)

        new_case = ""

        for keyword in rcase:
            if keyword == "VARNAME":
                var_name = random.choice(self.VARIABLES_ARRAY)
                new_case += var_name
                dic = {"name": var_name, "type": rcase[2]}  # MAKE THIS GENERIC
                self.variable_map.append(dic)

            elif keyword == "NUMBER":
                new_case += self.makeNumber()
            elif keyword == "BOOLEAN":
                new_case += self.makeBoolean()
            elif keyword == "STRING":
                new_case += self.makeString()
            elif keyword == "LIST":
                new_case += self.makeList()
            elif keyword == "CONDITION":
                new_case += self.makeCondition()
            else:
                new_case += keyword
            new_case += " "

        return new_case

    def makePrintStatement(self):
        if (len(self.variable_map)):
            return "print " + random.choice(self.variable_map)["name"]
        return "print " + self.makeConstant()

    def makeStatement(self):
        casesWithWeights = [{"name": 'CONDITION', "weight": 3},
                            # {"name": 'NUMBER', "weight": 1},
                            {"name": 'VARIABLE', "weight": 2, "concept": "VARIABLE"},
                            {"name": 'IF', "weight": 2, "concept": "IF"},
                            {"name": 'WHILE', "weight": 4},
                            {"name": "PRINT", "weight": 5, "concept": "PRINT" }]

        casesWithWeights = self.validCases(casesWithWeights)
        rcase = self.prepareForWeightedSelection(casesWithWeights)

        new_case = ""

        # TODO SHIFT SUCH IFS TO SWITCH STATEMENTS
        if rcase == "CONDITION":
            new_case += self.makeCondition()
        elif rcase == "NUMBER":
            new_case += self.makeNumber()
        elif rcase == "VARIABLE":
            new_case += self.makeVarAssignment()
        elif rcase == "IF":
            new_case += self.makeIfBlock()
        elif rcase == "WHILE":
            new_case += self.makeWhileBlock()
        elif rcase == "PRINT":
            new_case += self.makePrintStatement()

        #TODO - DO THIS WITH REGEX INSTEAD
        while ("  " in new_case):
            new_case = new_case.replace("  ", " ")

        while ("( " in new_case):
            new_case = new_case.replace("( ", "(")

        while (" )" in new_case):
            new_case = new_case.replace(" )", ")")

        while ("[ " in new_case):
            new_case = new_case.replace("[ ", "[")

        while (" ]" in new_case):
            new_case = new_case.replace(" ]", "]")

        if new_case.startswith(" "):
            new_case = new_case[1:]

        return new_case

    def makeSmallInteger(self):
        return str(int(random.random()*10))

    def makeSmallPositiveInteger(self):
        return str(int(random.random()*9)+1)

    def makeNumber(self, level=3):
        casesWithWeights = [{"name": ["FLOAT"], "weight": 3, "concept": "FLOAT"},
                            {"name": ["INTEGER"], "weight": 1, "concept": "INTEGER"}]

        if "BASIC_OPERATORS" in self.CONCEPT_ARRAYS and self.difficulty_level > 0.2:
            casesWithWeights.append(
                {"name": ["NUMBER", "BASIC_OPERATOR", "NUMBER"], "weight": 3, "concept": "BASIC_OPERATOR"})

        if "MODULUS_OPERATOR" in self.CONCEPT_ARRAYS and self.difficulty_level > 0.4:
            casesWithWeights.append(
                {"name": ["INTEGER", "MODULUS_OPERATOR", "SMALL_POSITIVE_INTEGER"], "weight": 3, "concept": "MODULUS_OPERATOR"})

        casesWithWeights = self.validCases(casesWithWeights)

        rcase = self.prepareForWeightedSelection(casesWithWeights)

        new_case = ""
        for keyword in rcase:
            if keyword == "FLOAT":
                new_case += str("{:12.2f}".format(random.random()*100))
            elif keyword == "INTEGER":
                new_case += str(int(random.random()*100))
            elif keyword == "SMALL_INTEGER":
                new_case += self.makeSmallInteger()
            elif keyword == "SMALL_POSITIVE_INTEGER":
                new_case += self.makeSmallPositiveInteger()
            elif keyword == "NUMBER":
                new_case += self.makeNumber()
            elif keyword == "BASIC_OPERATOR":
                new_case += random.choice(self.ARITHMETIC_OPERATORS)
            elif keyword == "MODULUS_OPERATOR":
                new_case += '%'
            else:
                new_case += keyword

            new_case += " "

        return new_case


    def makeCondition(self,level=3):
        casesWithWeights = []
        if level == 2 or level == 1:
            casesWithWeights.append({"name": ["True"], "weight": 2, "concept": "BOOLEAN"})
            casesWithWeights.append({"name": ["False"], "weight": 1, "concept": "BOOLEAN"})

        if level > 1:
            casesWithWeights.append({"name": ["(", "CONDITION", ")"], "weight": 2, "concept": "BRACKET"})

        if level > 1:
            casesWithWeights.append(
                {"name": ["CONDITION", "and", "CONDITION"], "weight": 4, "concept": "AND"})

        if level > 1:
            casesWithWeights.append(
                {"name": ["CONDITION", "or", "CONDITION"], "weight": 3, "concept": "OR"})

        if level > 1:
            casesWithWeights.append({"name": ["not", "CONDITION"], "weight": 1, "concept": "NOT"})

        if "CONDITIONAL_OPERATOR" in self.CONCEPT_ARRAYS and level > 1:
            casesWithWeights.append(
                {"name": ["(", "NUMBER", "CONDITIONAL_OPERATOR", "NUMBER", ")"], "weight": 5, "concept": "CONDITIONAL_OPERATOR"})

        casesWithWeights = self.validCases(casesWithWeights)
        rcase = self.prepareForWeightedSelection(casesWithWeights)

        if len(rcase) == 1:
            return rcase[0]

        else:
            new_case = ""
            for keyword in rcase:
                if keyword == "CONDITION":
                    new_case += self.makeCondition(level=level-1)
                elif keyword == "NUMBER":
                    new_case += self.makeNumber()
                elif keyword == "CONDITIONAL_OPERATOR":
                    new_case += random.choice(self.CONDITIONAL_OPERATORS)
                else:
                    new_case += keyword
                new_case += " "

            return new_case

        return 'BUG'


    def getBiggerBlock(self, num=2):
        block = self.makeBlock(num=2)
        block = map(lambda x: x.split('\n'), block)
        block = reduce(lambda x, y: x+y, block)
        return block

    def initaliseIncrementVariable(self, index_variable):
        return index_variable + " = " + str(random.choice([0, 1]))

    def makeWhileCondition(self, index_variable):
        condition = index_variable + " " + random.choice(["<", "<=", "!="]) + " " + self.makeSmallPositiveInteger()
        return condition

    def incrementCondition(self, index_variable):
        return random.choice([index_variable + " += 1", index_variable + " = " + index_variable + " + 1"])

    def makeWhileBlock(self, level=2):
        index_variable = random.choice(self.INDEX_VARIABLES_NAMES)

        return self.initaliseIncrementVariable(index_variable) + "\n" \
                "while ("+self.makeWhileCondition(index_variable)+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\n\t" + self.incrementCondition(index_variable)

    def makeIfBlock(self, level=3):
        casesWithWeights = [{"name": "IF", "weight": 2}]

        if self.difficulty_level > 0.3:
            casesWithWeights.append({"name": "IFELSE", "weight": 3})

        elif self.difficulty_level > 0.6:
            casesWithWeights.append({"name": "IFELIFSE", "weight": 4})

        casesWithWeights = self.validCases(casesWithWeights)

        rcase = self.prepareForWeightedSelection(casesWithWeights)

        if rcase == "IF":
            return "if ("+self.makeCondition(level=level-1)+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\n"

        elif rcase == "IFELSE":
            return "if ("+self.makeCondition(level=level-1)+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\nelse:\n\t" + \
                "\n\t".join(self.getBiggerBlock())

        elif rcase == "IFELIFSE":
            return "if ("+self.makeCondition(level=level-1)+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\nelif ("+self.makeCondition(level=level-1)+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\nelse:\n\t" + \
                "\n\t".join(self.getBiggerBlock())


    def makeBlock(self, num=5):
        statements = []
        num_statements = int(random.random()*num*3*min(0.3,self.difficulty_level))+1
        
        for _ in range(num_statements):
            statements.append(self.makeStatement())
        return statements

    def getBlock(self):
        try:
            block = self.makeBlock()
            return block
        except RuntimeError:
            return self.getBlock()

    def generateCode(self):
        block = self.getBlock()
        block = map(lambda x: x.split('\n'), block)
        block = reduce(lambda x, y: x+y, block)

        for var in self.variable_map:
            if random.random() > 0.6:
                block.append("print "+var["name"])
        
        self.variable_map = []
        return block

if __name__ == "__main__":
    codeGen = CodeGenerator()
    # codeGen.setConceptArray(["CONDITIONAL_OPERATOR"])
    # codeGen.setConceptArray(["IF"])
    # codeGen.setConceptArray(["BOOLEAN_OPERATORS"])
    # codeGen.setConceptArray(["WHILE"])
    # codeGen.setConceptArray(["INTEGER"])
    # codeGen.setConceptArray(["FLOAT"])
    # codeGen.setConceptArray(["STRING"])
    codeGen.setDifficultyLevel(1)
    print(codeGen.generateCode())