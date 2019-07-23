#!/usr/bin/env python

import sys, getopt
import glob,os

help_message = 'usage example: python merge_partition_parts.py -r 1 -i /project/home/cluster_vectors/ -o read_partitions/'
if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:],'hr:i:o:',["filerank=","inputdir=","outputdir="])
	except:
		print help_message
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h','--help'):
			print help_message
			sys.exit()
		elif opt in ('-r','--filerank'):
			fr = int(arg) - 1
		elif opt in ('-i','--inputdir'):
			inputdir = arg
			if inputdir[-1] != '/':
				inputdir += '/'
		elif opt in ('-o','--outputdir'):
			outputdir = arg
			if outputdir[-1] != '/':
				outputdir += '/'

	fr = str(fr)+'/'
	os.system('mkdir '+outputdir+fr)
	
	suffix = 'fastq'
	FP = glob.glob(os.path.join(inputdir+fr,'*.' + suffix + '.*'))
	
	
	#FP = glob.glob(os.path.join(inputdir+fr,'*.' + suffix + '.*'))
	FPl = list(set([fp[fp.rfind('/')+1:fp.index('.' + suffix)] for fp in FP]))
	if len(FPl) == 0:
		suffix = 'fa'
		FPl = list(set([fp[fp.rfind('/')+1:fp.index('.' + suffix)] for fp in FP]))


	for group in FPl:
		gp = [fp for fp in FP if inputdir+fr+group+ '.' + suffix == fp[:fp.rfind('.')]]
		#gp = [fp for fp in gp if '.empty' not in fp]
		if len(gp) > 0:
			os.system('cat '+' '.join(gp)+' > '+outputdir+fr+group+ '.' + suffix)
			#os.system('touch %s.empty' % (gp[0]))
			os.system('rm '+' '.join(gp))