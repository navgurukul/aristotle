
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
"""

concept_arrays = ["BRACKET", "and", "or", "not", "CONDITIONAL_OPERATOR", "BASIC_OPERATORS", "MODULUS_OPERATOR"]
basic_operators = ["+", "-", "*", "/"]
modulus_operator = "%"
conditional_operators = ["==", "!=", "<", ">", ">=", "<="]

# BLOCKS => LIST OF STATEMENTS (Random length upto say 5 )
# STATEMENT => CONDITION
# STATEMENT => NUMBER
# STATEMENT => VAR = NUMBER
# STATEMENT => VAR = VAR
# USE A LONG LIST OF GOOD VARIABLE NAMES IN variable_names.json snakeCase
# READ http://saral.navgurukul.org/course?id=18&slug=python__variables%2Fvariables-naming-conventions before defining variable names - have a mix of two names

def makeNumber():
    cases = [["FLOAT"], ["INTEGER"]]

    if "BASIC_OPERATORS" in concept_arrays:
        cases.append(["NUMBER", "BASIC_OPERATOR", "NUMBER"])
    
    if "MODULUS_OPERATOR" in concept_arrays:
        cases.append(["INTEGER", "MODULUS_OPERATOR", "SMALL_INTEGER"])

    rcase = random.choice(cases)

    new_case = ""
    for keyword in rcase:
        if keyword=="FLOAT":
            # TODO DO FLOAT TO STRING HERE
            new_case += str(int(random.random()*100))
        elif keyword=="INTEGER":
            new_case += str(int(random.random()*100))
        elif keyword=="SMALL_INTEGER":
            new_case += str(int(random.random()*10))
        elif keyword=="NUMBER":
            new_case += makeNumber()
        elif keyword=="BASIC_OPERATOR":
            new_case += random.choice(basic_operators)
        else:
            new_case += modulus_operator
        new_case += " "

    return new_case

def makeCondition():
    cases = [["True"], ["False"]]

    if "BRACKET" in concept_arrays:
        cases.append(["(", "CONDITION", ")"])
    
    if "and" in concept_arrays:
        cases.append(["CONDITION", "and", "CONDITION"])
    
    if "or" in concept_arrays:
        cases.append(["CONDITION", "or", "CONDITION"])
    
    if "not" in concept_arrays:
        cases.append(["not", "CONDITION"])
    
    if "CONDITIONAL_OPERATOR" in concept_arrays:
        cases.append(["(", "NUMBER", "CONDITIONAL_OPERATOR", "NUMBER", ")"])

    rcase = random.choice(cases)

    if len(rcase) == 1:
        return rcase[0]
    
    else:
        new_case = ""
        for keyword in rcase:
            if keyword=="CONDITION":
                new_case += makeCondition()
            elif keyword=="NUMBER":
                new_case += makeNumber()
            elif keyword=="CONDITIONAL_OPERATOR":
                new_case += random.choice(conditional_operators)
            else:
                new_case += keyword
            new_case += " "

        return new_case

    return 'BUG'

# also return answer of your question
print makeCondition()