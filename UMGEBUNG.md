# Umgebung nachbauen

Diese Anleitung erzeugt dieselbe Python-Umgebung, mit der das Projekt gerechnet wurde. Stand 26.11.2026.

## Verwendete Umgebung

| Teil | Version |
| --- | --- |
| Betriebssystem | Windows 11 Pro (64 Bit) |
| Python | 3.11.9 |
| PyTorch | 2.11.0 mit CUDA 12.8 |
| GDAL (in rasterio enthalten) | 3.10.3 |
| PROJ (in pyproj enthalten) | 9.5.1 |
| MLflow | 3.18.0 (Protokoll der Trainingsläufe) |
| GPU | NVIDIA GeForce RTX 4070 Ti, 12 GB; Treiber 616.92 |
| Arbeitsspeicher | 32 GB |

Die genauen Versionen aller Pakete stehen in `requirements-lock.txt`; die direkt verwendeten in `requirements.txt`.

## Schritte

```bash
# 1. Python 3.11 installieren (python.org oder Microsoft Store)
# 2. Im Projektordner eine eigene Umgebung anlegen
python -m venv .venv

# 3. Pakete in genau diesen Versionen installieren
.venv/Scripts/python -m pip install -r requirements-lock.txt --extra-index-url https://download.pytorch.org/whl/cu128

# 4. Die Umgebung als Jupyter-Kernel anmelden (Name wird in den Notebooks verwendet)
.venv/Scripts/python -m ipykernel install --user --name parkplatz --display-name "Python (parkplatz)"

# 5. Jupyter starten und die Notebooks in der Reihenfolge 00 bis 13 ausführen.
#    Zuerst Notebook 00, Abschnitt 1 (Einstellungen), dann einmalig rohdaten_herunterladen.ipynb (Rohdaten), dann 00 bis 13.
.venv/Scripts/jupyter lab notebooks

# oder alle Notebooks automatisch nacheinander, mit vollem Lernen und der Karte des ganzen Gebiets (etwa 2,5 h)
.venv/Scripts/python notebooks/nachtlauf.py --training
```

Unter Linux heisst der Pfad `.venv/bin/` statt `.venv/Scripts/`.

## Hinweise

- **Ohne NVIDIA-GPU** laufen die Notebooks 00 bis 06 normal; Lernen und Vorhersage (07, 08, 11 und 12) wären auf der CPU sehr langsam.
- **Ohne `--training`** braucht Notebook 07 die gelernten Netze in `ergebnisse/modelle/`. Sie liegen nicht im Repository (Dateien über 50 MB).
- **Windows und Grafikspeicher:** Windows kann bei vollem Grafikspeicher still in den Arbeitsspeicher auslagern. Notebook 07 begrenzt PyTorch deshalb auf 95 % des Grafikspeichers.
- **ImageNet-Gewichte** des Encoders werden beim ersten Lauf nach `daten/roh/modelle/torch/` geladen.
- **Literatur:** `.venv/Scripts/python notebooks/quellen_liste.py` lädt die PDFs von den Originalquellen nach `quellen/`.
- **MLflow:** Trainingsläufe stehen in `ergebnisse/mlflow.db`; ansehen mit `.venv/Scripts/mlflow ui --backend-store-uri sqlite:///ergebnisse/mlflow.db`.
- Andere Versionen können funktionieren, ergeben aber nicht zwingend dieselben Zahlen.
