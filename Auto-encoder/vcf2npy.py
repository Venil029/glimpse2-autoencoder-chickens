import numpy as np

# Map VCF GT strings to integers:
#   0/0 → 0, 0/1 → 1, 1/1 → 2, ./. → -1
MAP = {'0/0': 0, '0/1': 1, '1/1': 2, './.': -1}

coords = []
rows = []

with open('raw_genotypes.txt') as f:
    for line in f:
        parts = line.strip().split('\t')
        chrom, pos, *gts = parts
        coords.append((chrom, pos))
        # Convert each GT string
        rows.append([MAP.get(gt, -1) for gt in gts])

# Build the genotype matrix (V variants × S samples)
G = np.array(rows, dtype=int)
np.save('genotypes.npy', G)

# Save variant coordinates in the same order
with open('variants.tsv', 'w') as out:
    out.write("CHROM\tPOS\n")
    for chrom, pos in coords:
        out.write(f"{chrom}\t{pos}\n")

print(f"Saved genotypes.npy with shape {G.shape}")

print(f"Saved variants.tsv with {len(coords)} lines")


