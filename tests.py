import unittest
import json

from reg import *
from stack import *
from instr import *
from env import *

from evalFuncs import *

from init import initialize
from parse import parse


class EvalTest(unittest.TestCase):

	# setup #

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.verbose = 1
		
	def setUp(self):
		# ensure files exist?
		initialize()
		self.display()

	def tearDown(self):
		# initialize()
		self.display()

	# environment operations #

	def test_lookup(self):
		env = [
			{'ragdoll': 4}, [
				{'sphynx': 5},
				[]
			]
		]

		pairs = (
			('ragdoll', 4),
			('sphynx', 5),
			('siamese', UNBOUND))

		self.assign_and_verify(ENV, env)

		for var, val in pairs:
			self.assign_and_verify(VAL, var)
			self.assertEqual(val, lookup(VAL))


	def test_define_var(self):
		initial_env = [
			{'trout': 4}, [
				{'cod': 5},
				[]
			]
		]

		var, val = 'halibut', 6

		expected_env = [
			{'trout': 4, 'halibut': 6}, [
				{'cod': 5},
				[]
			]
		]

		before = {
			ENV : initial_env,
			VAL : val,
			UNEV : var
		}

		func = defineVar

		after = {
			ENV : expected_env
		}

		self.assert_before_func_after(before, func, after)

	# basic register tests #

	def test_reg(self):
		'''
		1) Assign several words to EXPR.

		2) Assign distinct contents to VAL and CONT, 
		then assign CONT to VAL.
		'''
		for animal in 'wren', 'jay', 'finch':
			self.assign_and_verify(EXPR, animal)

		self.display()

		val, cont = 'lark', 'thrush'

		self.set_up_registers({
			VAL : val,
			CONT : cont
		})

		assign(VAL, fetch(CONT))

		self.verify_outcome({
			VAL : cont,
			CONT : cont
		})

		code = parse('(warbler bulbul titmouse)')

		self.assign_and_verify(FUNC, code)


	def test_stack(self):
		'''
		Assign to VAL and CONT, save from both, 
		then assign back to them in reverse order.
		'''
		val, cont = 'schipperke', 'pomeranian'

		self.set_up_registers({
			VAL : val,
			CONT : cont
		})

		self.assert_empty_stack()

		self.save_and_verify_pairs(
			(VAL, val),
			(CONT, cont))

		self.assert_stack_depth(2)

		self.restore_and_verify_pairs(
			(VAL, cont),
			(CONT, val))

		self.assert_empty_stack()

		# save and restore lists

		self.display()

		code = parse('(yorkie scottie jack russell)')

		self.assign_and_verify(ARGL, code)
		self.save_and_verify(ARGL, code)
		self.restore_and_verify(UNEV, code)


	def test_goto(self):
		self.goto_and_verify('quince')
		self.goto_continue_and_verify('fig')
		self.goto_eval_and_verify()

	# assertions #

	def assert_before_func_after(self, before, func, after):
		'''
		before and after are dicts, func a function
		'''
		self.set_up_registers(before)
		func()
		self.verify_outcome(after)

	def set_up_registers(self, setup):
		for reg in setup:
			self.assign_and_verify(reg, setup[reg])

	def verify_outcome(self, expected):
		for reg in expected:
			self.assert_reg_contents(reg, expected[reg])

	def goto_eval_and_verify(self):
		goto_eval()
		self.assert_reg_contents(INSTR, EVAL_EXP)

	def goto_continue_and_verify(self, label):
		self.set_continue_and_verify(label)
		goto_continue()
		self.assert_reg_contents(INSTR, label)

	def set_continue_and_verify(self, label):
		set_continue(label)
		self.assert_reg_contents(CONT, label)

	def goto_and_verify(self, label):
		goto(label)
		self.assert_reg_contents(INSTR, label)

	def save_and_verify_pairs(self, *pairs):
		for reg, expected in pairs:
			self.save_and_verify(reg, expected)

	def save_and_verify(self, reg, expected):
		self.display('saving from {}...'.format(reg))
		depth = self.get_stack_depth()
		save(reg)
		self.show_stack()
		self.assert_stack_depth(depth + 1)
		self.assert_stack_top(expected)
		self.assert_reg_contents(reg, expected)

	def restore_and_verify_pairs(self, *pairs):
		for reg, expected in pairs:
			self.restore_and_verify(reg, expected)

	def restore_and_verify(self, reg, expected):
		self.display('restoring to {}...'.format(reg))
		depth = self.get_stack_depth()
		restore(reg)
		self.show_stack()
		self.assert_stack_depth(depth - 1)
		self.assert_reg_contents(reg, expected)

	def assert_stack_depth(self, expected):
		depth = self.get_stack_depth()
		self.display_expected_actual(
			'STACK DEPTH', expected, depth)
		self.assertEqual(expected, depth)

	def assert_stack_top(self, expected):
		top = self.get_stack_top()
		self.display_expected_actual(
			'STACK TOP', expected, top)
		self.assertEqual(top, expected)

	def assert_empty_stack(self):
		with open(STACK, 'r') as stack:
			self.assertEqual(stack.read(), '')

	def assign_and_verify_pairs(self, *pairs):
		for reg, contents in pairs:
			self.assign_and_verify(reg, contents)

	def assign_and_verify(self, reg, contents):
		msg = 'assigning {} to {}...'
		self.display(msg.format(contents, reg))
		assign(reg, contents)
		self.assert_reg_contents(reg, contents)

	def assert_reg_contents_pairs(self, *pairs):
		for reg, expected in pairs:
			self.assert_reg_contents(reg, expected)

	def assert_reg_contents(self, reg, expected):
		contents = fetch(reg)
		self.display_expected_actual(reg, expected, contents)
		self.assertEqual(contents, expected)

	# utilities #

	def get_stack_depth(self):
		with open(STACK, 'r') as stack:
			return len(stack.readlines())

	def get_stack_top(self):
		with open(STACK, 'r') as stack:
			contents = stack.readlines()

		self.assertNotEqual(contents, '')
		*tail, head = contents
		return json.loads(head)

	def show_stack(self):
		with open(STACK, 'r') as stack:
			stack_contents = stack.read().split('\n')
			self.display('STACK: ' + str(stack_contents))

	def display_expected_actual(self, reg, expected, actual):
		msg = '{} -- expected: {} -- actual: {}'
		self.display(msg.format(reg, expected, actual))

	def display(self, msg=''):
		if self.verbose:
			print(msg)


if __name__ == '__main__':
	unittest.main()
