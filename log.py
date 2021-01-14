from colors import YELLOW, PURPLE, RED, END


class Logger:
	def __init__(self, type, vb=False):
		self.type = type
		self.vb = vb

	def info(self, message, end_char='\n', type=None):
		if self.vb is True:
			type = type or self.type
			info = f"{YELLOW}<{type}>{END}"
			print(f"{info:16} {message}", end=end_char)

	def warning(self, message, type=None):
		type = type or self.type
		print(f"{PURPLE}<{type}> Warning: {END}{message}")

	def error(self, message, type=None):
		type = type or self.type
		print(f"{RED}<{type}> Error: {END:6}{message}")
		raise Exception("logger", message)
