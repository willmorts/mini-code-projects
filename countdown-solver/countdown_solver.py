class CountdownObject():
	def __init__(self, list_nums, target):
		self._list_nums = list_nums # e.g. [1,2,3,4]
		self._target = target
		self._permutations = [list_nums.copy()] # list of lists, all possible permutations of original list, e.g. [[1,5,7],[2,4,3]...], starts as original list of nums
		self._solutions = [[""] *len(list_nums)] #list of lists, tracker of solutions to get to each permutaiton, e.g. [[1,2+3,7],[1+1,2*2,3]..]

	# handy debug
	def get_permutations(self):
		return self._permutations
	def get_solutions(self):
		return self._solutions

	# operators take tuple of two numbers, and string of solution so far
	# return tuple of new number and update solution
	def _stringify_op(self, num1, num2, sol1, sol2, op_str, result):
		return (str(num1) +op_str +str(num2) +"=" +str(result) +"\r\n" +sol1 +sol2)
	def _countdown_add(self, num1, num2, sol1, sol2):
		# add the numbers, order doesn't matter so just concat the current solution with "+" and the other solution
		return (num1+num2), self._stringify_op(num1,num2,sol1,sol2,"+",num1+num2)
	# No point in getting negative numbers in countdown, so don't have to look back in list, and can just pick the subtraction that makes sense
	def _countdown_subtract(self, num1, num2, sol1, sol2):
		if (num1 == num2):
			return None, None
		elif (num1 > num2):
			return (num1-num2), self._stringify_op(num1,num2,sol1,sol2,"-",num1-num2)
		else:
			return (num2-num1), self._stringify_op(num2,num1,sol1,sol2,"-", num2-num1)
	def _countdown_multiply(self, num1, num2, sol1, sol2):
		# multiply the numbers, order doesn't matter so just concat the current solution with "+" and the other solution
		return (num1*num2), self._stringify_op(num1,num2,sol1,sol2,"*",num1*num2)
	def _countdown_divide(self, num1, num2, sol1, sol2):
		if (num1 == 0) or (num2 == 0):
			return None, None
		if (num1 > num2):
			if (num1 % num2 == 0):
				return (num1 // num2), self._stringify_op(num1,num2,sol1,sol2,"/",num1//num2)
		else:
			if (num2 % num1 == 0):
				return (num2 // num1), self._stringify_op(num2,num1,sol1,sol2,"/",num2//num1)

		return None, None

	# permutate the _permutations list once and update _solutions
	def permutate(self):
		operators = [self._countdown_add, self._countdown_subtract, self._countdown_multiply, self._countdown_divide]

		new_permutations = [] # will be the new list, as will permutate and delete the original
		new_solutions = []
		# go through each permutation
		for index,permutation in enumerate(self._permutations):
			# if permutation already contains solutions, just append it onto the new_permutations
			temp1,temp2 = _check_solutions(permutation, self._target)
			if (temp1 == True):
				new_permutations.append(permutation.copy())
				new_solutions.append(self._solutions[index].copy())
				continue
			# then perform each operation
			for op in operators:
				# for each number in _permutations
				for i in range(0, len(permutation)):
					# for each number after current i number:
					for j in range((i+1), len(permutation)):
						temp_perm = permutation.copy()
						temp_solutions = self._solutions[index].copy()

						# make the i value the result of operating on it against the j value, then remove the j value
						# e.g. [2,3,4] could multiply 2 and 3 to get [6,3,4] then remove j so 3 can't be used again to get [6,4]
						temp_perm[i], temp_solutions[i] = op(temp_perm[i], temp_perm[j], temp_solutions[i], temp_solutions[j])
						temp_perm.pop(j)
						temp_solutions.pop(j)

						# if the new value is valid, update the permutations list
						if (temp_perm[i] != None):
							new_permutations.append(temp_perm)
							new_solutions.append(temp_solutions)

		# finally update the _permutations and _solutions trackers
		self._permutations = new_permutations.copy()
		self._solutions = new_solutions.copy()

	# to be called at end - returns index of any permutations with a valid solution, and index of where the solution is within that list
	def return_solutions(self):
		successful_solutions = []
		for index,permutation in enumerate(self._permutations):
			temp1,temp2 = _check_solutions(permutation, self._target)
			if (temp1 == True):
				# we have a successful solution, check it's not already in the list:
				unique_solution = True
				for soln in successful_solutions:
					if (self._solutions[index][temp2] == self._solutions[soln[0]][soln[1]]):
						# not unique, don't add
						unique_solution = False
						break
				if (unique_solution):
					successful_solutions.append([index,temp2])

		return successful_solutions


# checks if there's a valid solution within your list of nums, returns true if there is, and where the valid solution is
def _check_solutions(list_nums, goal):
	for index, each in enumerate(list_nums): 
		if each == goal:
			return True,index
	return False, 0

if __name__=='__main__':
	# inputs = [75, 10, 4, 6, 9, 6]
	inputs = [1,2,3]
	goal = 675
	temp = CountdownObject(inputs, goal)
	# permutate the length of the list -1 to get down to list of 1s and solutions
	for i in range(0,(len(inputs))-1):
		temp.permutate()

	successful_solutions = temp.return_solutions()
	print("Input numbers: " +str(inputs))
	print("Goal: " +str(goal))
	print("\r\n")
	print("Total solutions: " +str(len(successful_solutions)))
	for i,each in enumerate(successful_solutions):
		print("Solution " +str(i+1))
		print(temp._solutions[each[0]][each[1]])
