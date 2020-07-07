#!/usr/bin/env perl
use warnings;
use strict;

my $gffFile = shift;
my $geneLengthCutOff = 100;
my ($sampleName) = $gffFile =~ m/(.*).gff/;
my %info;
open IN, "$gffFile" or die $!;
while (<IN>){
        if     (m/^[^#]/ and not m/^$/){
                @_ = split /\t/;
                (my $gene_id) = $_[8] =~ m/gene_id=([0-9]*)/;
                $info{$gene_id}{'scaffold'}  = $_[0];
                $info{$gene_id}{'scaffold'} =~ s/ .*//g;
                $info{$gene_id}{'start_pos'} = $_[3];
                $info{$gene_id}{'stop_pos'}  = $_[4];
                $info{$gene_id}{'cis-trans'} = $_[6];
                next;
        }elsif (m/^##DNA ([0-9]*)/){
                my $gene_id = $1;
                my $seq;
                my $seq_fold;
                my $complete;
                while (<IN>){
                        last if m/^##end-DNA/;
                        s/^##//g;
                        $seq_fold .= $_;
                        chomp;
                        $seq .= $_;
                }
                if ($seq =~ m/^[ATG]TG/i){
                        $complete = ($seq =~ m/T(AG|AA|GA)$/i) ? "[Complete]"    : "[Lack 3'-end]";
                }else {
                        $complete = ($seq =~ m/T(AG|AA|GA)$/i) ? "[Lack 5'-end]" : "[Lack both ends]";
                }
                $gene_id = ">$sampleName\_GI_" . sprintf("%07d", $gene_id) . "  locus=$info{$gene_id}{'scaffold'}:$info{$gene_id}{'start_pos'}:$info{$gene_id}{'stop_pos'}:$info{$gene_id}{'cis-trans'}:$complete";
                print "$gene_id\n$seq_fold" if length($seq)  >= $geneLengthCutOff;
        }
}
close IN;
