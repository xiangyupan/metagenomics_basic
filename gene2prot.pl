#!/usr/bin/perl
use strict;

my %codon=(
"GCU" => "A","GCC" => "A","GCA" => "A","GCG" => "A",
"CGU" => "R","CGC" => "R","CGA" => "R","CGG" => "R","AGA" => "R","AGG" => "R",
"AAU" => "N","AAC" => "N",
"GAU" => "D","GAC" => "D",
"UGU" => "C","UGC" => "C",
"CAA" => "Q","CAG" => "Q",
"GAA" => "E","GAG" => "E",
"GGU" => "G","GGC" => "G","GGA" => "G","GGG" => "G",
"CAU" => "H","CAC" => "H",
"AUU" => "I","AUC" => "I","AUA" => "I",
"UUA" => "L","UUG" => "L","CUU" => "L","CUA" => "L","CUG" => "L","CUC" => "L",
"AAA" => "K","AAG" => "K",
"AUG" => "M",
"UUU" => "F","UUC" => "F",
"CCU" => "P","CCC" => "P","CCA" => "P","CCG" => "P",
"UCU" => "S","UCC" => "S","UCA" => "S","UCG" => "S","AGU" => "S","AGC" => "S",
"ACU" => "T","ACC" => "T","ACA" => "T","ACG" => "T",
"UGG" => "W",
"UAU" => "Y","UAC" => "Y",
"GUU" => "V","GUC" => "V","GUA" => "V","GUG" => "V",
"UAG" => "","UGA" => "","UAA" => "",);

$/="\>";##在Perl中，$/意即输入记录分隔符，代表着一个记录的结束和开始。
open IN,@ARGV[0] or die "$!";
my %cds;
<IN>;
while(<IN>){
        chomp;
        my @aa=split("\n", $_);##这里的split将字符串按照分行符号\n进行分割然后结果放入数组“@aa”中。
        my $name=shift @aa;
        my $string1 = join ("",@aa);
        $string1 =~ s/t/U/gi;
        $string1 =~ tr/[a-z]/[A-Z]/;
        $string1 =~ s/^((\D\D\D)+).*$/$1/g;
        $string1 =~ s/(\D\D\D)/$codon{$1}/gi;
        my $out_string = &fasta_seq($string1);
        print ">$name\n$out_string";
}
$/="\n";
close IN;

sub fasta_seq{
        my $cds_seq=shift;
        my $c;
        my $length_seq=length $cds_seq;
        for(my $i=0;$i<$length_seq;$i+=60){
                $c.=substr($cds_seq,$i,60)."\n";
        }
        return $c;
}