"""Bauplan des neuronalen Netzes (Dense-U-Net) – erklärt in Notebook 07.

Diese Datei gibt es nur, weil die Notebooks 07 (Training), 08 (Vorhersage) und 11 (Nachtrag)
genau denselben Bauplan brauchen. Alles andere steht sichtbar in den Notebooks.
Quellen: Henry ISPRS 2021, Hellekes 2022.
"""
import os
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]                                    # Projektordner
os.environ.setdefault("TORCH_HOME", str(ROOT / "daten" / "roh" / "modelle" / "torch"))   # ImageNet-Gewichte im Projekt
warnings.filterwarnings("ignore", message="IProgress not found")              # harmloser Hinweis eines Hilfspakets

import torch                           # noqa: E402
import torch.nn as nn                  # noqa: E402
import torch.nn.functional as F        # noqa: E402
import torchvision                     # noqa: E402

GERAET = "cuda" if torch.cuda.is_available() else "cpu"           # Grafikkarte, falls vorhanden
MITTEL = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)        # Farbmittel von ImageNet (Rot, Grün, Blau)
STREUUNG = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)      # Farbstreuung von ImageNet


class DichterBlock(nn.Module):
    """Dichter Block: jede Schicht erhält die Ausgaben aller vorherigen Schichten (wie in DenseNet)."""
    def __init__(self, kanaele_ein, wachstum=32, schichten=4):
        super().__init__()
        self.schichten = nn.ModuleList()
        k = kanaele_ein
        for _ in range(schichten):
            self.schichten.append(nn.Sequential(nn.BatchNorm2d(k), nn.ReLU(inplace=True),
                                                nn.Conv2d(k, wachstum, 3, padding=1, bias=False)))
            k += wachstum
        self.kanaele_aus = k

    def forward(self, x):
        for s in self.schichten:
            x = torch.cat([x, s(x)], 1)
        return x


class DenseUNet(nn.Module):
    """U-förmiges Netz: Encoder = DenseNet-121 (ImageNet), Decoder = dichte Blöcke mit Skip-Connections."""
    def __init__(self, klassen=2):
        super().__init__()
        f = torchvision.models.densenet121(weights="IMAGENET1K_V1").features
        self.stufe0 = nn.Sequential(f.conv0, f.norm0, f.relu0)              # 64 Kanäle, 1/2 Bildgrösse
        self.stufe1 = nn.Sequential(f.pool0, f.denseblock1)                # 256, 1/4
        self.stufe2 = nn.Sequential(f.transition1, f.denseblock2)          # 512, 1/8
        self.stufe3 = nn.Sequential(f.transition2, f.denseblock3)          # 1024, 1/16
        self.stufe4 = nn.Sequential(f.transition3, f.denseblock4, f.norm5) # 1024, 1/32
        skip = [1024, 512, 256, 64]
        k = 1024
        self.decoder, self.reduktion = nn.ModuleList(), nn.ModuleList()
        for s, aus in zip(skip, [512, 256, 128, 64]):
            blk = DichterBlock(k + s)
            self.decoder.append(blk)
            self.reduktion.append(nn.Conv2d(blk.kanaele_aus, aus, 1))
            k = aus
        self.kopf = nn.Sequential(nn.ConvTranspose2d(k, 32, 2, stride=2), nn.ReLU(inplace=True),
                                  nn.Conv2d(32, klassen, 1))
        for m in [*self.decoder.modules(), *self.reduktion.modules(), *self.kopf.modules()]:
            if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d)):
                nn.init.xavier_uniform_(m.weight)                          # Xavier-uniform wie Hellekes 2022

    def forward(self, x):
        s0 = self.stufe0(x)
        s1 = self.stufe1(s0)
        s2 = self.stufe2(s1)
        s3 = self.stufe3(s2)
        x = self.stufe4(s3)
        for blk, red, skip in zip(self.decoder, self.reduktion, [s3, s2, s1, s0]):
            x = F.interpolate(x, size=skip.shape[-2:], mode="bilinear", align_corners=False)
            x = red(blk(torch.cat([x, skip], 1)))
        return self.kopf(x)


def lade_modell(name):
    """Lädt ein gespeichertes Modell aus ergebnisse/modelle/ und schaltet es in den Anwendungsmodus."""
    modell = DenseUNet().to(GERAET)
    modell.load_state_dict(torch.load(ROOT / "ergebnisse" / "modelle" / f"{name}.pt", map_location=GERAET))
    modell.eval()
    return modell
