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

		files = ('test_expr', 'test_val', 
				'test_env', 'test_unev', 
				'test_func', 'test_argl', 
				'test_cont', 'test_stack')

		(self.expr, self.val, self.env,
		self.unev, self.func, self.argl, 
		self.cont, self.stack) = files

		self.files = files
		
	def setUp(self):
		self.touch_files()
		self.display()

	def tearDown(self):
		self.rm_files()
		self.display()

	# tests #

	def test_assign_and_fetch(self):
		'''
		Assign several words to val.
		'''
		for animal in 'cow', 'sheep', 'pig':
			self.assign_and_verify(self.val, animal)


	def test_assign_one_reg_to_another(self):
		'''
		Assign distinct data to val and cont, 
		then assign cont to val
		'''
		val, cont = self.val, self.cont


		self.assign_and_verify(val, 'lark')
		self.assign_and_verify(cont, 'thrush')

		assign(self.val, fetch(self.cont))
		self.assert_reg_data(val, 'thrush')
		self.assert_reg_data(cont, 'thrush')


	def test_save_and_restore(self):
		val, cont = self.val, self.cont

		self.assign_and_verify(val, 'cat')
		self.assign_and_verify(cont, 'dog')

		self.assert_empty_stack()

		self.save_and_verify(val)
		self.save_and_verify(cont)

		self.assert_stack_depth(2)

		self.restore_and_verify(val)
		self.restore_and_verify(cont)


	# assertions #

	def save_and_verify(self, reg):
		self.display('saving from {}...'.format(reg))
		depth = self.get_stack_depth()
		save(reg, self.stack)
		self.show_stack()
		self.assert_stack_depth(depth + 1)
		self.assert_stack_top(fetch(reg))

	def restore_and_verify(self, reg):
		self.display('restoring to {}...'.format(reg))
		depth = self.get_stack_depth()
		top = self.get_stack_top()
		restore(reg, self.stack)
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
		with open(self.stack, 'r') as stack:
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
		with open(self.stack, 'r') as stack:
			return len(stack.readlines())

	def get_stack_top(self):
		with open(self.stack, 'r') as stack:
			data = stack.read()
			self.assertNotEqual(data, '')
			return data.split('\n')[-1]			

	def show_stack(self):
		with open(self.stack, 'r') as stack:
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


if __name__ == '__main__':
	unittest.main()
