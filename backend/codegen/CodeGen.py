import random
from functools import reduce

# TODO need to work on the glevel
# TODO need to work on the difficulty level

class CodeGenerator:
    NEW_CONCEPTS = []
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
    indent = 0
    complexity = 10

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
                "ifThere": ["LIST"],
                "shouldBeThere": ["NUMBER", "STRING"]
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
        self.NEW_CONCEPTS = concept_array.copy()
        self.CONCEPT_ARRAYS = concept_array
        self.sanitiseConceptArrays()
        print(self.CONCEPT_ARRAYS)

    def setDifficultyLevel(self, level=1):
        self.difficulty_level = level

    def getVariable(self, VTYPE):
        nmap = []
        for i in self.variable_map:
            if i['type'] == VTYPE:
                nmap.append(i["name"])

        if len(nmap):
            return random.choice(nmap)
        else:
            return ""

    def newOrOld(self, vtype, prob, nvalue):
        var = ""
        if random.random() > prob:
            var = self.getVariable(vtype)

        if not var:
            var = nvalue

        return var

    def makeBoolean(self):
        self.complexity -= 1
        return self.newOrOld("BOOLEAN", 0.4, random.choice(self.BOOLEAN_VALUES))

    def makeString(self):
        self.complexity -= 1
        return self.newOrOld("STRING", 0.5, '"' + random.choice(self.VARIABLES_ARRAY) + '"')

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
                    if case["concept"] in self.NEW_CONCEPTS:
                        case["weight"] += 10
                    ncases.append(case)

            if case['name'] in self.CONCEPT_ARRAYS:
                if case["name"] in self.NEW_CONCEPTS:
                    case["weight"] += 10
                ncases.append(case)

        return ncases

    def makeList(self, casesWithWeights = [{"name": "NUMBER", "weight": 3},
                            {"name": "STRING", "weight": 2},
                            {"name": "BOOLEAN", "weight": 1}]):

        self.complexity -= 2

        if self.difficulty_level > 0.5:
            casesWithWeights.append({"name": 'LIST', "weight": 2})

        casesWithWeights = self.validCases(casesWithWeights)

        rcase = self.prepareForWeightedSelection(casesWithWeights)

        new_case = '['
        num_elements = int(random.random()*5+0.7)

        if num_elements == 0:
            return "[]"

        vtype = rcase

        if rcase == 'NUMBER':
            for i in range(num_elements):
                new_case = new_case + self.makeNumber() + ', '
        elif rcase == 'STRING':
            for i in range(num_elements):
                new_case = new_case + self.makeString() + ', '
        elif rcase == 'BOOLEAN':
            for i in range(num_elements):
                bool_val = str(self.makeBoolean())
                new_case = new_case + bool_val + ', '
        elif rcase == 'LIST':
            nvtype = ""

            for i in range(num_elements):
                newCasesWithWeights = []
                for i in casesWithWeights:
                    if i['name'] != "LIST":
                        newCasesWithWeights.append(i)

                list_type = self.prepareForWeightedSelection(newCasesWithWeights)
                (ncase, nvtype) = self.makeList(casesWithWeights=[{"name": list_type, "weight": 1}])
                new_case = new_case + ncase + ', '

            vtype += "_" + nvtype

        new_case = new_case[:-2]
        new_case += ']'
        return (new_case, vtype)

    def makeConstant(self):
        self.complexity -= 1

        casesWithWeights = [{"name": "NUMBER", "weight": 3},
                            {"name": "STRING", "weight": 2},
                            {"name": "BOOLEAN", "weight": 1}]

        if self.difficulty_level > 0.4:
            casesWithWeights.append({"name": "LIST", "weight": 2})

        casesWithWeights = self.validCases(casesWithWeights)

        rcase = self.prepareForWeightedSelection(casesWithWeights)

        if rcase == 'NUMBER':
            new_case = self.makeNumber()[0]
        elif rcase == 'STRING':
            new_case = self.makeString()
        elif rcase == 'BOOLEAN':
            bool_val = str(self.makeBoolean())
            new_case = bool_val
        elif rcase == 'LIST':
            new_case = self.makeList(2)[0]

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
        vtype = ""

        for keyword in rcase:
            if keyword == "VARNAME":
                var_name = random.choice(self.VARIABLES_ARRAY)
                new_case += var_name
                vtype = rcase[2]

            elif keyword == "NUMBER":
                (ncase, vtype) = self.makeNumber()
                new_case += ncase
            elif keyword == "BOOLEAN":
                new_case += self.makeBoolean()
            elif keyword == "STRING":
                new_case += self.makeString()
            elif keyword == "LIST":
                (ncase, vtype) = self.makeList()
                new_case += ncase
                vtype = "LIST_" + vtype
            elif keyword == "CONDITION":
                new_case += self.makeCondition()
            else:
                new_case += keyword
            new_case += " "

        dic = {"name": var_name, "type": vtype}  # MAKE THIS GENERIC
        self.variable_map.append(dic)

        return new_case

    def makePrintStatement(self):
        if (len(self.variable_map)):
            return "print(" + random.choice(self.variable_map)["name"] + ")"
        return "print(" + self.makeConstant() + ")"

    def sanitiseStatement(self, new_case):
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

    def makeStatement(self, start=False):
        if start:
            self.indent = 3
            self.complexity = 10

        casesWithWeights = [{"name": 'BOOLEAN', "weight": 2}]
        casesWithWeights.append({"name": 'VARIABLE', "weight": 4, "concept": "VARIABLE"})
        casesWithWeights.append({"name": 'ARITHMETIC_OPERATORS', "weight": 3, "concept": "NUMBER"})
        casesWithWeights.append({"name": "PRINT", "weight": 1, "concept": "PRINT" })

        if self.indent > 1:
            casesWithWeights.append({"name": 'IF', "weight": 4, "concept": "IF"})
            casesWithWeights.append({"name": 'WHILE', "weight": 3})

        casesWithWeights = self.validCases(casesWithWeights)
        rcase = self.prepareForWeightedSelection(casesWithWeights)
        new_case = ""

        if rcase == "BOOLEAN":
            new_case += self.makeCondition()
        elif rcase == "ARITHMETIC_OPERATORS":
            new_case += self.arithmeticStatement()[0]
        elif rcase == "VARIABLE":
            new_case += self.makeVarAssignment()
        elif rcase == "IF":
            new_case += self.makeIfBlock()
        elif rcase == "WHILE":
            new_case += self.makeWhileBlock()
        elif rcase == "PRINT":
            new_case += self.makePrintStatement()

        new_case = self.sanitiseStatement(new_case)

        return new_case

    def makeSmallInteger(self):
        self.complexity -= 1
        return str(int(random.random()*10))

    def makeSmallPositiveInteger(self):
        self.complexity -= 1
        return self.newOrOld("SMALL_POSITIVE_INTEGER", 0.5, str(int(random.random()*9)+1))

    def arithmeticStatement(self):
        return self.makeNumber(flag="onlyArithmetic")

    def makeNumber(self, flag=""):
        self.complexity -= 1

        casesWithWeights = [{"name": ["FLOAT"], "weight": 1, "concept": "FLOAT"},
                            {"name": ["INTEGER"], "weight": 3, "concept": "INTEGER"}]

        if "ARITHMETIC_OPERATORS" in self.CONCEPT_ARRAYS and self.difficulty_level > 0.2:
            casesWithWeights.append(
                {"name": ["NUMBER", "ARITHMETIC_OPERATOR", "NUMBER"], "weight": 3, "concept": "ARITHMETIC_OPERATORS"})

        if "MODULUS_OPERATOR" in self.CONCEPT_ARRAYS and self.difficulty_level > 0.4:
            casesWithWeights.append(
                {"name": ["INTEGER", "MODULUS_OPERATOR", "SMALL_POSITIVE_INTEGER"], "weight": 3, "concept": "MODULUS_OPERATOR"})

        if flag=="onlyArithmetic":
            casesWithWeights = [{"name": ["NUMBER", "ARITHMETIC_OPERATOR", "NUMBER"], "weight": 3, "concept": "IF"}]

        casesWithWeights = self.validCases(casesWithWeights)

        rcase = self.prepareForWeightedSelection(casesWithWeights)

        new_case = ""
        vtype = ""
        for keyword in rcase:
            if keyword == "FLOAT":
                vtype = keyword
                new_case += self.newOrOld(vtype, 0.5, str("{:12.2f}".format(random.random()*100)))
            elif keyword == "INTEGER":
                vtype = keyword
                new_case += self.newOrOld(vtype, 0.5, str(int(random.random()*100)))
            elif keyword == "SMALL_INTEGER":
                vtype = keyword
                new_case += self.newOrOld(vtype, 0.5, self.makeSmallInteger())
            elif keyword == "SMALL_POSITIVE_INTEGER":
                vtype = keyword
                new_case += self.makeSmallPositiveInteger()
            elif keyword == "NUMBER":
                ncase, vtype = self.makeNumber()
                new_case += ncase
            elif keyword == "ARITHMETIC_OPERATOR" and self.complexity>0:
                self.complexity -= 2
                new_case += random.choice(self.ARITHMETIC_OPERATORS)
            elif keyword == "MODULUS_OPERATOR" and self.complexity>0:
                self.complexity -= 2
                new_case += '%'
            else:
                new_case += keyword
            new_case += " "

        return (new_case, vtype)

    def makeCondition(self):
        casesWithWeights = []
        casesWithWeights.append({"name": ["True"], "weight": 1, "concept": "BOOLEAN"})
        casesWithWeights.append({"name": ["False"], "weight": 1, "concept": "BOOLEAN"})

        casesWithWeights.append({"name": ["(", "CONDITION", ")"], "weight": 2, "concept": "BRACKET"})

        casesWithWeights.append(
            {"name": ["CONDITION", "and", "CONDITION"], "weight": 4, "concept": "AND"})

        casesWithWeights.append(
            {"name": ["CONDITION", "or", "CONDITION"], "weight": 3, "concept": "OR"})

        casesWithWeights.append({"name": ["not", "CONDITION"], "weight": 1, "concept": "NOT"})

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
                    new_case += self.makeCondition()
                elif keyword == "NUMBER":
                    new_case += self.makeNumber()[0]
                elif keyword == "CONDITIONAL_OPERATOR" and self.complexity>0:
                    self.complexity -= 2
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

    def makeWhileBlock(self):
        self.indent -= 1

        index_variable = random.choice(self.INDEX_VARIABLES_NAMES)

        return self.initaliseIncrementVariable(index_variable) + "\n" \
                "while ("+self.makeWhileCondition(index_variable)+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\n\t" + self.incrementCondition(index_variable)

    def makeIfBlock(self):
        self.indent -= 1
        
        casesWithWeights = [{"name": "IF", "weight": 2}]

        if self.difficulty_level > 0.3:
            casesWithWeights.append({"name": "IFELSE", "weight": 3})

        elif self.difficulty_level > 0.6:
            casesWithWeights.append({"name": "IFELIFSE", "weight": 4})

        casesWithWeights = self.validCases(casesWithWeights)

        rcase = self.prepareForWeightedSelection(casesWithWeights)

        if rcase == "IF":
            return "if ("+self.makeCondition()+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\n"

        elif rcase == "IFELSE":
            return "if ("+self.makeCondition()+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\nelse:\n\t" + \
                "\n\t".join(self.getBiggerBlock())

        elif rcase == "IFELIFSE":
            return "if ("+self.makeCondition()+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\nelif ("+self.makeCondition()+") :\n\t" + \
                "\n\t".join(self.getBiggerBlock()) + \
                "\nelse:\n\t" + \
                "\n\t".join(self.getBiggerBlock())


    def getStatement(self, start=False):
        try:
            statement = self.makeStatement(start=start)
            return statement
        except RuntimeError:
            return self.getStatement(start = start)

    def makeBlock(self, num=2, start=False):
        statements = []
        num_statements = int(random.random()*num*3*min(0.3,self.difficulty_level))+2

        for _ in range(num_statements):
            statements.append(self.getStatement(start=start))
        
        return statements

    def generateCode(self):
        block = self.makeBlock(start=True)
        block = map(lambda x: x.split('\n'), block)
        block = reduce(lambda x, y: x+y, block)

        for var in self.variable_map:
            if random.random() > 0.6:
                block.append("print("+var["name"]+")") 

        self.variable_map = []
        return block

if __name__ == "__main__":
    codeGen = CodeGenerator()
    # codeGen.setConceptArray(["CONDITIONAL_OPERATOR"])
    # codeGen.setConceptArray(["IF"])
    # codeGen.setConceptArray(["BOOLEAN_OPERATORS"])
    codeGen.setConceptArray(["WHILE"])
    # codeGen.setConceptArray(["ARITHMETIC_OPERATORS"])
    # codeGen.setConceptArray(["INTEGER"])
    # codeGen.setConceptArray(["FLOAT"])
    # codeGen.setConceptArray(["BOOLEAN"])
    codeGen.setDifficultyLevel(1)
    for i in codeGen.generateCode():
        print(i)
