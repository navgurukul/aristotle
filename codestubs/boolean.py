
import random

## Difficlulty let's have a difficulty in terms of 1 - 5
difficulty = {
	1 : {
		'variables': 2,
		'parenthisis': False,
		'extensive_not': False
	},
	2 : {
		'variables': 2,
		'parenthisis': False,
		'extensive_not': True
	},
	3 : {
		'variables': 3,
		'parenthisis': True,
		'extensive_not': False
	},
	4 : {
		'variables': 3,
		'parenthisis': True,
		'extensive_not': True
	},
	5 : {
		'variables': 4,
		'parenthisis': True,
		'extensive_not': True
	},
}

dual_expression = ['and', 'or']
singular_expression = ['not']

def define_variables(variable_count):
	variable_stub = ""
	for i in xrange(variable_count):
		variable_stub += chr(65 + i) + " = " + str(bool(random.getrandbits(1))) + "\n"
	return variable_stub

def add_parenthisis(expression):
	return '(' + expression + ')'

def add_not_operator(expression, prob=0.05):
	if random.random() < prob:
		return "not " + expression
	else:
		return expression

def get_expression(level):
	not_prob = 0.05
	if difficulty[level]['extensive_not']:
		not_prob = 0.3
	variables = random.sample(range(difficulty[level]['variables']), random.randint(2, difficulty[level]['variables']))
	expression = chr(65 + variables[0])
	for variable in xrange(1, len(variables)):
		expression += " " + random.choice(dual_expression) + " " + add_not_operator(chr(65 + variable), not_prob)
	expression = add_parenthisis(expression)
	expression = add_not_operator(expression, not_prob)
	return expression

def generate_expression(level):
	no_of_expression = difficulty[level]['variables'] - 1
	expression = get_expression(level)
	for _ in xrange(1, no_of_expression):
		expression += " " + random.choice(dual_expression) + " " + get_expression(level)
	return expression


def generate_code_stub(level):
	if not (level >= 1 and level <= 5):
		return "print 'Error!' "
	stub = ""
	stub += define_variables(difficulty[level]['variables'])
	expression = generate_expression(level)
	stub += "print " + expression
	return stub

print generate_code_stub(5)