#!/usr/bin/env python3.4
'''
#-------------------------------------------------------------------------------
#Author:Pan Xiangyu(bendanpanxiangyu@163.com)
#Time:  2016/11/19
#Version: 1.0
#-------------------------------------------------------------------------------
'''
#######################modle####
import sys
import getopt
def usage():
    print('''Useage: python script.py [option] [parameter]
    -m/--megan_taxa        input megan taxa file
    -g/--gene_ex     input gene abudence file per sample
    -o/--output1      output1 file
    -p/--output2      output2 file
    -t/--output3      output3 file
    -h/--help            show possible options''')
####################### argv ######
opts, args = getopt.getopt(sys.argv[1:], "hm:g:o:p:t:",["help","megan_taxa=","gene_ex=","output1=","output2=","output3="])
for op, value in opts:
    if op == "-m" or op == "--megan_taxa":
        megan_taxa = value
    elif op == "-g" or op == "gene_ex":
        gene_ex = value
    elif op == "-o" or op == "output1":
        output1 = value
    elif op == "-p" or op == "output2":
        output2 = value
    elif op == "-t" or op == "output3":
        output3 = value
    elif op == "-h" or op == "--help":
        usage()
        sys.exit(1)
if len(sys.argv) < 5:
    usage()
    sys.exit(1)
'''f1 megan kingdom taxatom
"Bacteria"      mix_denovo/k39-mix_seq_GI_0217652       mix_denovo/k39-mix_seq_GI_0110128       k39-15/k39-15_seq_GI_0019789    k39-35/k39-35_seq_GI_0031264    k39-35/k39-35_seq_GI_0038767    mix_denovo/k39-mix_seq_GI_0085097
        k39-35/k39-35_seq_GI_0084015    k39-44/k39-44_seq_GI_0088363    k39-12/k39-12_seq_GI_0031594
        k39-66/k39-66_seq_GI_0014094    k39-28/k39-28_seq_GI_0055650    k39-37/k39-37_seq_GI_0055916    k39-41/k39-41_seq_GI_0009411
        k39-45/k39-45_seq_GI_0029216    k39-41/k39-41_seq_GI_0018127
        k39-41/k39-41_seq_GI_0060804
###f2 sample gene abudence
k39-24/k39-24_seq_GI_0059749    6.186109450638615e-05
k39-28/k39-28_seq_GI_0092957    1.7778039913173518e-06
k39-10/k39-10_seq_GI_0067180    1.7869039652142765e-06
k39-35/k39-35_seq_GI_0085442    1.1510961094860553e-06
k39-3/k39-3_seq_GI_0034207      4.3986902877955096e-06
mix_denovo/k39-mix_seq_GI_0206452       1.4939529338801279e-06
k39-29/k39-29_seq_GI_0071903    6.853817057980796e-07
k39-3/k39-3_seq_GI_0070857      6.603271967750164e-06
k39-15/k39-15_seq_GI_0045818    5.254593077785276e-07
k39-10/k39-10_seq_GI_0020431    6.015126286412093e-07
k39-9/k39-9_seq_GI_0048437      2.9977022804414366e-06
k39-12/k39-12_seq_GI_0073079    1.0113929154144227e-06
k39-9/k39-9_seq_GI_0043833      1.576377923335583e-06
k39-11/k39-11_seq_GI_0031285    5.873989245054938e-06
k39-30/k39-30_seq_GI_0030321    7.525096259544346e-07
k39-10/k39-10_seq_GI_0022578    9.661607045250483e-05
k39-19/k39-19_seq_GI_0061819    1.7855001124918858e-05
k39-7/k39-7_seq_GI_0055077      9.35965053248729e-06
k39-36/k39-36_seq_GI_0054231    4.5487522165902396e-07
'''
f1=open(megan_taxa)
f2=open(gene_ex)
f3=open(output1,'w')
f4=open(output2,'w')
f5=open(output3,'w')
genetaxa=[]
genetaxaname=[]
for gene in f1:
    gene=gene.strip('\n\t')
    genetaxa.append(gene)
i=0
for reads in genetaxa:
    reads_spl=reads.split('\t')
    if '_GI_' not in reads_spl[0] and i == 0:
        genetaxaname.append(reads)
        i += 1
    elif '_GI_' not in reads_spl[0] and i >0 :
        genetaxaname.append('\n'+reads)
    else:
        genetaxaname.append('\t'+reads)
newtaxa=''.join(genetaxaname)
f3.write(newtaxa)
f3.close()
f3=open(output1)
abudence={}
for gene in f3:
    gene_spl=gene.split('\t')
    abudence[gene_spl[0].strip()]=gene_spl[1:]
gene_abu_dict={}
for line in f2:
    line=line.split('\t')
    gene_abu_dict[line[0].strip()]=line[1].strip()
for key,value in abudence.items():
    num=0
    num_abu=0
    result1=[]
    result2=[]
    result1.append(key)
    result2.append(key)
    for a in abudence[key]:
        a_s=a.strip()
        num += float(gene_abu_dict.get(a_s,0))
        if float(gene_abu_dict.get(a_s,0)):
            num_abu += 1
    taxa_abu='\t'+str(num)+'\n'
    gene_abu='\t'+str(num_abu)+'\n'
    result1.append(taxa_abu)
    result2.append(gene_abu)
    result1_new=''.join(result1)
    result2_new=''.join(result2)
    f4.write(result1_new)
    f5.write(result2_new)
#################
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
