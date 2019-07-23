###
# Dependencies
# numpy
# scipy
# gensim: pip install gensim
# Pyro4: pip install Pyro4
###

if [ "$#" -ne 3 ]; then
	echo "Illegal number of parameters"
	echo "Usage: bash KmerSVDClustering.sh numThreads hashSize clustThresh"
	exit 1
fi


if [ $? -ne 0 ]; then echo "printing end of last log file..."; tail Logs/KmerClusterCols.log; exit 1; fi

echo $(date) Kmer clustering is complete
numThreads=$1
hashSize=$2
clusterNumber=$3



python NMF.py -i hashed_reads/ -o cluster_vectors/ -l1 0.1 -l2 0.0 -p $numThreads -cn $clusterNumber


# KmerClusterCols
echo $(date) Arranging k-mer clusters on disk
python LSA/kmer_cluster_cols.py -i hashed_reads/ -o cluster_vectors/ > Logs/KmerClusterCols.log 2>&1
