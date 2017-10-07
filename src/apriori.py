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

def initialize_product_counter(transactions):
	# Three iter size 
	product_counter = Counter()
	for transaction in tqdm(transactions):
		two_items_keys = set(combinations(transaction, 2))
		product_counter.update(two_items_keys)
	return product_counter

def filter_candidate_keys(product_counter, support):
	return [key for key in product_counter.keys() if product_counter[key] >= support]

def generate_candidate_keys(current_keys, itemset_size):
	raw_candidate_keys = set([set(i).union(j) for i in current_keys for j in current_keys if len(set(i).union(j)) == itemset_size])
	return candidate_keys

def generate_product_counter(transactions, candidate_keys):
	product_counter = Counter()
	for transaction in tqdm(transactions):
		update_list = [key for key in candidate_keys if set(key) <= set(transaction)]
		product_counter.update(update_list)
	return product_counter


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_directory', type=str, default="../data/retail_25k.dat")
	parser.add_argument('--support', type=int, default=4)
	parser.add_argument('--size_threshold', type=int, default=2)
	itemset_size = 2
	args = parser.parse_args()
	transactions = load_transactions(args.data_directory)
	product_counter = initialize_product_counter(transactions)
	filtered_keys = filter_candidate_keys(product_counter, args.support)
	print (filtered_keys[0:100])
	while filtered_keys:
		print (len(filtered_keys))
		print("start generate_candidate_keys")
		itemset_size += 1
		candidate_keys = generate_candidate_keys(filtered_keys, itemset_size)
		print("start generate_product_counter")
		product_counter = generate_product_counter(transactions, candidate_keys)
		filtered_keys = filter_candidate_keys(product_counter, args.support)
		if itemset_size > args.size_threshold:
			for i in filtered_keys:
				print (product_counter[i])
