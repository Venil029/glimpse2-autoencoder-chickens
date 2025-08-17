#!/bin/bash
#$ -N postimp_filter
#$ -cwd
#$ -t 1-18
#$ -pe smp 1
#$ -l h_vmem=4G
#$ -o logs/filter_$TASK_ID.out
#$ -e logs/filter_$TASK_ID.err

module load bcftools

# your samples and coverages
SAMPLES=(OL1393a OL1397a OL1677)
COVS=(cov0.1 cov0.25 cov0.5 cov0.75 cov1.0 cov2.0)

# the GP thresholds you want
GP_LIST=(0 0.7 0.8 0.9 0.95 0.99)

# which sample+cov this task is:
IDX=$((SGE_TASK_ID-1))
SAMPLE=${SAMPLES[$((IDX % ${#SAMPLES[@]}))]}
COV=${COVS[$((IDX / ${#SAMPLES[@]}))]}

echo "Task $SGE_TASK_ID → $SAMPLE @ $COV"

IN_BCF="calls/imputed/${COV}/${SAMPLE}/${SAMPLE}.chr2.ligated.renamed.bcf"
if [[ ! -f "$IN_BCF" ]]; then
  echo "[ERROR] Missing input: $IN_BCF"
  exit 1
fi

OUT_DIR="calls/filtered_gp/${COV}/${SAMPLE}"
mkdir -p "$OUT_DIR"

for GP in "${GP_LIST[@]}"; do
  # build a label: 0→0, 0.7→7, 0.95→95 etc
  if (( $(echo "$GP==0" | bc -l) )); then
    L="0"
  else
    L=$(echo "$GP" | sed 's/^0\.//;s/\.//')
  fi

  OUT_BCF="${OUT_DIR}/${SAMPLE}.chr2.filtered.gp${L}.bcf"

  if (( $(echo "$GP==0" | bc -l) )); then
    echo "  • GP=0 (no filtering) → $OUT_BCF"
    bcftools view "$IN_BCF" -Ob -o "$OUT_BCF"
  else
    echo "  • GP≥${GP} → $OUT_BCF"
    bcftools view -i "FORMAT/GP[*]>=${GP}" "$IN_BCF" -Ob -o "$OUT_BCF"
  fi

  bcftools index -c "$OUT_BCF"
done

echo " Done $SAMPLE @ $COV"

