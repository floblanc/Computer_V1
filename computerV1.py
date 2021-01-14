import argparse
import re
import numpy
from log import Logger


class Equation():
	def __init__(self):
		self.equation = numpy.array([0, 0, 0])


def solve_degre_one(reduced: Equation, logger: Logger):
	res = (reduced.equation[0] * -1) / reduced.equation[1]
	print("The solution is:")
	logger.info(f"Fraction : {(reduced.equation[0] * -1)} / {reduced.equation[1]}\nDecimal : ", end='')
	print(f"{res}")


def solve_degre_two(reduced: Equation, logger: Logger):
	try:
		delta = reduced.equation[1] * reduced.equation[1] - 4 * reduced.equation[2] * reduced.equation[0]
		logger.info(f"Delta = {delta}")
		if (delta == 0):
			res = (reduced.equation[1] * -1) / (reduced.equation[2] * 2)
			print("Discriminant is equal to zero, the solution is:")
			logger.info(f"Precalculation details : {(reduced.equation[1] * -1)} / (2 * {reduced.equation[2]})")
			logger.info(f"Fraction : {(reduced.equation[1] * -1)} / {reduced.equation[2] * 2}\nDecimal : ", end_char="")
			print(f"{res}")
		else:
			if delta > 0:
				res_one = (reduced.equation[1] * -1 - square_root(delta)) / (reduced.equation[2] * 2)
				res_two = (reduced.equation[1] * -1 + square_root(delta)) / (reduced.equation[2] * 2)
				print("Discriminant is strictly positive, the two solutions are:")
				logger.info(f"Precalculation details : ({reduced.equation[1] * -1} - sqrt({delta}) / (2 * {reduced.equation[2]})")
				logger.info(f"Fraction : {(reduced.equation[1] * -1 - square_root(delta))} / {reduced.equation[2] * 2}\nDecimal : ", end_char="")
				print(f"{res_one}")
				logger.info(f"Precalculation details : ({reduced.equation[1] * -1} + sqrt({delta}) / (2 * {reduced.equation[2]})")
				logger.info(f"Fraction : {(reduced.equation[1] * -1 + square_root(delta))} / {reduced.equation[2] * 2}\nDecimal : ", end_char="")
				print(f"{res_two}")
			else:
				res_three = (reduced.equation[1] * -1) / (reduced.equation[2] * 2)
				res_four = square_root(delta * -1) / (reduced.equation[2] * 2)
				print("Discriminant is strictly negative, there is no real solution but there is two non-real solution:")
				logger.info(f"Precalculation details : {reduced.equation[1] * -1} / (2 * {reduced.equation[2]}) - i(sqrt({-delta}) / (2 * {reduced.equation[2]}))")
				logger.info(f"Fraction : {reduced.equation[1] * -1} / {reduced.equation[2] * 2} - i(sqrt({delta}) / {reduced.equation[2] * 2})\nDecimal : ", end_char="")
				print(f"{res_three} - i({res_four})")
				logger.info(f"Precalculation details : {reduced.equation[1] * -1} / (2 * {reduced.equation[2]}) + i(sqrt({-delta}) / (2 * {reduced.equation[2]}))")
				logger.info(f"Fraction : {reduced.equation[1] * -1} / {reduced.equation[2] * 2} + i(sqrt({delta}) / {reduced.equation[2] * 2})\nDecimal : ", end_char="")
				print(f"{res_three} + i({res_four})")
	except Exception as e:
		print(e)


def print_reduced_form(reduc: Equation, degree):
	print("Reduced form: ", end="")
	print(reduc.equation[0], end="")
	print(f" + {reduc.equation[1]} * X", end="")
	if degree == 2:
		print(f" + {reduc.equation[2]} * X^2", end="")
	print(" = 0")


def solve(left, right, vb):
	logger = Logger("Solver", vb)
	reduced = Equation()
	for it in range(3):
		reduced.equation[it] = left.equation[it] - right.equation[it]
	if (reduced.equation[2] != 0):
		print_reduced_form(reduced, 2)
		print("Polynomial degree : 2")
		solve_degre_two(reduced, logger)
	elif (reduced.equation[1] != 0):
		print_reduced_form(reduced, 1)
		print("Polynomial degree : 1")
		solve_degre_one(reduced, logger)
	else:
		print("Polynomial degree : 0")
		print("There is no solutions for degree 0.")


def parsing(eq_content, vb):
	logger = Logger("Parsing", vb)
	logger.info("Analysing equation syntax.")
	eq_content = eq_content.replace(" ", "")
	if (eq_content == ""):
		logger.error("Equation is empty.")
	regex = re.compile(r'[^-+=^*/.xX0-9]')
	if regex.match(eq_content) is not None:
		logger.error("Some invalid characters detected.")
	if ("//" in eq_content or "**" in eq_content or "/*" in eq_content or "*/" in eq_content
			or "+/" in eq_content or "-/" in eq_content or "+*" in eq_content or "-*" in eq_content
			or "/+" in eq_content or "/-" in eq_content or "*+" in eq_content or "*-" in eq_content
			or "=+" in eq_content or "=*" in eq_content or "=/" in eq_content or "==" in eq_content
			or not ((eq_content[0]).isalpha() or (eq_content[0]).isdigit() or (eq_content[0]) == "+" or (eq_content[0]) == "-")):
		logger.error("Invalid operator sequence")
	eq_content = eq_content.replace("x", "X")
	while ("--" in eq_content or "++" in eq_content or "-+" in eq_content or "+-" in eq_content):
		eq_content = (
			eq_content.replace("--", "+")
			.replace("++", "+")
			.replace("+-", "-")
			.replace("-+", "-")
		)
	eq_content = eq_content.replace("*", "*/")
	equation = eq_content.split("=")
	if (len(equation) != 2):
		logger.error("Wrong equal symbols number.")
	left = None
	right = None
	for part in equation:
		part = part.replace("-", "+-")
		subparts = part.split("+")
		equation = Equation()
		for subpart in subparts:
			multsubparts = subpart.split("*")
			degre = 0
			value = 1
			for it in range(len(multsubparts)):
				div = 1
				if (multsubparts[it][0] == '/'):
					div = -1
					multsubparts[it] = multsubparts[it][1:]
				if ("X" in multsubparts[it]):
					if ("X^" not in multsubparts[it]):
						multsubparts[it] = multsubparts[it].replace("X", "X^1")
					try:
						int(multsubparts[it][2:])
					except Exception:
						logger.error(f"Syntax error : '{multsubparts[it][2:]}' isn't an integer to use as X power.")
					degre += int(multsubparts[it][2:])
				elif div == 1:
					value *= float(multsubparts[it])
				else:
					value /= float(multsubparts[it])
			if (degre > 2 or degre < 0):
				logger.error(f"Bad polynomial degree : {degre}")
			equation.equation[degre] += value
		if left is None:
			left = equation
		else:
			right = equation
	logger.info("Syntax approuved.")
	return left, right


def square_root(num):
	if num < 0:
		return None
	if num == 1 or num == 0:
		return float(num)
	sqrt = num / 2
	if (sqrt < 2):
		sqrt = 2.0
	diff = sqrt * sqrt - num
	decrem = 1
	while decrem < sqrt:
		decrem *= 10
	decrem *= 0.1
	while decrem > 0.0000000000001 and (diff > 0.0000000000001 or diff < -0.0000000000001):
		if decrem >= sqrt or diff < 0:
			sqrt += decrem
			decrem /= 10
		sqrt -= decrem
		diff = sqrt * sqrt - num
	return sqrt


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="ComputerV1")
	parser.add_argument("equation", help="polynomial equation")
	parser.add_argument("-vb", "--verbose", action="store_true", help="Enable verbose")
	args = parser.parse_args()
	logger = Logger("Main", args.verbose)
	try:
		left, right = parsing(args.equation, args.verbose)
		solve(left, right, args.verbose)
	except Exception:
		pass
	