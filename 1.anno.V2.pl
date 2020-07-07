#!/usr/bin/perl

#
# kegg_parser.pl  -- the program to do kegg analysis
# This program extract the ko number and its class.
# The input is the m8 format blast result against KEGG database.
#

die "useage:[in blast m8][out anno file]" if (@ARGV == 0);

use strict;
use Getopt::Long;
use FindBin qw($Bin $Script);
use File::Basename qw(basename dirname); 
use Data::Dumper;
use lib "$Bin/../../lib";
use PGAP qw(parse_config);

my $outfile = $ARGV[1];
my $blast_tab = $ARGV[0];

my ($Gene_inf, $ko_path) = parse_config("$Bin/../../config.txt", "$Bin/../..", "kegg_info", "kegg_ko");

my $blast_tab_base = basename($blast_tab);

my %KO_Class; ##´æ´¢È«²¿µÄKOÓëÆäËûÊôÐÔµÄ¶ÔÓ¦¹ØÏµ
my %KO_EC;
my %KO_Name;
my %KO_Defi;
my %Map_Gene; ##´æ´¢Êµ¼ÊÒª»­µÄmapÍ¼ºÍËù°üº¬µÄ»ùÒò

my %gene_inf;
open IN,$Gene_inf || "fail $Gene_inf";
while (<IN>) {
	chomp;
	my @inf=split /\s+/,$_;
	my $gene_name=shift @inf;
	my $tag=(split /\>/,$gene_name)[1];
	my $inf=join " ",@inf;
	$gene_inf{$tag}=$inf;
}
close IN;

# read ko file for useful information

open KO,$ko_path || "fail $ko_path";
$/="///";
while (<KO>) {
	my ($ko,$name,$defi,$class,$ec);
	$ko = $1 if (/ENTRY\s+(K\d{5})/s);  $ko =~ s/\s+/ /sg;
	$name = $1 if(/\nNAME\s+(.+?)\n\w/s);  $name =~ s/\s+/ /sg;
	if(/\nDEFINITION\s+(.+?)\s+\[EC\:(.+?)\]\n\w/s) {
		($defi,$ec)=($1,$2); $defi =~ s/\s+/ /sg; $defi =~ s/\n/ /sg; $ec =~ s/\s+/ /sg;}
	elsif(/\nDEFINITION\s+(.+?)\n\w/s) {
		$defi=$1; $defi =~ s/\s+/ /sg; $defi =~ s/\n/ /sg;};
	$class = $1 if(/\nCLASS\s+(.+?)\n\w/s); $class =~ s/\s+/ /sg;
	$KO_Name{$ko} = ($name) ? $name : "--";
	$KO_Defi{$ko} = ($defi) ? $defi : "--";
	$KO_EC{$ko} = ($ec) ? $ec : "--";
	$KO_Class{$ko} = ($class) ? $class : "--";
}
$/="\n";
close KO;

# read the table format blast result file

open TAB,$blast_tab || die "fail $blast_tab";
open OUT,">$outfile" || die "fail open out";
print OUT "Gene_id\tIdentity\tE_value\tKegg_geneID\tKo_id\tKo_name\tKo_defi\tKo_EC\tKo_class\n";
while (<TAB>) {
	chomp;
	next if (/^Gene_id/);
	my ($gene_id,$kegg_gene,$identity,$Eval) = (split /\t/)[0,1,2,10];
	my $kegg_info=$gene_inf{$kegg_gene};
	my $ko = $1 if($kegg_info =~ /\s+(K\d{5})\s*/);
	print OUT "$gene_id\t$identity\t$Eval\t$kegg_gene\t$ko\t$KO_Name{$ko}\t$KO_Defi{$ko}\t$KO_EC{$ko}\t$KO_Class{$ko}\n";
}
close OUT;
close TAB;


__END__
