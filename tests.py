import unittest

from reg import *
from stack import *
from instr import *

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

	# tests #

	def test_assign_and_fetch(self):
		'''
		Assign several words to VAL.
		'''
		for animal in 'cow', 'sheep', 'pig':
			self.assign_and_verify(VAL, animal)


	def test_assign_one_reg_to_another(self):
		'''
		Assign distinct data to VAL and CONT, 
		then assign CONT to VAL.
		'''
		self.assign_and_verify(VAL, 'lark')
		self.assign_and_verify(CONT, 'thrush')

		assign(VAL, fetch(CONT))
		self.assert_reg_data(VAL, 'thrush')
		self.assert_reg_data(CONT, 'thrush')


	def test_save_and_restore(self):
		'''
		Assign to VAL and CONT, save from both, 
		then assign back to them in reverse order.
		'''
		self.assign_and_verify(VAL, 'cat')
		self.assign_and_verify(CONT, 'dog')

		self.assert_empty_stack()

		self.save_and_verify(VAL)
		self.save_and_verify(CONT)

		self.assert_stack_depth(2)

		self.restore_and_verify(VAL)
		self.restore_and_verify(CONT)

		self.assert_empty_stack()


	def test_goto(self):
		self.goto_and_verify('quince')
		self.goto_continue_and_verify('fig')
		self.goto_eval_and_verify()


	# assertions #

	def goto_eval_and_verify(self):
		goto_eval()
		self.assert_reg_data(INSTR, EVAL_EXP)

	def goto_continue_and_verify(self, label):
		self.set_continue_and_verify(label)
		goto_continue()
		self.assert_reg_data(INSTR, label)

	def set_continue_and_verify(self, label):
		set_continue(label)
		self.assert_reg_data(CONT, label)

	def goto_and_verify(self, label):
		goto(label)
		self.assert_reg_data(INSTR, label)

	def save_and_verify(self, reg):
		self.display('saving from {}...'.format(reg))
		depth = self.get_stack_depth()
		save(reg)
		self.show_stack()
		self.assert_stack_depth(depth + 1)
		self.assert_stack_top(fetch(reg))

	def restore_and_verify(self, reg):
		self.display('restoring to {}...'.format(reg))
		depth = self.get_stack_depth()
		top = self.get_stack_top()
		restore(reg)
		self.assert_reg_data(reg, top)
		self.show_stack()
		self.assert_stack_depth(depth - 1)

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

	def assign_and_verify(self, reg, data):
		self.display('assigning {} to {}...'.format(data, reg))
		assign(reg, data)
		self.assert_reg_data(reg, data)

	def assert_reg_data(self, reg, expected):
		msg = '{} should contain {}; contains {}...'
		reg_contents = fetch(reg)
		self.display(msg.format(reg, expected, reg_contents))
		self.assertEqual(reg_contents, expected)

	# utilities #

	# general assertion 'should be'/'is' msg?

	def get_stack_depth(self):
		with open(STACK, 'r') as stack:
			return len(stack.readlines())

	def get_stack_top(self):
		with open(STACK, 'r') as stack:
			data = stack.read()
			self.assertNotEqual(data, '')
			return data.split('\n')[-1]			

	def show_stack(self):
		with open(STACK, 'r') as stack:
			stack_contents = stack.read().split('\n')
			self.display('STACK: ' + str(stack_contents))

	def display(self, msg=''):
		if self.verbose:
			print(msg)


def initialize():
	clear_registers()
	clear_stack()


if __name__ == '__main__':
	unittest.main()
