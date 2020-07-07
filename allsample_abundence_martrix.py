#!/usr/bin/env python3.4
'''
#-------------------------------------------------------------------------------
#Author:Pan Xiangyu(bendanpanxiangyu@163.com)
#Time:  2016/11/1
#Version: 1.0
#-------------------------------------------------------------------------------
'''
#######################modle####
import sys
import re
import getopt
def usage():
    print('''Useage: python script.py [option] [parameter]
    -l/--list        input path list file
    -h/--help            show possible options''')
####################### argv ######
opts, args = getopt.getopt(sys.argv[1:], "hl:",["help","list="])
for op, value in opts:
    if op == "-l" or op == "--list":
        list = value
    elif op == "-h" or op == "--help":
        usage()
        sys.exit(1)
if len(sys.argv) < 0:
    usage()
    sys.exit(1)
f1=open(list)
'''path list  f1
/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/geneset_alinger/10.gene.abundence
/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/geneset_alinger/11_HWMYYCCXX_L2.gene.abundence
/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/geneset_alinger/12_HWT73CCXX_L7.gene.abundence
/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/geneset_alinger/15_HWT73CCXX_L4.gene.abundence
###
/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/megan_anno/phylum/10_s
#####line_content
Firmicutes      0.380599884
Bacteroidetes   0.242476542
Proteobacteria  0.21774682
Verrucomicrobia 0.028017321
####
/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/k39/k39-12/k39-12_seq_GI_0071647 2.229771878131042e-06
/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/k39/k39-11/k39-11_seq_GI_0040193 1.100099653401522e-06
/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/k39/mix_denovo/k39-mix_seq_GI_0195433    2.6272968193001053e-06
/stor9000/apps/users/NWSUAF/2016050001/meta/data_release/my_clean_data/my_clean_data/new_fastq/k39/mix_denovo/k39-mix_seq_GI_0142544    1.1815885166164495e-06
####
ACH1    159     112     26      21
ACO1    3210    2734    438     38
ACO2    555     497     24      34
ACP1    576     506     67      3
ACS2    5136    3823    1292    21

'''
totaldict={}
sample_list = []
name=''
title='taxa'
for line in f1:
    line=line.strip()
    a=line.split('/')
#    b=a[-1].split('_')
    c=a[-1]
    name += c+'\t'
    file1=open(line)
    for reads in file1:
        reads=reads.split('\t')
        totaldict[reads[0]]=''
    file1.close()
f1.close()

f1=open(list)
for sample_file in f1:
    sample_name = sample_file.strip('\n')
#    print(sample_file.split('.'))
    sample_name = sample_name.split('/')[-1]
#    print(sample_name)
    sample_list.append(sample_name)
    locals()[sample_name] = {}
    file1 = open(sample_name)
    for line in file1:
#        print(line)
        line = line.strip('\n').split('\t')
        gene = line[0]
#        print(line[0])
        abu = line[1]
#        print(abu)
        locals()[sample_name][gene] = abu

#print("gene_name\t"+"\t".join(sample_list))
print(title+'\t'+name)
for gene in totaldict.keys():
#    print(gene)
    abu_list = []
    for sample in sample_list:
        abu = locals()[sample].get(gene,'0')
        abu_list.append(abu)
    print(str(gene)+ '\t'+ "\t".join(abu_list))

f1.close()
