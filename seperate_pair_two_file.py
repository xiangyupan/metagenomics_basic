#!/usr/bin/env python3.5
#coding=utf-8
'''
#-------------------------------------------------------------------------------
#Author:Pan Xiangyu(bendanpanxiangyu@163.com)
#Time:  2016/10/23
#Version: 1.0
#-------------------------------------------------------------------------------
'''
#######################modle####
import sys
import re
import os
import getopt
def usage():
    print('''Useage: python script.py [option] [parameter]
    -u/--unmap        input unmap file
    -o/--output1                 output1 file
    -f/--output2                 output2 file
    -h/--help            show possible options''')
####################### argv ######
opts, args = getopt.getopt(sys.argv[1:], "hu:o:f:",["help","unmap=","output1=","output2="])
for op, value in opts:
    if op == "-u" or op == "--unmap":
        unmap = value
    elif op == "-o" or op == "--output":
        output1 = value
    elif op == "-f" or op == "--output2":
        output2 = value
    elif op == "-h" or op == "--help":
        usage()
        sys.exit(1)
if len(sys.argv) < 5:
    usage()
    sys.exit(1)
f1=open(unmap)
f2=open(output1,'w')
f3=open(output2,'w')
'''f1 unmap file
>ST-E00142:294:HWT73CCXX:7:1101:10531:1766/1
ACTTTCTCAATTCCCGGGATCGCCTTGATCTGTTTTGCAAGACTTGCACAGCCCTTACGAACAAGAGGCTCACCGCCTGTCAGTTTAATCTTACGGATTCCCAGATCTGCTGCGCACCTGCAGATGCGGAGAATCTCATCGTATGTGAG
>ST-E00142:294:HWT73CCXX:7:1101:10531:1766/2
ATAGACAAATATGGAAGAGAAATAGATTATTTAAGGATTTCCCTGACAGACAGATGTAATCTGAGATGCATTTACTGTATGCCGGAAGAAGGCGTAAAATCCCTTTCTCATGTAGAAATCCTCACATACGATGAGATTCTCCGCATCTG
>ST-E00142:294:HWT73CCXX:7:1101:23683:1766/1
ATGTGCATGTCTCAAATGCTTCTGTGCTTCCGATGAGCACTGTACCTGTCACGCTTTTATGTCACAGCAGGATTTCAAGCAGGGAGAGTGCCTATACGCGCGATGCCTTTGTTACGCCGGGCTCAGGCTCTTCGCTTTGCTTTTACCTG
>ST-E00142:294:HWT73CCXX:7:1101:28331:1766/1
AGGAAAATGGCGGTATTTCCATTAATAGAAATAAAGCGATTGAGATGGCGACGGGGGAATATCTGATGCTCAGTGATCACGAGGATACGCTGGAACCGGATGCGTTATATGAAA
>ST-E00142:294:HWT73CCXX:7:1101:28331:1766/2
TTCAAAATAAAATTCCCCATCCATACTCAGCTTGTCTTCATCTGTATAAACAATCTCCGGCCCCTGATGGTCATTGATGGCTTTGACGATTTCATATAACGCATCCGGTTCCAGCGTATCGTCGTGATCACTG
'''
seq={}
tagname={}
for line in f1:
    if '>' in line:
        tag1=line.strip('\n').split('/')
    else:
        fasta=line.strip('\n')
        seq[tag1[0]+'/'+tag1[1]]=line
        if tag1[0] in tagname:
            tagname[tag1[0]]=tag1[0]
        else:
            tagname[tag1[0]]=''
#print(tagname)
for key,value in tagname.items():
    if value:
        f2.write(key+'/1'+'\n'+seq[key+'/1'])
        f3.write(key+'/2'+'\n'+seq[key+'/2'])
    else:
        pass
f1.close()
f2.close()
f3.close()