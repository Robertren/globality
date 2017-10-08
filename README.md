# Globality code challenge

In this project, You are given as input:
* A transaction database - a file consisting of a single row per transaction, with individual product's SKUs given as space–separated integers. A single transaction consisting of products with SKUs 1001, 1002 and 1003 would have a line that looks like: ‘1001 1002 1003' 
* A minimal ’support level’ parameter, sigma – a positive integer 

An efficient algorithm for generating all frequent item sets of size 3 or more: groups of 3 or more items that appear together in the transactions log at least as often as the support level parameter value. For example, given a value of sigma = 2, all sets of 3 items that appear 2 or more times together in the transaction log should be returned.

Run the algorithm on the attached transaction log file and provide the results obtained for a value of sigma = 4
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This projects is written in python3. As a result, it is necessary have a python3 in your enviroments.Here is the link to install it [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installing

Because this project takes sometime to do calculation, tqdm is a good tool to track the program.
```
pip install tqdm
```
### Data Understanding

In order to better understand the data we are working on, author wrote a script to get some basic statics of the data which may help for the next step. To run the code:
```
cd src
python data_analysis.py
```
The result we get shows:
> Here is a sample for the data:

>['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29']

>Here are the information of our data:

>There are totally 25000 transactions.

>There are 11427 kinds of product.

>The most frequent product appear 14198 times.

>The mean appearance times of product is 22.65432747002713 times.

## Algorithm brief introduction 

This part will introduce three algorithms author have tried to solve this problem and the problem which arosed during the implementation.

### Brute force
To start with, author tried most straightforward approach.The idea is use combinations in python itertools to get all possible combinations with different size in each of the transaction. And after get all combinations, we count all the combinations, then filter out those whose support is less than 4. 

To run the code:
``` 
cd src
python brute_force.py  
```
* problem for this method: the combination method will be very slow when increase the item size. As a matter of fact, this code can not finish the task because the os will kill the process.This method only works well when itemsize is 3 and 4 (will get killed for size 5). Hence, we need to find a way to speed it up. 

### Apriori algorithm

After the first method, author did some research on frequent itemset problems and found an algorithm called [Apriori algorithm](https://www3.cs.stonybrook.edu/~cse634/lecture_notes/07apriori.pdf) (please click the link for more details). This method is bascially keeping iterating to increase the size of frequent itemset and the items are the combinations of previous itemset. Also, it will filter out those whose number of occurrence is less than threshold.

To run the code:
```
cd src                  #if you already in /src, you can omit this
python apriori.py 
```
* problem for this method: after the experiment, this method doesn't work well for the whole set because there are so many frequent itemset, and everytime when we want to get candiate keys for next level. It will be extremely expensive. It will take a long time to run the code.

### Updated Apriori algorithm(original)
In order to decrease the times of calculate next level candidate keys, author proposed a new way to find frequent itemset. After one iteration, this method will reconstruct all transactions based on frequent itemset for now. Also the candidated is calculated when iterate each of the transaction. The rest part for this method is similar to Apriori. This method will decrease the size of candidate keys significantly since it is only caculated on transaction lever instead of the whole dataset level.

To run the code:
```
cd src                        #if you already in /src, you can omit this
python final_aprior.py 
```
* This method works well and takes about 20-25 minutes depending on the computer.

NOTE: For parameters of the code, please refer to the source code.

## Evaluation
In order to evaluate the performance of author's algorithm. Author tried two ways
* Compare with brute force method
Since brute force method works really well for item set size 3 and 4. Author compared the brute force results with the results after running the final_aprior method and get the same results for size 3 and 4.
* Choose special sample
The longest frequent item set size is 14, the count for this item set is 4.
The ids for this set are  [38,3330,272,932,48,1143,905,987,1103,2951,3336,65,32,39.]
Run code:
```sh
cd ../data
awk "/38/&&/3330/&&/272/&&/932/&&/48/&&/1143/&&/905/&&/987/&&/1103/&&/2951/&&/3336/&&/65/&&/32/&&/39/" retail_25k.dat 
```

we got 4 lines of results, which means this method work well for longest frequent itemset in the transactions.


* The result can be found in data/result_log.dat in required format:
```
<item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, …. <item N id>
```
## Authors

* **Zizhuo Ren** 

## Acknowledgments

* Get inspired from asaini's code [Apriori](https://github.com/asaini/Apriori)


