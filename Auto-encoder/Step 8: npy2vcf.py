#!/usr/bin/env python3
import numpy as np
import pysam

# Paths (adjust as needed)
GENO_NPY     = "imputation_data/genotypes_imputed.npy"
VARIANTS_TSV = "imputation_data/variants.tsv"
TEMPLATE_VCF = "merged.vcf.gz"
OUTPUT_VCF   = "imputed.vcf.gz"

# Samples must match the column order in the NPY
SAMPLES = ["OL1677", "OL1393", "OL1397"]

# Load data
G_imp = np.load(GENO_NPY)
variants = [l.strip().split("\t") for l in open(VARIANTS_TSV)][1:]

# Open VCFs
in_vcf  = pysam.VariantFile(TEMPLATE_VCF, "r")
out_vcf = pysam.VariantFile(OUTPUT_VCF, "w", header=in_vcf.header)

# Mapping 0,1,2 → GT tuples
GT_MAP = {0:(0,0), 1:(0,1), 2:(1,1)}

for (chrom,pos), row, rec in zip(variants, G_imp, in_vcf.fetch()):
    # sanity check
    if rec.chrom != chrom or str(rec.pos) != pos:
        raise RuntimeError(f"Mismatch at {chrom}:{pos}")

    for i, sample in enumerate(SAMPLES):
        code = int(round(row[i]))
        # clamp into [0,2]
        code = max(0, min(2, code))
        rec.samples[sample]["GT"] = GT_MAP[code]

    out_vcf.write(rec)

out_vcf.close()
in_vcf.close()
print(f"Wrote {OUTPUT_VCF}")

