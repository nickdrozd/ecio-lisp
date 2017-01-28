'''
TODO:
	* create temp files / temp dir with tempfile
	* figure out how to test eval funcs
'''

import unittest
import subprocess

from reg import *
from stack import *

class EvalTest(unittest.TestCase):

	# setup #

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.verbose = 1
		
	def setUp(self):
		initialize()
		self.display()

	def tearDown(self):
		initialize()
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
		then assign CONT to VAL
		'''
		self.assign_and_verify(VAL, 'lark')
		self.assign_and_verify(CONT, 'thrush')

		assign(VAL, fetch(CONT))
		self.assert_reg_data(VAL, 'thrush')
		self.assert_reg_data(CONT, 'thrush')


	def test_save_and_restore(self):

		self.assign_and_verify(VAL, 'cat')
		self.assign_and_verify(CONT, 'dog')

		self.assert_empty_stack()

		self.save_and_verify(VAL)
		self.save_and_verify(CONT)

		self.assert_stack_depth(2)

		self.restore_and_verify(VAL)
		self.restore_and_verify(CONT)


	# assertions #

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

	def assert_stack_top(self, data):
		top = self.get_stack_top()
		msg = 'top of stack is {}, should be {}...'
		self.display(msg.format(top, data))
		self.assertEqual(top, data)

	def assert_empty_stack(self):
		with open(STACK, 'r') as stack:
			self.assertEqual(stack.read(), '')

	def assign_and_verify(self, reg, data):
		self.display('assigning {} to {}...'.format(data, reg))
		assign(reg, data)
		self.assert_reg_data(reg, data)

	def assert_reg_data(self, reg, expected):
		msg = '{} should contain {}, contains {}...'
		reg_contents = fetch(reg)
		self.display(msg.format(reg, expected, reg_contents))
		self.assertEqual(reg_contents, expected)

	# utilities #

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



	def touch_files(self):
		self.run_cmd_on_files('touch')

	def rm_files(self):
		self.run_cmd_on_files('rm')

	def run_cmd_on_files(self, cmd):
		for file in self.files:
			subprocess.call(
				'{} {}'.format(cmd, file).split(' '))


def initialize():
	clear_registers()
	clear_stack()


if __name__ == '__main__':
	unittest.main()
