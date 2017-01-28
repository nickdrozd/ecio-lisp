import unittest

from reg import *
from stack import *
from instr import *

from evalFuncs import *

from init import initialize

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

	# eval tests #

	def test_eval_quote(self):
		pass


	def test_eval_var(self):
		"lookup not implemented"


	def test_eval_num(self):
		expr, cont = '5', 'persimmon'

		self.assign_and_verify_pairs(
			(EXPR, expr), 
			(CONT, cont))

		evalNum()

		self.assert_reg_contents_pairs(
			(VAL, expr), 
			(INSTR, cont))

	# basic register tests #

	def test_reg(self):
		'''
		1) Assign several words to EXPR.

		2) Assign distinct contents to VAL and CONT, 
		then assign CONT to VAL.
		'''

		for animal in 'cow', 'pig', 'sheep':
			self.assign_and_verify(EXPR, animal)

		self.display()

		val, cont = 'lark', 'thrush'

		self.assign_and_verify_pairs(
			(VAL, val), 
			(CONT, cont))

		assign(VAL, fetch(CONT))

		self.assert_reg_contents_pairs(
			(VAL, cont), 
			(CONT, cont))


	def test_stack(self):
		'''
		Assign to VAL and CONT, save from both, 
		then assign back to them in reverse order.
		'''
		val, cont = 'cat', 'dog'

		self.assign_and_verify_pairs(
			(VAL, val), 
			(CONT, cont))

		self.assert_empty_stack()

		self.save_and_verify(
			VAL, 
			CONT)

		self.assert_stack_depth(2)

		self.restore_and_verify_pairs(
			(VAL, cont), 
			(CONT, val))

		self.assert_empty_stack()


	def test_goto(self):
		self.goto_and_verify('quince')
		self.goto_continue_and_verify('fig')
		self.goto_eval_and_verify()


	# assertions #

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

	def save_and_verify(self, *regs):
		for reg in regs:
			self.display('saving from {}...'.format(reg))
			depth = self.get_stack_depth()
			save(reg)
			self.show_stack()
			self.assert_stack_depth(depth + 1)
			self.assert_stack_top(fetch(reg))

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
		msg = 'stack depth should be {}; is {}...'
		self.display(msg.format(expected, depth))
		self.assertEqual(expected, depth)

	def assert_stack_top(self, expected):
		top = self.get_stack_top()
		msg = 'top of stack should be {}; is {}...'
		self.display(msg.format(expected, top))
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
		msg = '{} should contain {}; contains {}...'
		reg_contents = fetch(reg)
		self.display(msg.format(reg, expected, reg_contents))
		self.assertEqual(reg_contents, expected)

	# utilities #

	def get_stack_depth(self):
		with open(STACK, 'r') as stack:
			return len(stack.readlines())

	def get_stack_top(self):
		with open(STACK, 'r') as stack:
			contents = stack.readlines()

		self.assertNotEqual(contents, '')
		*tail, head = contents
		return head

	def show_stack(self):
		with open(STACK, 'r') as stack:
			stack_contents = stack.read().split('\n')
			self.display('STACK: ' + str(stack_contents))

	# general assertion 'should be'/'is' msg?

	def display(self, msg=''):
		if self.verbose:
			print(msg)


def initialize():
	clear_registers()
	clear_stack()


if __name__ == '__main__':
	unittest.main()
