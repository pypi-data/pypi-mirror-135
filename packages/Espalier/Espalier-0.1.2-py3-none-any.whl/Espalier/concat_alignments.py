
"""
Created on Tue Jun  9 10:14:29 2020

"Concatenate seq alignments adding sequences with same id in each align end-to-end"

@author: david
"""
from Bio import SeqIO

path = 'sim_trees/original_test_trees/'
segments = 4
seq_files = [path + "disentangler_test1_tree" + str(i) + ".fasta" for i in range(segments)]

file_out = 'concat-align.fasta'

for idx, file in enumerate(seq_files):
    seq_dict = SeqIO.to_dict(SeqIO.parse(file, "fasta")) # one line alternative
    if idx == 0:
        concat_seqs = seq_dict
    else:
        for key in concat_seqs:
            concat_seqs[key] += seq_dict[key]            

# Convert to list and write seq records to fasta file
concat_records = [concat_seqs[key] for key in concat_seqs]
SeqIO.write(concat_records, file_out, "fasta")


