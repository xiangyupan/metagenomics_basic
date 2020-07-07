# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 16:45:28 2017

@author: Pan Xiangyu
@Email: pan_xiangyu@nwafu.edu.cn
"""
import sys
import re
if len(sys.argv) < 3:
    print('Usage: python3.5 '+sys.argv[0]+'[blastp.NR] [blastp.NR.filter]')
    exit(1)
infile1 = open(sys.argv[1])
outfile=open(sys.argv[2],'w')
'''
k39-8/k39-8_seq_GI_0004570      WP_049498163.1  98.6    142     2       0       1       142     23      164     3.7e-71 276.2
k39-8/k39-8_seq_GI_0004570      WP_045759179.1  98.6    142     2       0       1       142     23      164     3.7e-71 276.2
k39-8/k39-8_seq_GI_0004570      ETJ03885.1      98.6    142     2       0       1       142     12      153     3.7e-71 276.2
k39-8/k39-8_seq_GI_0004570      WP_049514247.1  98.6    142     2       0       1       142     23      164     3.7e-71 276.2
k39-8/k39-8_seq_GI_0004570      WP_009732420.1  97.9    142     3       0       1       142     23      164     1.8e-70 273.9
k39-8/k39-8_seq_GI_0004570      WP_013903231.1  97.9    142     3       0       1       142     23      164     2.4e-70 273.5
'''
name = {}
new={}
allinfo = {}
for reads in infile1:
    reads = reads.strip().split("\t")
E    allinfo[reads[0]+"\t"+reads[1]+"\t"+reads[10]] = "\t".join(reads[:])
    reads[10] = float(reads[10])
    name[reads[10]] = []
    if reads[0] in name:
        name[reads[0]].append(reads[10])
    else:
        name[reads[0]].append(reads[10])
for key,value in name.items():
    ee = min(value)
    new[key] = ee
for line in infile1:
    line = line.strip().split("\t")
    if line[0] in new:
        if line[10] <= ee*10:
            outfile.write("\t".join(line[:]))
        else:
            pass
    else:
        print(line[0])
infile1.close()
outfile.close()   