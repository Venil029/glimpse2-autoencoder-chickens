import matplotlib.pyplot as plt

# Data
samples = ['OL1393', 'OL1397', 'OL1677']
snp_nrd = [0.12, 0.10, 0.09]       # Non-Reference Discordance (%)
indel_nrd = [1.94, 2.41, 1.37]     # Non-Reference Discordance (%)
snp_r2 = [99.6, 99.5, 99.7]        # Converted to % for plotting
indel_r2 = [96.0, 95.8, 96.3]      # Converted to % for plotting

# Create figure
plt.figure(figsize=(12,6))

# Plot 1: Error Rates
plt.subplot(1,2,1)
plt.bar(samples, snp_nrd, width=0.4, label='SNPs', color='blue', align='center')
plt.bar(samples, indel_nrd, width=0.4, label='Indels', color='orange', bottom=snp_nrd, align='center')
plt.axhline(y=1, color='red', linestyle='--')
plt.ylabel('Non-Reference Discordance (%)')
plt.title('A. Error Rates')
plt.legend()

# Plot 2: Concordance
plt.subplot(1,2,2)
plt.bar(samples, snp_r2, width=0.4, label='SNPs', color='blue', align='center')
plt.bar(samples, indel_r2, width=0.4, label='Indels', color='orange', align='edge')
plt.axhline(y=95, color='green', linestyle='--')
plt.ylabel('Concordance (%)')
plt.title('B. Imputation Quality')
plt.legend()

plt.tight_layout()
plt.savefig('imputation_quality_simple.png')
print("Graph saved as imputation_quality_simple.png")


