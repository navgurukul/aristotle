import random
"""
Our current vocab

CONDITION
and
or
not
BRACKET
number
CONDITIONAL_OPERATOR
WHILE
"""

GLEVEL = 0
CONCEPT_ARRAYS = ["BRACKET", "and", "or", "not", "CONDITIONAL_OPERATOR",
                  "BASIC_OOPERATORS", "MODULUS_OPERATOR",
                  "VAR_ASSIGNMENT", "IFELSE", "WHILE"]

BASIC_OOPERATORS = ["+", "-", "*", "/"]
MODULUS_OPERATOR = "%"
CONDITIONAL_OPERATORS = ["==", "!=", "<", ">", ">=", "<="]
BOOLEAN_VALUES = ["True", "False"]
VARIABLES_ARRAY = ["caboVerde", "costaRica", "dominicanRepublic", "elSalvador", "guineaBissau", "holySee", "koreaSouth",
                   "newZealand", "palestinianTerritories", "sanMarino", "solomonIslands", "sriLanka", "timorLeste", "unitedKingdom", "southSudan"]
INDEX_VARIABLES_NAMES = ["ctr", "index", "i", "n"]

# Kaun kaun se variables, kis type se define kiye hai
# [{name: "shivam", type: "bool"}]
variable_map = []

def makeBoolean():
    return random.choice(BOOLEAN_VALUES)

def makeString():
    return '"' + random.choice(VARIABLES_ARRAY) + '"'

def select(container, weights):
    total_weight = float(sum(weights))
    rel_weight = [w / total_weight for w in weights]

    # Probability for each element
    probs = [sum(rel_weight[:i + 1]) for i in range(len(rel_weight))]

    slot = random.random()*1
    for (i, element) in enumerate(container):
        if slot <= probs[i]:
            break

    return element


def makeList(level=3):
    cases = ['NUMBER', 'STRING', 'BOOLEAN']

    weights = [3, 4, 1]

    if level > 1:
        cases.append('LIST')
        # TODO ERROR - SHIFT To a dictionary list to accomodate weights
    rcase = select(cases, weights)

    new_case = '['
    num_elements = int(random.random()*5)

    if num_elements == 0:
        return "[]"

    for i in range(num_elements):
        if rcase == 'NUMBER':
            new_case = new_case + makeNumber() + ', '
        elif rcase == 'STRING':
            new_case = new_case + makeString() + ', '
        elif rcase == 'BOOLEAN':
            bool_val = str(makeBoolean())
            new_case = new_case + bool_val + ', '
        elif rcase == 'LIST':
            new_case = new_case + makeList(level=level-2) + ', '
            # ast.literal_eval(makeList(level=level-2)) + ', '

    new_case = new_case[:-2]
    new_case += ']'
    return new_case

def makeConstant(level=2):
    cases = ['NUMBER', 'STRING', 'BOOLEAN', "LIST"]
    weights = [3, 4, 1, 3]

    #TDOD - MAKE A FUNCTION TO FIND INTERSECTION OF CASES WITH CONCEPT_ARRAY INPUT TO CREATE A NEW CASE ARRAY

    rcase = select(cases, weights)

    if rcase == 'NUMBER':
        new_case = makeNumber()
    elif rcase == 'STRING':
        new_case = makeString()
    elif rcase == 'BOOLEAN':
        bool_val = str(makeBoolean())
        new_case = bool_val
    elif rcase == 'LIST':
        new_case = makeList(2)

    return new_case

def makeVarAssignment():
    cases = [["VARNAME", "=", 'NUMBER'],
             ["VARNAME", "=", 'STRING'],
             ["VARNAME", "=", 'BOOLEAN'],
             ["VARNAME", "=", 'LIST'],
             ["VARNAME", "=", 'CONDITION']
             ]
    weights = [4, 2, 1, 1, 2]
    rcase = select(cases, weights)
    new_case = ""

    for keyword in rcase:
        if keyword == "VARNAME":
            var_name = random.choice(VARIABLES_ARRAY)
            new_case += var_name
            dic = {"name": var_name, "type": rcase[2]}  # MAKE THIS GENERIC
            variable_map.append(dic)

        elif keyword == "NUMBER":
            new_case += makeNumber()
        elif keyword == "BOOLEAN":
            new_case += makeBoolean()
        elif keyword == "STRING":
            new_case += makeString()
        elif keyword == "LIST":
            new_case += makeList()
        elif keyword == "CONDITION":
            new_case += makeCondition()
        else:
            new_case += keyword
        new_case += " "

    return new_case

def makePrintStatement():
    if (len(variable_map)):
        return "print " + random.choice(variable_map)["name"]
    return "print " + makeConstant()

def makeStatement():
    cases = ['CONDITION', 'NUMBER', "VAR_ASSIGNMENT", "IFSTATEMENT", "WHILE", "PRINT_STATEMENT"]
    weights = [3, 1, 2, 2, 4, 5]
    rcase = select(cases, weights)

    new_case = ""

    # TODO SHIFT SUCH IFS TO SWITCH STATEMENTS
    if rcase == "CONDITION":
        new_case += makeCondition()
    elif rcase == "NUMBER":
        new_case += makeNumber()
    elif rcase == "VAR_ASSIGNMENT":
        new_case += makeVarAssignment()
    elif rcase == "IFSTATEMENT":
        new_case += makeIfBlock()
    elif rcase == "WHILE":
        new_case += makeWhileBlock()
    elif rcase == "PRINT_STATEMENT":
        new_case += makePrintStatement()

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

def makeSmallInteger():
    return str(int(random.random()*10))

def makeSmallPositiveInteger():
    return str(int(random.random()*9)+1)

def makeNumber(level=3):
    cases = [["FLOAT"], ["INTEGER"]]
    weights = [3, 2]

    if "BASIC_OOPERATORS" in CONCEPT_ARRAYS and level > 1:
        cases.append(["NUMBER", "BASIC_OPERATOR", "NUMBER"])

    if "MODULUS_OPERATOR" in CONCEPT_ARRAYS and level > 2:
        cases.append(["INTEGER", "MODULUS_OPERATOR", "SMALL_POSITIVE_INTEGER"])

    rcase = select(cases, weights)

    new_case = ""
    for keyword in rcase:
        if keyword == "FLOAT":
            # TODO DO FLOAT TO STRING HERE
            new_case += str("{:12.2f}".format(random.random()*100))
        elif keyword == "INTEGER":
            new_case += str(int(random.random()*100))
        elif keyword == "SMALL_INTEGER":
            new_case += makeSmallInteger()
        elif keyword == "SMALL_POSITIVE_INTEGER":
            new_case += makeSmallPositiveInteger()
        elif keyword == "NUMBER":
            new_case += makeNumber()
        elif keyword == "BASIC_OPERATOR":
            new_case += random.choice(BASIC_OOPERATORS)
        else:
            new_case += MODULUS_OPERATOR
        new_case += " "

    return new_case


def makeCondition(level=3):
    cases = []
    if level == 2 or level == 1:
        cases = [["True"], ["False"]]

    if "BRACKET" in CONCEPT_ARRAYS and level > 1:
        cases.append(["(", "CONDITION", ")"])

    if "and" in CONCEPT_ARRAYS and level > 1:
        cases.append(["CONDITION", "and", "CONDITION"])

    if "or" in CONCEPT_ARRAYS and level > 1:
        cases.append(["CONDITION", "or", "CONDITION"])

    if "not" in CONCEPT_ARRAYS and level > 1:
        cases.append(["not", "CONDITION"])

    if "CONDITIONAL_OPERATOR" in CONCEPT_ARRAYS and level > 1:
        cases.append(["(", "NUMBER", "CONDITIONAL_OPERATOR", "NUMBER", ")"])

    weights = [3, 2, 1, 1, 2, 1]
    rcase = select(cases, weights)

    if len(rcase) == 1:
        return rcase[0]

    else:
        new_case = ""
        for keyword in rcase:
            if keyword == "CONDITION":
                new_case += makeCondition(level=level-1)
            elif keyword == "NUMBER":
                new_case += makeNumber()
            elif keyword == "CONDITIONAL_OPERATOR":
                new_case += random.choice(CONDITIONAL_OPERATORS)
            else:
                new_case += keyword
            new_case += " "

        return new_case

    return 'BUG'


def getBiggerBlock(num=2):
    block = makeBlock(num=2)
    block = map(lambda x: x.split('\n'), block)
    block = reduce(lambda x, y: x+y, block)
    return block

def makeWhileCondition(index_variable):
    condition = index_variable + " " + random.choice(["<", "<=", "!="]) + " " + makeSmallInteger()
    return condition

def incrementCondition(index_variable):
    return random.choice([index_variable + " += 1", index_variable + " = " + index_variable + " + 1"])

def makeWhileBlock(level=2):
    index_variable = random.choice(INDEX_VARIABLES_NAMES)

    return "while ("+makeWhileCondition(index_variable)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\n\t" + incrementCondition(index_variable)

def makeIfBlock(level=2):
    cases = ["IF", "IFELSE"]

    if level > 1:
        cases.append("IFELIFSE")
    weights = [3, 2]
    rcase = select(cases, weights)

    if rcase == "IF":
        return "if ("+makeCondition(level=1)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\n"

    elif rcase == "IFELSE":
        return "if ("+makeCondition(level=1)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\nelse:\n\t" + \
            "\n\t".join(getBiggerBlock())

    elif rcase == "IFELIFSE":
        return "if ("+makeCondition(level=1)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\nelif ("+makeCondition(level=1)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\nelse:\n\t" + \
            "\n\t".join(getBiggerBlock())


def makeBlock(num=5):
    statements = []
    num_statements = int(random.random()*num)+1
    for _ in range(num_statements):
        statements.append(makeStatement())
    return statements


for i in makeBlock():
    print i

print "\n\n"

for var in variable_map:
    print "print "+var["name"]
