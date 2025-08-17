Reconstructing Genotypes from Ultra-Low-Coverage Ancient Chicken DNA:

A Benchmark of GLIMPSE2 and Deep-Learning Autoencoders

Overview
This repository contains the full analysis pipeline and scripts developed for my MSc thesis, which investigates how to rebuild accurate genotypes from ultra-low-coverage ancient chicken DNA. Ancient DNA (aDNA) is often degraded and sequenced at very low depths, making it difficult to study population history, domestication, and evolutionary processes.

To address this, two complementary imputation strategies are compared:
1. GLIMPSE2 – a haplotype-aware statistical method designed to maximize accuracy from low-coverage sequencing data.
2. Autoencoder (AE) – a deep-learning approach that learns patterns of genetic variation directly from a modern chicken reference panel and applies them to sparse ancient genomes.
By systematically benchmarking both approaches on downsampled high-coverage ancient chicken genomes, this project explores their relative strengths and limitations, and identifies best practices for future ancient DNA studies.

Goals of the Project

1.To test whether statistical haplotype-based methods (GLIMPSE2) and deep learning (autoencoders) can accurately reconstruct genotypes at ultra-low sequencing depths (0.1×–2×).

2.To determine minimum coverage thresholds for reliable imputation in ancient DNA studies.

3.To evaluate the impact of genotype probability (GP) filtering in rescuing accuracy at very low depths.

4.To explore whether deep learning can provide more coverage-independent performance compared to traditional statistical models.
Repository Structure

The project is divided into two main workflows, reflecting the two imputation strategies:

GLIMPSE2/ – Contains scripts for the stepwise statistical pipeline:
Preparing truth genotypes from high-coverage BAMs.
Genome chunking, reference panel splitting, phasing, ligating, and concordance analysis.
Genotype probability filtering and visualisation.

Auto-encoder/ – Contains Python scripts for the deep-learning workflow:
Converting VCFs to NumPy genotype matrices.
Splitting data into sliding genomic windows.
Model definition, training, and imputation.
Converting predictions back into VCF format and validation.

Additional helper scripts and visualisation utilities are included in both pipelines.

Requirements
To reproduce the analysis, you will need:

GLIMPSE2 (for statistical imputation)
bcftools / samtools (for BAM/VCF manipulation)
Python 3.9+ with PyTorch, NumPy, pandas, matplotlib
High-quality reference genome, genetic map, and phased reference panel
Ancient BAM files (deduplicated, indexed)
(Optional) High-coverage truth VCFs for validation

Workflow 1: GLIMPSE2 (Statistical Approach)
This pipeline uses the haplotype-based imputation method GLIMPSE2. It proceeds in the following order:

1. Prepare truth genotypes – Generate high-confidence reference VCFs from high-coverage ancient BAM files.

2. Chunking – Divide the genome into smaller regions for manageable and efficient processing.

3. Split the reference panel – Align the phased modern reference panel with the defined chunks.

4. Phasing & imputation – Infer missing genotypes in each chunk by comparing low-coverage samples to the reference panel.

5. Ligating – Stitch the imputed chunks back into whole chromosomes.

6. Concordance analysis – Compare imputed VCFs against the truth data to evaluate accuracy.

7. Filtering – Apply genotype probability (GP) thresholds to keep only the most reliable calls.

8. Visualisation – Summarise accuracy across coverage levels and filtering thresholds.

Workflow 2: Autoencoder (Deep Learning Approach):
This pipeline uses a convolutional autoencoder (AE) to learn genetic patterns and reconstruct genotypes:

1. VCF preparation – Convert VCF files into a unified genotype dataset.

2. Data conversion – Transform VCFs into NumPy arrays for machine learning.

3. Windowing – Split genomic data into sliding windows of fixed length to preserve local haplotype structures.

4. Model design – Define the architecture of the convolutional autoencoder.

5. Training – Train the model on the reference dataset until it learns key genetic patterns.

6. Imputation – Apply the trained model to low-coverage ancient genomes.

7. Back-conversion – Convert model predictions back into VCF format.

8. Validation & visualisation – Compare against truth data and plot accuracy metrics.

Citation:
If you use this repository in your research, please cite it as:
Belliappa, V. (2025). Reconstructing Genotypes from Ultra-Low-Coverage Ancient Chicken DNA: A Benchmark of GLIMPSE2 and Deep-Learning Autoencoders.

Acknowledgements:
This work was carried out as part of my MSc Bioinformatics dissertation at Queen Mary University of London.
I would like to thank my supervisors, lab colleagues, and the open-source community for tools like GLIMPSE2, as well as resources such as ChatGPT, Perplexity, and Grammarly, which supported refinement of ideas, writing, and code.

Contact:
For questions, suggestions, or collaborations, please reach out:
Vishnu Belliappa Kibbetta
Email: vishnubelliappa17@gmail.com
GitHub: https://github.com/Venil029/glimpse2-autoencoder-chickens/edit/main/.
