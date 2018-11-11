
import random

concept_arrays = ["bracket", "and", "or", "not", "bool"]

def makeCondition():
    cases = [["True"], ["False"]]

    if "bracket" in concept_arrays:
        cases.append(["(", "makeCondition", ")"])
    
    if "and" in concept_arrays:
        cases.append(["makeCondition", "and", "makeCondition"])
    
    if "or" in concept_arrays:
        cases.append(["makeCondition", "or", "makeCondition"])
    
    if "not" in concept_arrays:
        cases.append(["not", "makeCondition"])

    random_case = int(random.random() * len (cases))

    rcase = cases[random_case]

    if len(rcase) == 1:
        return rcase[0]
    
    else:
        new_case = ""
        for str in rcase:
            if str=="makeCondition":
                new_case += makeCondition() + " "
            else:
                new_case += str + " "

        return new_case

    return 'BUG'


print makeCondition()