#!/usr/bin/perl -w
use strict;
my $storefile = &FastaReader($ARGV[0]) or die "fasta file is required!\n";
open (TWO,">$ARGV[1]") or die "vcf file is required.";

foreach my $chr (keys %{$storefile}){
	if (length($storefile->{$chr})>=500){
		print TWO ">$chr","\n",$storefile->{$chr},"\n";
	}
}

sub FastaReader {
        my ($file) = @_;
        open IN, "<", $file or die "Fail to open file: $file!\n";
        local $/ = '>';
        <IN>;
        my ($head, $seq, %hash);
        while (<IN>){
                s/\r?\n>?$//;
                ( $head, $seq ) = split /\r?\n/, $_, 2;
                my $tmp = (split/\s+/,$head)[0];
                $seq =~ s/\s+//g;
                $hash{$tmp} = $seq;
        }
        close IN;
        $/ = "\n";
        return \%hash;
}
