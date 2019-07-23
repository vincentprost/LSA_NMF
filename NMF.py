#!/usr/bin/env python

import sys, getopt
import glob, os
import numpy as np
import spams
import multiprocessing
import argparse


n = 10
cpu = 42
clusters_nb = 1
thres = 0
wd = ""




parser = argparse.ArgumentParser(description='Optional app description')


parser.add_argument('-i', '--inputdir',  type=str,
                    help='input folder')


parser.add_argument('-o', '--outputdir', type=str,
                    help='output folder')


parser.add_argument('-cn', '--cluster_number', type=int, default = 200,
                    help='output folder')


parser.add_argument('-l1', '--lambda1', type=float, default=0.1,
                    help='output folder')


parser.add_argument('-l2', '--lambda2', type=float, default=0.05,
                    help='output folder')

parser.add_argument('-p', '--cpu', type=int, default=1,
                    help='output folder')






iter_nb = 1000
batchsize = 100
memory_limit = 8e9 # bytes


args = parser.parse_args()



f= open(args.outputdir + "/numClusters.txt","w")
f.write(str(args.cluster_number))
f.close()




Kmer_Hash_Count_Files = glob.glob(os.path.join(args.inputdir,'*.count.hash.conditioned'))
hash_size = int(np.log( os.path.getsize(Kmer_Hash_Count_Files[0]) / 4) / np.log(2))
print("hash_size = " + str(hash_size))

n = len(Kmer_Hash_Count_Files)

global_nonzeros = np.load(args.outputdir + "/" + "global_nonzeros.npy")
global_nonzero_indices = np.nonzero(global_nonzeros)[0]
nzi = np.shape(global_nonzero_indices)[0]

del global_nonzeros




submatrix_size = int(memory_limit / (4 * (args.cluster_number + n)))
print(submatrix_size) 
print(nzi)




print("dictionnary learning...")
submatrix_iterations =  int(iter_nb * batchsize / (0.2 * submatrix_size)) + 1
submatrix_size = min(nzi, submatrix_size)
print("submatrix iteration : " + str(submatrix_iterations))


submatrix = np.asfortranarray(np.zeros((n, submatrix_size), dtype = np.float32))

D = None
for k in range(submatrix_iterations):
	print("iteration on submatrices " + str(k))
	submatrix_nonzero_indices = global_nonzero_indices[(submatrix_size * k):(submatrix_size * (k + 1))]

	print("read data ")
	for i in range(len(Kmer_Hash_Count_Files)):
		submatrix[i,:] = np.memmap(Kmer_Hash_Count_Files[i], dtype='float32', mode='r')[submatrix_nonzero_indices]

	print("matrix normalization")
	submatrix = submatrix / np.sqrt(np.sum(submatrix * submatrix, 0))

	D = spams.trainDL(submatrix, D = D, K = args.cluster_number, lambda1 = args.lambda1, lambda2 = args.lambda2, 
		posAlpha = True, posD = True, rho = 1.0, iter = iter_nb, batchsize = batchsize, numThreads = cpu)



np.save(args.outputdir + "cluster_index.npy", D.T)




print("cluster kmers")

cluster_cols = np.zeros(2**hash_size, dtype = 'uint16')
submatrix_size = int(memory_limit / (4 * (args.cluster_number + n)))
submatrix_iterations =  int(nzi / submatrix_size) + 1
submatrix_size = min(nzi, submatrix_size)






print("clustering k-mers")

D = np.nan_to_num(D / np.sqrt(np.sum(D * D, 0)))



for k in range(submatrix_iterations):
	inds = np.arange(submatrix_size * k, min(submatrix_size * (k + 1), nzi))
	submatrix_nonzero_indices = global_nonzero_indices[inds]
	submatrix = np.zeros((n, np.shape(inds)[0]), dtype = np.float32)
	for i in range(len(Kmer_Hash_Count_Files)):
		submatrix[i,:] = np.memmap(Kmer_Hash_Count_Files[i], dtype='float32', mode='r')[submatrix_nonzero_indices]
	
	submatrix = submatrix / np.sqrt(np.sum(submatrix * submatrix, 0))
	cluster_cols[submatrix_nonzero_indices] = np.argmax(D.T.dot(submatrix), 0)
	

for c in range(0, args.cluster_number):
	kmers = np.nonzero(cluster_cols == c + 1)
	np.save(args.outputdir + str(c) + ".cluster.npy", kmers)
