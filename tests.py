import unittest
import subprocess

from reg import *
from stack import *

class EvalTest(unittest.TestCase):

	# setup #

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.verbose = 0

		self.reg1 = 'TEST_REG1'
		self.reg2 = 'TEST_REG2'
		self.stack = 'TEST_STACK'
		self.files = self.reg1, self.reg2, self.stack
		
	def setUp(self):
		self.touch_files()

	def tearDown(self):
		self.rm_files()

	# tests #

	def test_assign_and_fetch(self):
		'''
		Assign several words to reg1.
		'''
		for animal in 'cow', 'sheep', 'pig':
			self.assign_and_verify(self.reg1, animal)


	def test_assign_one_reg_to_another(self):
		'''
		Assign distinct data to reg1 and reg2, 
		then assign reg2 to reg1
		'''
		reg1, reg2 = self.reg1, self.reg2


		self.assign_and_verify(reg1, 'lark')
		self.assign_and_verify(reg2, 'thrush')

		assign(self.reg1, fetch(self.reg2))
		self.assert_reg_data(reg1, 'thrush')
		self.assert_reg_data(reg2, 'thrush')


	def test_save_and_restore(self):
		reg1, reg2 = self.reg1, self.reg2

		self.assign_and_verify(reg1, 'cat')
		self.assign_and_verify(reg2, 'dog')

		self.assert_empty_stack()

		self.save_and_verify(reg1)
		self.save_and_verify(reg2)

		self.assert_stack_depth(2)

		self.restore_and_verify(reg1)
		self.restore_and_verify(reg2)


	# assertions #

	def save_and_verify(self, reg):
		depth = self.get_stack_depth()
		save(reg, self.stack)
		self.show_stack()
		self.assert_stack_depth(depth + 1)
		self.assert_stack_top(fetch(reg))

	def restore_and_verify(self, reg):
		depth = self.get_stack_depth()
		top = self.get_stack_top()
		restore(reg, self.stack)
		self.show_stack()
		self.assert_reg_data(reg, top)
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

	def get_stack_depth(self):
		with open(self.stack, 'r') as stack:
			return len(stack.readlines())

	def get_stack_top(self):
		with open(self.stack, 'r') as stack:
			data = stack.read()
			self.assertNotEqual(data, '')
			# last item in read().split('\n') is empty string?
			return data.split('\n')[-1]			

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

	def show_stack(self):
		with open(self.stack, 'r') as stack:
			stack_contents = stack.read().split('\n')
			self.display('STACK: ' + str(stack_contents))

	def display(self, msg):
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
