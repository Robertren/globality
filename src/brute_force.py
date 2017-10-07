#/usr/bin/python
# -*- coding: utf-8 -*-
"""

Requirements::
    1.  You will need to install the tqdm library to run this code.
""" 
from util import load_transactions
from collections import Counter
from itertools import combinations
import argparse
from tqdm import tqdm

def iterate_product_counter(transactions, itemset_size):
	# Iterate for all transactions and count the combinations for different itemset_size
	product_counter = Counter()
	print("Iteration for item size {}".format(str(itemset_size)))
	for transaction in tqdm(transactions):
		if len(transactions) < itemset_size:
			continue
		items_keys = set(combinations(transaction, itemset_size))
		product_counter.update(items_keys)
	return product_counter

def filter_product_counter(product_counter, support):
	"""
		This function filters out all the itemset which count is below to support
	"""
	return {key: product_counter[key] for key in product_counter.keys() if product_counter[key] >= support}

def write_to_file(log, filtered_product_counter):
	"""
		This function is used to print results to the required format.
		Args:
			log(file) - opened file which records the record
			filtered_product(dictionary) - A dictionary, the key is frequent itemset 
			and the value is the time of appearance of this frequent itemset.
        Returns: 
        	None
	"""
	for freq_item_set in filtered_product_counter:
			freq_item_list = [item for item in freq_item_set]
			items = ",".join(freq_item_list)
			line = str(itemset_size) + "," + str(filtered_product_counter[freq_item_set])+ "," + items
			log.write(line + '\n')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_directory', type=str, default="../data/retail_25k.dat")
	parser.add_argument('--log_directory', type=str, default="../data/result_log_compare.dat")
	parser.add_argument('--support', type=int, default=4)
	parser.add_argument('--size_threshold', type=int, default=3)
	args = parser.parse_args()
	itemset_size = args.size_threshold
	log = open(args.log_directory, "w")
	transactions = load_transactions(args.data_directory)
	product_counter = iterate_product_counter(transactions, itemset_size)
	filtered_product_counter = filter_product_counter(product_counter, args.support)
	write_to_file(log, filtered_product_counter)

	print ("For itemsize{0}, the counter size is {1}".format(str(itemset_size), str(len(filtered_product_counter))))
	while filter_product_counter:
		itemset_size += 1
		product_counter = iterate_product_counter(transactions, itemset_size)
		filtered_product_counter = filter_product_counter(product_counter, args.support)
		write_to_file(log, filtered_product_counter)
		print ("For itemsize{0}, the counter size is {1}".format(str(itemset_size), str(len(filtered_product_counter))))