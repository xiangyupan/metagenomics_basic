# Custom scripts and codes
Custom scripts for manuscript "Dynamics of rumen gene expression, microbiome, and their interplay during early rumen development"    
## 1. Quality control    
`java -Xmx30g -jar trimmomatic-0.36.jar PE -threads 10 Rumen0-1_1.fq.gz Rumen0-1_2.fq.gz  Rumen0-1_1.clean.fq.gz Rumen0-1_1.unpaired.fq.gz Rumen0-1_2.clean.fq.gz Rumen0-1_2.unpaired.fq.gz LEADING:25 TRAILING:25 SLIDINGWINDOW:4:25 MINLEN:40 TOPHRED33 > Rumen0-1.log`   
### 1.1 Remove contaminate from host    
`bwa index -a bwtsw GCF_001704415.1_ASM170441v1_genomic.fna`   
`samtools faidx GCF_001704415.1_ASM170441v1_genomic.fna`   
`java -jar picard.jar CreateSequenceDictionary R=GCF_001704415.1_ASM170441v1_genomic.fna O=GCF_001704415.1_ASM170441v1_genomic.fna.dict`    
`bwa mem -t 4 -M -R \'@RG\tID:Rumen0-1\tLB:Rumen0-1\tPL:ILLUMINA\tSM:Rumen0-1\' GCF_001704415.1_ASM170441v1_genomic.fna Rumen0-1_1.clean.fq.gz Rumen0-1_2.clean.fq.gz > Rumen0-1.sam`     
`samtools view -bS Rumen0-1.sam >  Rumen0-1.bam`     
`samtools view -b -f 4 Rumen0-1.bam > Rumen0-1_unmapped.bam`    
`samtools sort -o Rumen0-1.unmapped.sort.bam -@ 8 -O bam Rumen0-1.unmapped.bam`   
`bedtools bamtofastq -i Rumen0-1.unmapped.sort.bam -fq Rumen0-1_1.cl.fq -fq2 Rumen0-1_2.cl.fq`    
## 2. Metagenome assembly(contig-level)   
`mkdir k39/;cd k39/`    
`SOAPdenovo-63mer pregraph -s configFile -K 39 -d 1 -R -o meta.k39 -p 40 1>pregraph.log 2>pregraph.err`   
`SOAPdenovo-63mer contig -g meta.k39 -p 40 1>contig.log 2>contig.err`   
### 2.1 Statistic the length of contig N50 and number of contigs    
`perl N50.PL meta.k39.contig 500 > contigN50.result`    
## 3. Metagenome assembly(scaffold-level)   
`cd k39/`   
`SOAPdenovo-63mer map -p 20 -s scaffold.cfg -g meta.k39 1>map.lot 2>map.err`    
`SOAPdenovo-63mer scaff -p 20 -L 200 -g meta.k39 1> scaff.log 2>scaff.err`    
### 3.1 Gap closer    
`GapCloser -a meta.k39.scafSeq -b scaffold.cfg -o Rumen0-1_gap_remove.scatigs`    
### 3.2 SoapAligner   
`2bwt-builder k39-25_gap_remove.scatigs`    
`soap -a Rumen0-1_1.cl.fq -b Rumen0-1_2.cl.fq -D Rumen0-1_gap_remove.scatigs.index -o blast -u Rumen0-1_unmap -m 200 -2 Single_output`    
## 4. Unmap fasta mixassembly    
`python3.5  seperate_pair_two_file.py -u Rumen0-1_unmap -o Rumen0-1_unmap_1.fa -f Rumen0-1_unmap_2.fa`    
## 5. Filter length of scaffolds    
`perl cut_specific_chr_length.pl Rumen0-1_gap_remove.scatigs Rumen0-1_gap_remove500.scatigs`    
## 6. Gene prediction by MetaGeneMark   
`gmhmmp -k -r -a -d -f G -m MetaGeneMark_v1.mod -o Rumen0-1.gff Rumen0-1_gap_remove500.scatigs`   
### 6.1 Gff to Gene   
`perl gff2gene.pl Rumen0-1.gff > Rumen0-1.gene.fa`    
### 6.2 Gene to Protein    
`perl gene2prot.pl Rumen0-1.gene.fa > Rumen0-1.gene.faa`    
## 7. Remove duplication    
`cat *.gene.fa > geneset.fa`    
`cd-hit-est -i geneset.fa -o geneset_unabundent.fa -n 8 -c 0.95 -G 0 -aS 0.9 -g 1 -d 0 -T 8 -M 5000`    
## 8. Mapping to geneset    
`soap -a Rumen0-1_1.cl.fq -b Rumen0-1_2.cl.fq -D geneset_unabundent.fa.index -o Rumen0-1_blast -2 Rumen0-1_Single_mapped_reads -u Rumen0-1_unmapped_reads -m 200 -x 400 -r 0`   
## 9. Caculate gene abundance   
`python3.5 gene_richness_unigene.py -f geneset_unabundent.fa -b Rumen0-1_blast -o Rumen0-1.unigene.fa -p Rumen0-1.gene.abundence`   
`cat *.unigene.fa > geneset.unabundant.unigene.fa`    
## 10. Blastp to NR database    
`diamond makedb --in NR.fa -d Taxa/
diamond blastp --query geneset_unabundent_unigene.faa --db nr --outfmt 6 --threads 30 --out geneset_unabundent_unigene_NR.table --evalue 1e-5 --block-size 10.0`    
### 10.1 Filter e-value of Results from Blastp    
`python3.5 fil_evalue10_20180115.py geneset_unabundent_unigene_NR.table geneset_unabundent_unigene_NR.table.filter`   
##  11. Visualization by Krona    
`ktImportBLAST geneset_unabundent_unigene_NR.table.filter -o geneset_unabundent_unigene_NR.table.filter.krona.html`   
##  12. Calculate taxonomic abundance based on the LCA results    
`python3.5 LCA_geneAbudunce.py -m geneset_unabundent_unigene_NR_blast_kingdom.txt -g Rumen0-1.gene.abundence -o Rumen0-1.kingdom_1 -p Rumen0-1.kingdom_2 -t Rumen0-1.kingdom_3`   
##  13. Merge each sample taxonomic/gene abundance to a Matrix    
`python3.5 allsample_abundence_martrix.py -l kingdom.list >kingdom.abundence.matrix`    
##  14. Functional annotation   
### 14.1 KEGG annotation    
`perl 0.choose_blast_m8.pl -i KEGG.blast.list.file -o blast.filter -b Y -d 40 -m 0 -e 1e-5 -p 40`   
`perl 1.anno.V2.pl blast.filter out.anno.file`    
`perl 2.catalog.pl out.anno.file out.anno.file.catalog`   
### 14.2  CAZy database annotation    
`hmmpress dbCAN-fam-HMMs.txt`   
`hmmscan dbCAN-fam-HMMs.txt geneset_unabundent_unigene.faa > CAZyme_geneset_unabundent_unigene.dbCAN`   
`sh hmmscan-parser.sh CAZyme_geneset_unabundent_unigene.dbCAN > CAZyme_geneset_unabundent_unigene.dbCAN.anno`   

**Finally: We'd love to hear from you. If you have any questions, please don't be hestitate to contact the author of this manuscript: pan_xiangyu@nwafu.edu.cn**    
