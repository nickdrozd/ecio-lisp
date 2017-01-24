from keywords import *
from reg import *
from parse import parse

def evalExp():
	expr = parse(fetch(EXPR)) # make dedicated fetch_expr()?
	# expr = transformMacros(expr)
	evalFunc = getEvalFunc(expr)
	# evalFunc()
	# reassign next step

def getEvalFunc(expr):
	if isVar(expr):
		return compVar

	if isNum(expr):
		return compNum

	# else
	tag, *_ = expr

	keyword_groups = {
		define_keys : evalDef, 
		ass_keys : evalAss, 
		lambda_keys : evalLambda, 
		if_keys : evalIf, 
		begin_keys : evalBegin, 
		quote_keys : evalQuote
	}

	for group in keyword_groups:
		if tag in group:
			return keyword_groups[group]

	# default
	return evalApp

def isNum(exp):
	try:
		return type(int(exp)) == int
	except:
		return False

def isVar(exp):
	return type(exp) == str
