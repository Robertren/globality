import argparse
from collections import Counter
from statistics import mean

def raw_data_information(directory):
	product_counter = Counter()
	transaction_counter = 0
	with open(directory, "r") as infile:
		for line in infile:
			line = line.split()
			transaction_counter += 1
			product_counter.update(line)
			if transaction_counter == 1:
				print ("Here is a sample for the data:")
				print ("=========================================")
				print (line)
	print("Here are the information of our data:")
	print("=========================================")
	print("There are totally {0} transactions.".format(str(transaction_counter)))
	print("There are {0} kinds of product.".format(str(len(product_counter.keys()))))
	print("The most frequent product appear {0} times.".format(max(product_counter.values()))) 
	print("The mean appearance times of product is {0} times.".format(str(mean(product_counter.values()))))


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_directory', type=str, default="../data/retail_25k.dat")
	args = parser.parse_args()
	raw_data_information(args.data_directory)