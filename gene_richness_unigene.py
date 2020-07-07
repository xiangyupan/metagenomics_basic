#!/usr/bin/env python3.5
#coding=utf-8
'''
#-------------------------------------------------------------------------------
#Author:Pan Xiangyu(bendanpanxiangyu@163.com)
#Time:  2016/10/27
#Version: 1.0
#-------------------------------------------------------------------------------
'''
#######################modle####
import sys
import os
import getopt
def usage():
    print('''Useage: python script.py [option] [parameter]
    -f/--fasta        input fasta file
    -b/--blastfile                 blastfile file
    -o/--output                 output file
    -p/--output1                output1 file
    -h/--help            show possible options''')
####################### argv ######
opts, args = getopt.getopt(sys.argv[1:], "hf:b:o:p:",["help","fasta=","blastfile=","output=","output1="])
for op, value in opts:
    if op == "-f" or op == "--fasta":
        fasta = value
    elif op == "-b" or op == "--blastfile":
        blastfile = value
    elif op == "-o" or op == "--output":
        output = value
    elif op == "-p" or op == "--output1":
        output1 = value
    elif op == "-h" or op == "--help":
        usage()
        sys.exit(1)
if len(sys.argv) < 6:
    usage()
    sys.exit(1)
f1=open(fasta)
f2=open(blastfile)
f3=open(output,'w')
f4=open(output1,'w')
'''fasta f1
>/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/k39/k39-10/k39-10_seq_GI_0000021  locus=scaffold3106:314:544:+:[Complete]
GTGCTGTCAGGAATTGTAGAACCTTTTGGAGCAATACTCACAATTCTGGCAGCGGATCTT
ATTATTCCGGTTTTGCCGTATTTACTCAGTCTTGCTGCCGGTGCTATGATCTATGTAGTG
GTTGAGGAGCTGATCCCGGAAATGTCAACAGGGGAGCATTCGAATATTGGAACCATATTT
TTTGCAACAGGTTTTTCCTTTATGATGATATTAGATGTGGCGTTGGGATGA
>/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/k39/k39-10/k39-10_seq_GI_0000023  locus=scaffold9556:241:699:-:[Lack 5'-end]
TCCGCGCTGGCCGCGGCGCTCCCCGCCGCTGTGATCTGGCTGGCATGGGGCTACATGAAC
GCCATCATCTGCCTGCTCCATCTGGCGCTGTTCTGGCTTTTGAGCGACGCGCTGTTCGCC
CTGCTGAAGCGGCTGCACGGCAAGCCGTGGCGGCGGTATTACGCCGGGCTCACGGCCCTG
CTGCTCACGGCCGCCTATCTTTCGGCCGGTTGGGTGCAGGCGCACCACGTCTGGCAGACA
AACTATATCATTCATACGGACAAGCCCGTCGGCACGCTCCGCGTCGCGCTRAGGCGCACC
ACGTCTGGCAGACAAACTATATCATTCATACGGACAAGCCCGTCGGCACGCTCCGCGTCG
CGCTCATCGCCGATTCCCACATGGGCACCACGTTCCACGCAGACGGCTTTGCCCGCGAGC
TGGACCGCATCGCGGCGCAGAAGCCCGACCTGCTCGTGA
###f2 blastfile 
ST-E00317:195:HWMYYCCXX:2:1101:25276:1151/1     CAATAATGAATTAATTGGCTTATATTATGATTGTTCCAAATCCCTAAAAGAAAATCTATCAACCTTTAAAGCACTGAATTTAAAAGTAGGAAAAAGTAAATTATATGAATG <<FFJJJJJJFJJ7JJJJJ<JJJJJJJAJJJJJJJJJJAJFJJJJJJJJJJJF-AFJ7AJJJJJJJJJJ<-F<JJJJFJJAJJJJJJJJJJJJJJJJJJJJJJJJJJFFAA 1       a       111     -       /stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/k39/k39-10/k39-10_seq_GI_0085800 1167    0       111M    111
ST-E00317:195:HWMYYCCXX:2:1101:25276:1151/2     AATTGAATTTGAACATTTGCTGCACTGTTTAGCCAACGAACTATACTATTACATCAATAACAGCAAGGACCCAATAAGCAAACAAGAGTTAGATGATATCGCAGAA      AAFFJJJJJJJJJJJJJJJJJJ<AJJJJJFJJJJJJJJJJJFJJJFJJJJJJJJJJFJJJJFJJFJJJJFJJJF-<JJJJJJJJJJJ#JJJ#JJJJJJJJJJJJJJ      1       b       106     +       /stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/k39/k39-10/k39-10_seq_GI_0085800 915     2       T->91G-29A->87G-29       106M    87A3T14
'''
genedict={}
seqdict={}
for line in f1:
    if line[0] == '>':
        allseq=''
        gene=line.split()
        gene_name=gene[0].split('>')[1].rstrip()
        gene_length=int(gene[1].split(':')[2])-int(gene[1].split(':')[1])+1
        genedict[gene_name]=gene_length
    else:
        line=line.strip('\n')
        allseq += line
        seqdict[gene_name]=allseq
blastdict={}
unigene={}
for reads in f2:
    reads = reads.split()
    if reads[7] not in blastdict:
        blastdict[reads[7]]=reads[3]
    else:
        blastdict[reads[7]]=int(blastdict[reads[7]])+int(reads[3])
for key,value in blastdict.items():
    if int(value)>2:
        unigene[key]=genedict[key]
    else:
        pass
for key,value in seqdict.items():
    if key in unigene:
        f3.write('>'+key+'\n'+value+'\n')
    else:
        pass
all_n_len=0
for key,value in unigene.items():
    if key in genedict:
        genelength=genedict[key]
        readsnum=blastdict[key]
        n_length=int(readsnum)/int(genelength)
        all_n_len += n_length
    else:
        pass
for key,value in unigene.items():
    if key in genedict:
        genelength=genedict[key]
        readsnum=blastdict[key]
        n_length=int(readsnum)/int(genelength)
        gen_abu = n_length*(1/all_n_len)
    else:
        pass
    f4.write(key+'\t'+str(gen_abu)+'\n')
f1.close()
f2.close()
f3.close()
f4.close()


#==============================================================================
# fasta = r'E:\temp\Pan_test\testfa.txt'
# blastfile = r'E:\temp\Pan_test\testblastdict.txt'
#==============================================================================
