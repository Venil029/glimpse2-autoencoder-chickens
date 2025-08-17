#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import argparse
import gzip
import matplotlib.pyplot as plt

def read_grp(path):
    """
    Read an rsquare.grp.txt.gz file created by GLIMPSE2_concordance.
    Assumes each data line has at least 4 whitespace-separated columns:
      0: bin index
      1: count of variants
      2: allele-frequency midpoint
      3: imputation r-squared value
    """
    bins = []
    r2_vals = []
    with gzip.open(path, 'rt') as f:
        for line in f:
            line = line.strip()
            # skip empty or comment lines
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            # need at least 4 columns: idx, count, midAF, r2
            if len(parts) < 4:
                continue
            try:
                af = float(parts[2])
                r2 = float(parts[3])
            except ValueError:
                continue
            bins.append(af)
            r2_vals.append(r2)
    return bins, r2_vals

def main():
    p = argparse.ArgumentParser(
        description="Plot GLIMPSE2 concordance r² by MAF bin"
    )
    p.add_argument(
        '--rsquare', '-r', nargs='+', required=True,
        help="Paths to *.rsquare.grp.txt.gz files"
    )
    p.add_argument(
        '--labels', '-l', nargs='+',
        help="Sample labels, in same order as --rsquare"
    )
    p.add_argument(
        '--out', '-o', default='rsquare_by_maf.png',
        help="Output PNG file"
    )
    args = p.parse_args()
    if args.labels and len(args.labels) != len(args.rsquare):
        p.error("Number of labels must match number of --rsquare files")

    plt.figure()
    for idx, path in enumerate(args.rsquare):
        label = args.labels[idx] if args.labels else path
        bins, r2_vals = read_grp(path)
        if not bins:
            print(f"Warning: no data found in {path}")
            continue
        plt.plot(bins, r2_vals, marker='o', label=label)

    plt.xscale('log')
    plt.xlabel("Allele Frequency (midpoint)")
    plt.ylabel("Imputation r²")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.out)
    print(f"Saved plot to {args.out}")

if __name__ == "__main__":
    main()
