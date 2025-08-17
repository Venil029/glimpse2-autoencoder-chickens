# model.py
import torch
import torch.nn as nn

class ConvAE(nn.Module):
    """


    A 1D convolutional autoencoder for genotype windows.
    Input shape: (batch, channels=3 samples, length=1000 SNPs)
    """

    def __init__(self, n_samples=3, window=1000, latent_dim=128):
        super().__init__()
        # Encoder: conv → conv → flatten → linear to latent
        self.encoder = nn.Sequential(
            nn.Conv1d(n_samples, 64, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.Conv1d(64, 32, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.Flatten(),
            nn.Linear(32 * window, latent_dim)
        )
        # Decoder: linear → unflatten → deconv → deconv to channels
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 32 * window),
            nn.ReLU(inplace=True),
            nn.Unflatten(1, (32, window)),
            nn.ConvTranspose1d(32, 64, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.ConvTranspose1d(64, n_samples, kernel_size=5, padding=2)
        )

    def forward(self, x):
        # x: (B, 3, 1000)
        z = self.encoder(x)
        return self.decoder(z)
