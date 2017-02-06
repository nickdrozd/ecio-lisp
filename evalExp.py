from keywords import *
from reg import *
from evalFuncs import *

def evalExp():
	expr = fetch(EXPR)
	# expr = transformMacros(expr)
	evalFunc = getEvalFunc(expr)
	evalFunc()


def getEvalFunc(expr):
	if isVar(expr):
		return evalVar

	if isNum(expr):
		return evalNum

	# else
	tag, *_ = expr

	keyword_groups = {
		define_keys : evalDef, 
		# ass_keys : evalAss, 
		lambda_keys : evalLambda, 
		if_keys : evalIf, 
		# begin_keys : evalBegin, 
		quote_keys : evalQuote
	}

	for group in keyword_groups:
		if tag in group:
			return keyword_groups[group]

	# default
	return evalFunc


def isNum(exp):
	try:
		return type(int(exp)) == int
	except:
		return False

def isVar(exp):
	return type(exp) == str
