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
	"""
		Iterate all the transactions and get new itemset with size equal to itemset_size. And get a new item counter, the key for
		this counter equals to itemset_size. And also get the new transactions_dict for reconstructing the transactions.
		Args:
			transactions(list) - A list which contains all transactions.
			itemset_size(int) - current itemsize
        Returns: 
        	product_counter(Counter) - A counter which counts the time of appearance of current frequent item set(with size of itemset_size).
			transactions_dict - A dictionary which stores all the item set(with size of itemset_size) for each transaction.
	"""
	transactions_dict = {}
	product_counter = Counter()
	print("Iteration for item size {}".format(str(itemset_size)))
	for index in tqdm(range(len(transactions))):
		items_keys = set(combinations(transactions[index], 2))
		if itemset_size != 2:
			items_keys = generate_key(items_keys, itemset_size)
		transactions_dict[index] = items_keys
		product_counter.update(items_keys)
	return product_counter, transactions_dict

def generate_key(items_keys, itemset_size):
	"""
		Generate a set of new itemsets which the size is itemset_size.
		Args:
			items_keys(set) - A set of all possible combinations (size 2) of current transaction
			itemset_size(int) - current itemsize
        Returns: 
        	new_keys(set) - A set of new itemsets which the size of the new itemsets is itemset_size
	"""
	new_keys = set([frozenset(key[0]).union(key[1]) for key in items_keys if len(set(key[0]).union(key[1])) == itemset_size])
	return new_keys

def reconstruct_transactions(transactions_dict, filtered_product_counter):
	"""
		This function reconstruct transactions after each iteration to speed up the algorithm. 
		For each record in the transactions_dict, this function will filter out the frequent itemset which doesn't appear 
		in the filtered_product_counter.
		Args:
			transactions_dict(dictionary) - 
			filtered_product_counter(dictionary) - A dictionary, the key is frequent itemset 
			and the value is the time of appearance of this frequent itemset.
        Returns: 
        	new_transactions(list) - A list of list, for each transaction in the list, it contains filtered itemset.
	"""
	new_transactions = []
	for index in transactions_dict:
		new_transaction = [item_set for item_set in transactions_dict[index] if item_set in filtered_product_counter]
		if len(new_transaction) != 0:
			new_transactions.append(new_transaction)
	return new_transactions

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
			filtered_product_counter(dictionary) - A dictionary, the key is frequent itemset 
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
	parser.add_argument('--log_directory', type=str, default="../data/result_log.dat")
	parser.add_argument('--support', type=int, default=4)
	parser.add_argument('--size_threshold', type=int, default=3)
	args = parser.parse_args()
	log = open(args.log_directory, "w")
	itemset_size = 2
	# Load all the data
	transactions = load_transactions(args.data_directory)
	# Get and filter the product counter
	product_counter, transactions_dict = iterate_product_counter(transactions, itemset_size)
	filtered_product_counter = filter_product_counter(product_counter, args.support)
	# Reconstruct transactions based on the results we got.
	transactions = reconstruct_transactions(transactions_dict, filtered_product_counter)
	# Keep iterating until there is no transaction in the transaction list.
	while transactions:
		itemset_size += 1
		product_counter, transactions_dict = iterate_product_counter(transactions, itemset_size)
		filtered_product_counter = filter_product_counter(product_counter, args.support)
		transactions = reconstruct_transactions(transactions_dict, filtered_product_counter)
		if itemset_size >= args.size_threshold:
			# Write to file.
			write_to_file(log, filtered_product_counter)
		print ("For itemsize{0}, the counter size is {1}".format(str(itemset_size), str(len(filtered_product_counter))))