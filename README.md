# LSA_NMF

LSA code has been cloned from https://github.com/brian-cleary/LatentStrainAnalysis.
https://latentstrainanalysis.readthedocs.io/en/latest/getting_started.html

## Getting Started

### Dependencies

```
Python (2.7)
NumPy
SciPy
Gensim
GNU Parallel
Pyro4
spams
```

## Example data

Hash and count k-mers :

```
bash HashCounting.sh 6 33 22
```

Cluster k-mers with NMF (100 clusters) :

```
bash KmerNMFClustering.sh 6 22 100
```

Partition reads :

```
bash ReadPartitioning.sh 4
```



