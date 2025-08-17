# impute.py
import numpy as np
import torch
from model import ConvAE

# PARAMETERS: must match train.py
WINDOW, STEP, LATENT_DIM, MASK_VAL = 1000, 500, 128, -1

# 1) Load the raw genotype matrix (variants × 3 samples)
G = np.load('imputation_data/genotypes.npy')  # shape (V, 3)
V, S = G.shape

# 2) Load the trained AE
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = ConvAE(n_samples=S, window=WINDOW, latent_dim=LATENT_DIM).to(device)
model.load_state_dict(torch.load('ae_checkpoint.pt', map_location=device))
model.eval()

# 3) Prepare output array (float to hold reconstructions)
G_imp = G.astype(float).copy()

# 4) Slide over windows and impute
for start in range(0, V - WINDOW + 1, STEP):
    win = torch.from_numpy(G[start:start+WINDOW, :].T).unsqueeze(0).to(device).float()
    with torch.no_grad():
        rec = model(win)[0].cpu().numpy().T    # (WINDOW, 3)
    mask = (G[start:start+WINDOW, :] == MASK_VAL)
    # Round reconstructed values to nearest integer genotype
    G_imp[start:start+WINDOW, :][mask] = np.round(rec[mask])

# 5) Save the imputed matrix
np.save('imputation_data/genotypes_imputed.npy', G_imp)
print("Imputation complete:", G_imp.shape)
