# metagenomics_basic
Basic analysis of metagenomics from assembly to gene abundance    
## Quality control    
`java -Xmx30g -jar trimmomatic-0.36.jar PE -threads 10 Rumen0-1_1.fq.gz Rumen0-1_2.fq.gz  Rumen0-1_1.clean.fq.gz Rumen0-1_1.unpaired.fq.gz Rumen0-1_2.clean.fq.gz Rumen0-1_2.unpaired.fq.gz LEADING:25 TRAILING:25 SLIDINGWINDOW:4:25 MINLEN:40 TOPHRED33 > Rumen0-1.log`   
### Remove contaminate from host    
`bwa index -a bwtsw GCF_001704415.1_ASM170441v1_genomic.fna`   
`samtools faidx GCF_001704415.1_ASM170441v1_genomic.fna`   
`java -jar picard.jar CreateSequenceDictionary R=GCF_001704415.1_ASM170441v1_genomic.fna O=GCF_001704415.1_ASM170441v1_genomic.fna.dict`    
`bwa mem -t 4 -M -R '@RG\tID:Rumen0-1\tLB:Rumen0-1\tPL:ILLUMINA\tSM:Rumen0-1' GCF_001704415.1_ASM170441v1_genomic.fna Rumen0-1_1.clean.fq.gz Rumen0-1_2.clean.fq.gz > Rumen0-1.sam`     
`samtools view -bS Rumen0-1.sam >  Rumen0-1.bam`     
`samtools view -b -f 4 Rumen0-1.bam > Rumen0-1_unmapped.bam`    
`samtools sort -o Rumen0-1.unmapped.sort.bam -@ 8 -O bam Rumen0-1.unmapped.bam`   
`bedtools bamtofastq -i Rumen0-1.unmapped.sort.bam -fq Rumen0-1_1.cl.fq -fq2 Rumen0-1_2.cl.fq`    
##  Metagenome assembly(contig-level)   
`mkdir k39/;cd k39/`    
`SOAPdenovo-63mer pregraph -s configFile -K 39 -d 1 -R -o meta.k39 -p 40 1>pregraph.log 2>pregraph.err`   
`SOAPdenovo-63mer contig -g meta.k39 -p 40 1>contig.log 2>contig.err`   
### Statistic the length of contig N50 and number of contigs    
`perl N50.PL meta.k39.contig 500 > contigN50.result`    
##  Metagenome assembly(scaffold-level)   
`cd k39/`   
`SOAPdenovo-63mer map -p 20 -s scaffold.cfg -g meta.k39 1>map.lot 2>map.err`    
`SOAPdenovo-63mer scaff -p 20 -L 200 -g meta.k39 1> scaff.log 2>scaff.err`    
### Gap closer    
`GapCloser -a meta.k39.scafSeq -b scaffold.cfg -o Rumen0-1_gap_remove.scatigs`    
### SoapAligner   
`2bwt-builder k39-25_gap_remove.scatigs`    
`soap -a Rumen0-1_1.cl.fq -b Rumen0-1_2.cl.fq -D Rumen0-1_gap_remove.scatigs.index -o blast -u Rumen0-1_unmap -m 200 -2 Single_output`    
## Unmap fasta mixassembly    
`python3.5  seperate_pair_two_file.py -u Rumen0-1_unmap -o Rumen0-1_unmap_1.fa -f Rumen0-1_unmap_2.fa`    
##  Filter length of scaffolds    
`perl cut_specific_chr_length.pl Rumen0-1_gap_remove.scatigs Rumen0-1_gap_remove500.scatigs`    
##  Remove duplication    
`cd-hit-est -i geneset.fa -o geneset_unabundent.fa -n 8 -c 0.95 -G 0 -aS 0.9 -g 1 -d 0 -T 8 -M 5000`    
##  Gene prediction by MetaGeneMark   
`gmhmmp -k -r -a -d -f G -m MetaGeneMark_v1.mod -o Rumen0-1.gff Rumen0-1_gap_remove500.scatigs`   
###  Gff to Gene   
`perl gff2gene.pl Rumen0-1.gff > Rumen0-1.gene.fa`    
###  Gene to Protein    
`perl gene2prot.pl Rumen0-1.gene.fa > Rumen0-1.gene.faa`    
