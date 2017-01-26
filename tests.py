import unittest
import subprocess

from reg import *

class EvalTest(unittest.TestCase):
	def setUp(self):
		self.verbose = 1
		self.test_reg = 'TEST'
		subprocess.call('touch TEST'.split(' '))

	def tearDown(self):
		subprocess.call('rm TEST'.split(' '))

	def test_reg(self):
		data = 'hello'
		self.assign_and_verify(self.test_reg, data)

	def assign_and_verify(self, reg, data):
		self.display('assigning {} to {}...'.format(data, reg))
		assign(self.test_reg, data)
		self.display('fetching from {}...'.format(reg))
		self.assert_reg(self.test_reg, data)

	def assert_reg(self, reg, data):
		self.assertEqual(fetch(reg), data)

	def display(self, msg):
		if self.verbose:
			print(msg)

if __name__ == '__main__':
	unittest.main()