#!/usr/bin/perl -w

use strict;
use warnings;
if (@ARGV<1){
        print"usage:\nperl $0 <fasta_seq>  < len_cut [100] > > out_file \n";
        exit;
}

open IN,"$ARGV[0]" or die $!;

sub nx($);
my $cutoff_len =($ARGV[1]|| 500 );
my @array_len=();
my $total_len=0;
my $total_len_100=0;
my $total_len_1000=0;
my $total_len_2000=0;
my $total_len_5000=0;
my $total_len_10k=0;
my $count=0;
my $len=0;
my $average_len=0;

while(<IN>){
        chomp;
        if(/^>/){
                if($len>=$cutoff_len){
                        $total_len+=$len;
                        if($len>=100){$total_len_100++;}
                                                if($len>=1000){$total_len_1000++;}
                        if($len>=2000){$total_len_2000++;}
                                                if($len>=5000){$total_len_5000++;}
                        if($len>=10000){$total_len_10k++;}
                        push @array_len,$len;
                }
                $len=0;
        }
        else {$len += length;}
}
close IN;

$total_len+=$len;
if($len>=100){$total_len_100++;}
if($len>=1000){$total_len_1000++;}
if($len>=2000){$total_len_2000++;}
if($len>=5000){$total_len_5000++;}
if($len>=10000){$total_len_10k++;}
push @array_len,$len;

$count = @array_len;
@array_len = sort {$b<=>$a} @array_len;
for(my $n=90;$n>0;$n-=10){
        my ($nlen,$index) = nx($n);
        print "N$n\t$nlen\t$index\n"
}
$average_len=int($total_len/$count);
print "Max length = $array_len[0]\n";
print "Total length = $total_len\tTotal number = $count\tAverage length = $average_len\n";
print "Number>=100bp = $total_len_100\tNumber>=1000bp = $total_len_1000\tNumber>=2000bp = $total_len_2000\tNumber>=5000bp = $total_len_5000\tNumber>=10kbp = $total_len_10k\n\n";

sub nx($){
        my ($n)=@_;
        my $nlen=0;
        for (my $i=0;$i<@array_len;$i++ ){
                $nlen += $array_len[$i];
                if($nlen*100>=$total_len*$n){
                        return ($array_len[$i],$i+1);
                        last;
                }
        }
}

