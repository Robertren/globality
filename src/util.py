import argparse
from collections import Counter
from statistics import mean

def load_transactions(directory):
	"""
	Load transaction into a list of transactions
	"""
	transactions = []
	with open(directory, "r") as infile:
		for line in infile:
			transaction = line.split()
			transactions.append(transaction)
	return transactions




