======================================================
==     gnomAD_STR_genotypes__[datestamp].tsv.gz     ==
======================================================

This is a flat table that contains the ExpansionHunter genotypes from
all samples at each of the 59 disease-associated loci. Also, it contains Population, Sex, Age, and PcrProtocol
metadata columns, so the data in this table can be used to generate any of the plots displayed in the gnomAD
browser STR pages. It also contains results not currently available through the browser.
These are in the GenotypeUsingOfftargetRegions and GenotypeConfidenceIntervalUsingOfftargetRegions columns
which store ExpansionHunter calls generated using off-target regions. Finally, the ReadvizFilename column
links each row to a REViewer read visualization image that is available through the browser. This should allow users
to construct the full public url of the image and programmatically download specific images of interest.

Below is an example of column names and values from a typical row in this table:

                                              Id : PABPN1
                                         LocusId : PABPN1
                                 ReferenceRegion : chr14:23321472-23321490
                                           Chrom : chr14
                                    Start_0based : 23321472
                                             End : 23321490
                                           Motif : GCG
                                IsAdjacentRepeat : False
                                      Population : nfe
                                             Sex : XY
                                             Age : 20-25
                                     PcrProtocol : pcr_free
                                        Genotype : 6/13
                                         Allele1 : 6
                                         Allele2 : 13
                      GenotypeConfidenceInterval : 6-6/11-30
                   GenotypeUsingOfftargetRegions : 6/13
                    Allele1UsingOfftargetRegions : 6
                    Allele2UsingOfftargetRegions : 13
 GenotypeConfidenceIntervalUsingOfftargetRegions : 6-6/11-30
                                 ReadvizFilename : c82034cf2aad813a07a8523898d64c81148.svg

Id : This id is unique to each STR locus and repeat, meaning that it differs between repeats and any adjacent repeats
    at a locus. For example the main GAA repeat at the FXN locus has id "FXN" while the adjacent poly-A repeat has id
    "FXN_A". This id corresponds to the "VariantId" field in the ExpansionHunter variant catalogs @
    https://github.com/broadinstitute/str-analysis/tree/main/str_analysis/variant_catalogs
LocusId: This id is unique to each STR locus. It corresponds to the "LocusId" field in the ExpansionHunter variant
    catalogs @ https://github.com/broadinstitute/str-analysis/tree/main/str_analysis/variant_catalogs
    and can be used to look up reference information about each locus there - including the
    gene name, disease associations, mode of inheritance, and pathogenic threshold. For most but not all loci, the
    LocusId is identical to the name of the gene that contains the locus.
ReferenceRegion: Genomic interval delineating the exact boundaries of the STR repeat in the reference genome.
    The start coordinate is 0-based.
Chrom: The chromosome of the ReferenceRegion. This is provided as a separate column for convenience.
Start_0based: The 0-based start coordinate of the ReferenceRegion. This is provided as a separate column for convenience.
End: The end coordinate of the ReferenceRegion. This is provided as a separate column for convenience.
Motif: The repeat unit of the STR locus. For example this would be "GAA" at the FXN locus.
IsAdjacentRepeat: True or False depending on whether this row represents the main repeat at a locus or an adjacent repeat.
    Adjacent repeats are included for some loci either for technical reasons to improve ExpansionHunter accuracy, or
    due to research interest in the size of these adjacent repeats.
Population: The gnomAD ancestry group of the individual. Possible values are: "afr", "ami", "amr", "asj", "eas", "fin",
    "mid", "nfe", "oth", "sas"
Sex: The sex karyotype of the genotyped individual. Possible values are "XX" and "XY".
Age: The age of the individual at the time when they enrolled in one of the research studies underlying gnomAD.
    The values represent 5 year bins such as "20-25", as well as ">80" for individuals over 80 years old and "<20" for
    individuals younger than 20. For individuals with unknown age, the value is "age_not_available"
PcrProtocol: Possible values are "pcr_free", "pcr_plus" and "pcr_info_not_available"
Genotype: The ExpansionHunter genotype for this individual at this locus, generated using the variant catalog without
    off-target regions (see https://github.com/broadinstitute/str-analysis/tree/main/str_analysis/variant_catalogs).
    These are the genotypes used to generate all plots in the gnomAD browser STR pages.
Allele1: The shorter repeat size from the genotype. This is provided as a separate column for convenience.
Allele2: The longer repeat size from the genotype; empty in the special case of hemizygous genotypes (e.g., in male samples
    at loci on chrX). This is provided as a separate column for convenience.
GenotypeConfidenceInterval: The ExpansionHunter confidence intervals associated with the genotype in the "Genotype" column.

GenotypeUsingOfftargetRegions: Same meaning as the "Genotype" column, but generated using the variant catalog with off-target regions.
Allele1UsingOfftargetRegions: Same meaning as the "Allele1" column, but generated using the variant catalog with off-target regions.
Allele2UsingOfftargetRegions: Same meaning as the "Allele2" column, but generated using the variant catalog with off-target regions.
GenotypeConfidenceIntervalUsingOfftargetRegions: Same meaning as the "GenotypeConfidenceInterval" column, but generated using the
    variant catalog with off-target regions.

ReadvizFilename: The filename of the SVG image generated by REViewer based on the ExpansionHunter call reported in the "Genotype"
    column. This can be used to compute the public url and programatically retrieve this image from the gnomAD browser server.
