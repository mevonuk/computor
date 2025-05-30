from variable import Variable

def get_value(value, history):
	if value in history:
		result = history[value]
		if isinstance(result, str):
			result = get_value(result, history)
		if isinstance(result, Variable):
			result = result.value
		return result
	# print(value + " is not defined")
	return None

def get_value2(value, history):
	if value in history:
		result = history[value]
		if isinstance(result, str):
			result = get_value2(result, history)
		if isinstance(result, Variable):
			result = result.value
		return result
	# print(value + " is not defined")
	return value