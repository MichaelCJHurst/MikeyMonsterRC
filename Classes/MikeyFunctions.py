"""
Miscellaneous functions I tend to use alot
v 1.1 - added MikeyResult class
"""
import os

class MikeyResult(object):
	""" Used for different APIs or classes interacting with each other """
	def __init__(self, success = False, error_msg = None, errors = (), result = None):
		""" Sets up the result """
		self.success   = success
		self.error_msg = error_msg
		self.errors    = errors
		self.result    = result

def mikeyresult_success(result = None):
	""" Populates the MikeyResult with a success """
	return MikeyResult(True, None, None, result)

def mikeyresult_error(error_msg, errors = ()):
	""" Populates the MikeyResult with an error """
	return MikeyResult(False, error_msg, errors, None)

def absolute_path(path):
	""" Returns an absolute path """
	return os.path.abspath(
		os.path.join(
			os.path.dirname(__file__),
			"..",
			path
		)
	)
