#! /usr/bin/perl -w
use strict;
use File::Basename qw(basename dirname); 
die "Usage:[ ko anno file] [out file]\n" unless( @ARGV == 2);

#
# this program do with the kegg annotation file
#

use strict;
open IN,$ARGV[0] or die "$ARGV[0] $!\n";
my $cate_base = basename($ARGV[0]);
open OUT,">$ARGV[1]";
print OUT "Ko_id\tGene_number\tGene_id\n";

my %hash=();
my @temp;

while(<IN>) {
	chomp;
	@temp = split("\t");
	if($temp[4] =~ /K\S{5}/){
	    my $name = $temp[0];
	    if(!exists $hash{$temp[4]}){
		$hash{$temp[4]} .= "$name\t";
	    }elsif($hash{$temp[4]} !~ /$name/){
		$hash{$temp[4]} .= "$name\t";
	    };
	};
}
close(IN);
foreach my $key(sort keys(%hash)) {
    chomp $hash{$key};
    my @tmp = split(/\t/,$hash{$key});
    my $num = @tmp;
	print OUT "$key\t$num\t$hash{$key}\n";
}
close(OUT);

# end
