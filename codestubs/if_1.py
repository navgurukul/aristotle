
import random

## Difficlulty let's have a difficulty in terms of 1 - 5
difficulty = {
	1 : {
		'variables': 1,
		'elif_condidtions': 1,
		'extensive_not': False
	},
	2 : {
		'variables': 1,
		'elif_condidtions': 2,
		'extensive_not': True
	},
	3 : {
		'variables': 2,
		'elif_condidtions': 2,
		'extensive_not': False
	},
	4 : {
		'variables': 3,
		'elif_condidtions': 2,
		'extensive_not': True
	},
	5 : {
		'variables': 3,
		'elif_condidtions': 3,
		'extensive_not': True
	},
}

dual_expression = ['and', 'or']
singular_expression = ['not']
logical_operators = ['<', '<=', '>', '>=', '!=', '==', '<', '<=', '>', '>=',]

def define_variables(variable_count):
	variable_stub = ""
	for count in xrange(variable_count):
		variable_stub += chr(65 + count) + " = " + str(int(random.random() * 100000)) + "\n"
	return variable_stub

def add_parenthisis(expression):
	return '(' + expression + ')'

def add_not_operator(expression, prob=0.05):
	if random.random() < prob:
		return "not " + expression
	else:
		return expression

def create_logical_expression(variable):
	return variable + " " + random.choice(logical_operators) + " " + str(int(random.random() * 100000))

def create_partial_expression(level):
	not_prob = 0.05
	if difficulty[level]['extensive_not']:
		not_prob = 0.3
	variables = random.sample(range(difficulty[level]['variables']), random.randint(1, difficulty[level]['variables']))
	expression = create_logical_expression(chr(65 + variables[0]))
	for variable in xrange(1, len(variables)):
		expression += " " + random.choice(dual_expression) + " " + create_logical_expression(chr(65 + variable))
	expression = add_parenthisis(expression)
	expression = add_not_operator(expression, not_prob)
	return expression

def create_complete_expression(level):
	no_of_expression = difficulty[level]['variables'] - 1
	expression = create_partial_expression(level)
	for _ in xrange(1, no_of_expression):
		expression += " " + random.choice(dual_expression) + " " + create_partial_expression(level)
	return expression

def generate_code_stub(level):
	if not (level >= 1 and level <= 5):
		return "print 'Error!' "
	stub = ""
	stub += define_variables(difficulty[level]['variables'])
	conditions_count = difficulty[level]['elif_condidtions'] + 2
	for count in xrange(conditions_count):
		if count == 0:
			stub += "if " + create_complete_expression(level) + ":" + "\n"
		elif count	== conditions_count - 1:
			stub += "else:\n"
		else:
			stub += "elif " + create_complete_expression(level) + ":" + "\n"
		stub += "\tprint " + "'" + chr(65 + count) + "'" + "\n"
	return stub

print generate_code_stub(1)