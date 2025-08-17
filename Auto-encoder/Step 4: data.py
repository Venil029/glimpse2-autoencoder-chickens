# dataset.py
import numpy as np
import torch
from torch.utils.data import Dataset

class GenotypeWindowDataset(Dataset):
    def __init__(self,
                 geno_npy='imputation_data/genotypes.npy',
                 window=1000,
                 step=500,
                 mask_val=-1):
        # Load the genotype matrix we just generated
        G = np.load(geno_npy)      # shape: (V, 3)
        V, S = G.shape
        self.windows = []
        for start in range(0, V - window + 1, step):
            win = G[start:start+window, :]            # (window, S)
            self.windows.append(win.T.astype(float))  # (S, window)
        self.mask_val = mask_val

    def __len__(self):
        return len(self.windows)

    def __getitem__(self, idx):
        return torch.from_numpy(self.windows[idx])
