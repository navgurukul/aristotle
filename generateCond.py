
import random
import ast
from numpy.random import choice

"""
Our current vocab

CONDITION
and
or
not
BRACKET
number
CONDITIONAL_OPERATOR
"""

concept_arrays = ["BRACKET", "and", "or", "not", "CONDITIONAL_OPERATOR",
                  "BASIC_OPERATORS", "MODULUS_OPERATOR", "VAR_ASSIGNMENT", "IFELSE"]
basic_operators = ["+", "-", "*", "/"]
modulus_operator = "%"
conditional_operators = ["==", "!=", "<", ">", ">=", "<="]
boolean_values = ["True", "False"]

# Kaun kaun se variables, kis type se define kiye hai
# [{name: "shivam", type: "bool"}]

variable_map = []


variables_array = ["caboVerde", "costaRica", "dominicanRepublic", "elSalvador", "guineaBissau", "holySee", "koreaSouth",
                   "newZealand", "palestinianTerritories", "sanMarino", "solomonIslands", "sriLanka", "timorLeste", "unitedKingdom", "southSudan"]

# BLOCKS => LIST OF STATEMENTS (Random length upto say 5 )
# STATEMENT => CONDITION
# STATEMENT => NUMBER
# STATEMENT => VAR = NUMBER | BOOLEAN | STRING | LIST (VAR_ASSIGNMENT)
# STORE THIS VARIABLE IN THE VARIABLE MAP
# LIST => [ NUMBER ]
#         [ BOOLEAN ],
#         [ STRING ]
#          [LIST ]
# USE A LONG LIST OF GOOD VARIABLE NAMES IN variable_names.json snakeCase
# READ http://saral.navgurukul.org/course?id=18&slug=python__variables%2Fvariables-naming-conventions before defining variable names - have a mix of two names


def makeBoolean():
    if random.random() > 0.5:
        return True
    return False


def makeString():
    return random.choice(variables_array)


def makeList(level=3):
    cases = ['NUMBER', 'STRING', 'BOOLEAN']
    weights = [0.3,0.5,0.2]

    if level > 1:
        cases.append('LIST')
    rcase = choice(cases,1, p=weights)

    new_case = '['
    num_elements = int(random.random()*5)

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


def makeVarAssignment():
    cases = [["VARNAME", "=", 'NUMBER'],
             ["VARNAME", "=", 'STRING'],
             ["VARNAME", "=", 'BOOLEAN'],
             ["VARNAME", "=", 'LIST'],
             ["VARNAME", "=", 'CONDITION']
             ]

    weights = [0.1,0.2, 0.1, 0.1, 0.5]

    rcase = choice(cases,1, p=weights)
    new_case = ""

    for keyword in rcase:
        if keyword == "VARNAME":
            var_name = random.choice(variables_array)
            new_case += var_name
            dic = {"name": var_name, "type": rcase[2]}  # MAKE THIS GENERIC
            variable_map.append(dic)

        elif keyword == "NUMBER":
            new_case += makeNumber()
        elif keyword == "BOOLEAN":
            new_case += random.choice(boolean_values)
        elif keyword == "STRING":
            new_case += '"' + random.choice(variables_array) + '"'
        elif keyword == "LIST":
            new_case += makeList()
        elif keyword == "CONDITION":
            new_case += makeCondition()
        else:
            new_case += keyword
        new_case += " "

    return new_case


def makeStatement():
    cases = ['CONDITION', 'NUMBER', "VAR_ASSIGNMENT", "IFSTATEMENT"]
    weights = [0.2, 0.1, 0.4, 0.3]


    rcase = choice(cases,1, p=weights)

    new_case = ""
    if rcase == "CONDITION":
        new_case += makeCondition()
    elif rcase == "NUMBER":
        new_case += makeNumber()
    elif rcase == "VAR_ASSIGNMENT":
        new_case += makeVarAssignment()
    elif rcase == "IFSTATEMENT":
        new_case += makeIfBlock()

    while ("  " in new_case):
        new_case = new_case.replace("  ", " ")

    while ("( " in new_case):
        new_case = new_case.replace("( ", "(")

    while (" )" in new_case):
        new_case = new_case.replace(" )", ")")

    if new_case.startswith(" "):
        new_case = new_case[1:]

    return new_case


def makeNumber(level=3):
    cases = [["FLOAT"], ["INTEGER"]]

    weights = [0.5, 0.5]

    if "BASIC_OPERATORS" in concept_arrays and level > 1:
        cases.append(["NUMBER", "BASIC_OPERATOR", "NUMBER"])

    if "MODULUS_OPERATOR" in concept_arrays and level > 2:
        cases.append(["INTEGER", "MODULUS_OPERATOR", "SMALL_POSITIVE_INTEGER"])

    rcase = choice(cases,1, p=weights)

    new_case = ""
    for keyword in rcase:
        if keyword == "FLOAT":
            # TODO DO FLOAT TO STRING HERE
            new_case += str("{:12.2f}".format(random.random()*100))
        elif keyword == "INTEGER":
            new_case += str(int(random.random()*100))
        elif keyword == "SMALL_INTEGER":
            new_case += str(int(random.random()*10))
        elif keyword == "SMALL_POSITIVE_INTEGER":
            new_case += str(int(random.random()*9)+1)
        elif keyword == "NUMBER":
            new_case += makeNumber()
        elif keyword == "BASIC_OPERATOR":
            new_case += random.choice(basic_operators)
        else:
            new_case += modulus_operator
        new_case += " "

    return new_case


def makeCondition(level=3):
    cases = []
    if level == 2 or level == 1:
        cases = [["True"], ["False"]]

    if "BRACKET" in concept_arrays and level > 1:
        cases.append(["(", "CONDITION", ")"])

    if "and" in concept_arrays and level > 1:
        cases.append(["CONDITION", "and", "CONDITION"])

    if "or" in concept_arrays and level > 1:
        cases.append(["CONDITION", "or", "CONDITION"])

    if "not" in concept_arrays and level > 1:
        cases.append(["not", "CONDITION"])

    if "CONDITIONAL_OPERATOR" in concept_arrays and level > 1:
        cases.append(["(", "NUMBER", "CONDITIONAL_OPERATOR", "NUMBER", ")"])

    rcase = random.choice(cases)

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
                new_case += random.choice(conditional_operators)
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


def makeIfBlock(level=2):
    cases = ["IF", "IFELSE"]
    weights = [0.6, 0.4]

    if level > 1:
        cases.append("IFELIFSE")

    rcase = choice(cases,1, p=weights)

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
    for i in range(num_statements):
        statements.append(makeStatement())
    return statements


for i in makeBlock():
    print i

print "\n\n"

for var in variable_map:
    print "print "+var["name"]
