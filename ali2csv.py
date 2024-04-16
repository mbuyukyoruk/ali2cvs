import argparse
import os
import sys
import subprocess
import pandas as pd
import textwrap

try:
    from tqdm import tqdm
except:
    print("tqdm module is not installed! Please install tqdm and try again.")
    sys.exit()

try:
    from Bio import SeqIO
except:
    print("SeqIO module is not installed! Please install SeqIO and try again.")
    sys.exit()


parser = argparse.ArgumentParser(prog='python ali2csv.py',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\

# ali2csv

Author: Murat Buyukyoruk

        ali2csv help:

This script is developed to convert a multiple sequence alingment to a CSV file. 

SeqIO package from Bio is required to fetch sequences. tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.
        
Syntax:

        python ali2csv.py -i demo.fasta -l demo_sub_list.txt -o demo_sub_list.fasta

ali2csv dependencies:

Bio module and SeqIO available in this package      refer to https://biopython.org/wiki/Download
	
pandas                                              refer to https://pandas.pydata.org/
	
tqdm                                                refer to https://pypi.org/project/tqdm/
	
Input Paramaters (REQUIRED):
----------------------------
	-i/--input		FASTA			Specify a MSA fasta file.

	-o/--output		output file	    Specify a output file name that should contain CSV output.
	
Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.

      	'''))
parser.add_argument('-i', '--input', required=True, type=str, dest='filename',
                        help='Specify a MSA fasta file.\n')

parser.add_argument('-o', '--output', required=True, dest='out',
                        help='Specify a output file name that should contain CSV output.\n')

results = parser.parse_args()
filename = results.filename
out = results.out

seq_id_list = []
seq_list = []
seq_description_list = []

os.system('> ' + out)

proc = subprocess.Popen("grep -c '>' " + filename, shell=True, stdout=subprocess.PIPE, text=True)
length = int(proc.communicate()[0].split('\n')[0])

data = pd.DataFrame([])

with tqdm(range(length), desc = 'Reading...' ) as pbar:
    for record in SeqIO.parse(filename, "fasta"):
        pbar.update()
        seq_id_list.append(record.id)
        seq_list.append(record.seq)
        seq_description_list.append(record.description)
        seq_parse = list(record.seq)
        seq_parse.insert(0,record.description)

        df = pd.Series(seq_parse)

        row_df = pd.DataFrame([df])

        data = pd.concat([data, row_df], ignore_index=True)

data.to_csv(out,sep='\t', index = False)





