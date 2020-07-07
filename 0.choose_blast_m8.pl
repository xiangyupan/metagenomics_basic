#! /usr/bin/perl -w
use strict;

sub usage {
	print STDERR <<USAGE;

Usage:  choose_blast_m8 -i <blast_list_lile> -o <file_for_chosen_blast_results> <options>

			-i  <C>: input list contain blast m8 results
			-o  <C>: output file of chosen results
	options
			-b  <B>: Y or N, choose the BestHit.       Default Y
			-d  <N>: identity threshold.               Default 40
			-m  <N>: match length threshold.           Default 0
			-e  <N>: e_value threshold.                Default 1e-5
			-p  <N>: min match percentage%.            Default 40
			-q  <C>: query file of blast if -p.
			-s  <C>: subject file of blat if -p.
			-h     : output this help message.
USAGE
}

use Getopt::Std;
getopts('i:o:b:d:m:e:p:q:s:h');
our ($opt_i,$opt_o,$opt_b,$opt_d,$opt_m,$opt_e,$opt_p,$opt_q,$opt_s,$opt_h);

if($opt_h) {usage;exit;}
unless($opt_i && $opt_o) {usage;exit;}
if ($opt_p && !($opt_q && $opt_s)) {usage;exit;}


$opt_d = 40 unless(defined($opt_d));
$opt_e = 1e-5 unless(defined($opt_e));
$opt_m = 0 unless((defined$opt_m));
$opt_b = "Y" unless((defined$opt_b));
$opt_p = 40 unless((defined$opt_p));

#---- filt match percentage
my %seq;
get_seq("query",$opt_q);
get_seq("db",$opt_s);

open BLAST,$opt_i or die "$opt_i $!\n";
open OUT,">$opt_o.temp" or die "$opt_o.temp $!\n";
while(<BLAST>){
	chomp;
	my $filename = $_;
	open TEMP,$filename or die "$filename $!\n";
	while(<TEMP>) {
		chomp;
		my @split = split;
		die "$filename: \"$_\" Not 12 columns, please Check Your blast m8 result!\n" if(@split != 12);
		next if (abs($split[6]-$split[7]))*100/$seq{query}{$split[0]}<$opt_p;
		next if (abs($split[8]-$split[9]))*100/$seq{db}{$split[1]}<$opt_p;
		print OUT join "\t",@split, "\n";
	}
	close TEMP;
}
close BLAST;
close OUT;

print "start to filt percentage....\n";
open IN,"$opt_o.temp" || die;
open OUT,">$opt_o" || die;
print OUT "Gene_id\tSubject_id\tIdentity\tAlign_length\tMismatch\tGap\tGene_start\tGene_end\tSubject_start\tSubject_end\tE_value\tScore\n";
my %check;
while (<IN>) {
	chomp;
	my @a = split;
	print "$opt_i\n$_\n" if(@a != 12);
	die "$_ Not 12 columns, please Check Your blast m8 result!\n" if(@a != 12);
	if(exists $check{$a[0]} and ($opt_b eq "Y")){next;}
	if($a[2] < $opt_d || $a[-2] > $opt_e || $a[3] < $opt_m){next;}
	$check{$a[0]} = 1;
	print OUT "$_\n";
}
close IN;
close OUT;
#`rm $opt_o.temp`;

#============= sub ===============
sub get_seq {
	my ($tag,$file)=@_;
	open INA,$file;
	while(<INA>){
		chomp;
		my @split=split /[\t\s]+/,$_;
		$split[0]=~s/>//g;
		$/=">";
		my $seq=<INA>;
		$seq=~s/>//g;
		$seq=~s/\n//g;
		$/="\n";
		$seq{$tag}{$split[0]}=length $seq;
	}
	close INA;
}


