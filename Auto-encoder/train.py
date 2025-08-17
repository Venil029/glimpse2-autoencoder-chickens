# train.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from dataset import GenotypeWindowDataset
from model import ConvAE

def main():
    # Hyperparameters
    WINDOW, STEP   = 1000, 500
    BATCH, EPOCHS  = 32, 50
    LR             = 1e-3
    LATENT_DIM     = 128
    MASK_VAL       = -1

    # 1) Load data
    ds     = GenotypeWindowDataset('imputation_data/genotypes.npy',
                                   window=WINDOW,
                                   step=STEP,
                                   mask_val=MASK_VAL)
    loader = DataLoader(ds, batch_size=BATCH, shuffle=True, num_workers=2)

    # 2) Build model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model  = ConvAE(n_samples=3, window=WINDOW, latent_dim=LATENT_DIM).to(device)

    # 3) Optimizer & loss
    opt      = optim.Adam(model.parameters(), lr=LR)
    mse_fn   = nn.MSELoss(reduction='none')

    # 4) Training loop
    for epoch in range(1, EPOCHS+1):
        epoch_loss, epoch_obs = 0.0, 0
        for batch in loader:
            x = batch.to(device).float()           # (B,3,1000)
            pred = model(x)
            mask = (x != MASK_VAL).float()         # only observed sites

            loss = (mse_fn(pred, x) * mask).sum() / mask.sum()
            opt.zero_grad(); loss.backward(); opt.step()

            epoch_loss += loss.item() * mask.sum().item()
            epoch_obs  += mask.sum().item()

        print(f"Epoch {epoch:2d}/{EPOCHS} — MSE = {epoch_loss/epoch_obs:.6f}")

    # 5) Save the checkpoint
    torch.save(model.state_dict(), 'ae_checkpoint.pt')
    print("Training complete. Model saved as ae_checkpoint.pt")

if __name__ == '__main__':
    main()
