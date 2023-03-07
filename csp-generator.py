from spec import specs
import csv
import time

TOTAL_NODES_LENGTH = 12000 #millimeters

file = open("states.csv", "w")
writer = csv.writer(file)

ntypes = [{
    "len": 0,
    "kook": None
}]

invalid_counter = 0
valid_counter = 0

for kook, spec in specs.items():
    ntypes.append({
        "len": spec["len"],
        "kook": kook
    })

def conbination_is_valid(state):
	sum = 0
	for ntype in state:
		sum += ntype["len"]
	if sum > TOTAL_NODES_LENGTH or sum == 0:
		return False
	else:
		return True
	
# Python3 program to print all combination
# of size r in an array of size n

''' arr[] ---> Input Array
	chosen[] ---> Temporary array to store
			current combination
	start & end ---> Starting and Ending indexes in arr[]
	r---> Size of a combination to be printed

	'''
def CombinationRepetitionUtil(chosen, arr, index,
							r, start, end):
								
	# Current combination is ready,
	# print it
	global invalid_counter
	global valid_counter
	global writer
	if index == r:
		state = []
		for j in range(r):
			state.append(chosen[j])
			#print(chosen[j], end = " ")
		if conbination_is_valid(state):
			valid_counter += 1
			writer.writerow([s["kook"] for s in state if s["len"] > 0])
		else:
			invalid_counter += 1
		if (valid_counter + invalid_counter) % 500000 == 0:
			print("So far, valids : ", valid_counter, " - invalids: ", invalid_counter)
			time.sleep(15)

		return
		
	# When no more elements are
	# there to put in chosen[]
	if start > n:
		return
		
	# Current is included, put
	# next at next location
	chosen[index] = arr[start]
	
	# Current is excluded, replace it
	# with next (Note that i+1 is passed,
	# but index is not changed)
	CombinationRepetitionUtil(chosen, arr, index + 1,
							r, start, end)
	CombinationRepetitionUtil(chosen, arr, index,
							r, start + 1, end)

# The main function that prints all
# combinations of size r in arr[] of
# size n. This function mainly uses
# CombinationRepetitionUtil()
def CombinationRepetition(arr, n, r):
	
	# A temporary array to store
	# all combination one by one
	chosen = [0] * r

	# Print all combination using
	# temporary array 'chosen[]'
	CombinationRepetitionUtil(chosen, arr, 0, r, 0, n)

# Driver code
arr = ntypes
r = 30
n = len(arr) - 1

CombinationRepetition(arr, n, r)

# This code is contributed by Vaibhav Kumar 12.

print("Finished, valids : ", valid_counter, " - invalids: ", invalid_counter)

file.close()
