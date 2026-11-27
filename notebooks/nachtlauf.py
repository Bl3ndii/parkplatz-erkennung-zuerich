"""Führt alle Notebooks nacheinander aus und protokolliert jeden Schritt.

Aufruf (im Projektordner):
    .venv/Scripts/python notebooks/nachtlauf.py              alle Notebooks 00-13
    .venv/Scripts/python notebooks/nachtlauf.py --ab 08      ab Notebook 08 (z. B. nach einer Korrektur)
    .venv/Scripts/python notebooks/nachtlauf.py --training   mit vollem Lernen in Notebook 07 (vier Läufe und der Nachtrag) und der Vorhersage für das ganze Gebiet in Notebook 12 (zusammen etwa 2,5 h)
    .venv/Scripts/python notebooks/nachtlauf.py --ab 12 --karte   nur die Vorhersage für das ganze Gebiet neu rechnen (etwa 30 min)
Rohdaten: einmalig vorher mit rohdaten_herunterladen.ipynb (nicht Teil dieses Laufs).

Bricht ein Notebook ab, stoppt der Lauf, damit kein späteres Notebook mit falschen Daten rechnet.
Protokoll: ergebnisse/nachtlauf_log.txt
"""
import ctypes
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
LOG = HIER.parent / "ergebnisse" / "nachtlauf_log.txt"
NOTEBOOKS = sorted(p.stem for p in HIER.glob("[0-9][0-9]_*.ipynb"))


def protokoll(text):
    zeile = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {text}"
    print(zeile, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(zeile + "\n")


def wach_bleiben(an):
    """Verhindert unter Windows den Ruhezustand, solange dieses Skript läuft (ändert keine Einstellung)."""
    if os.name == "nt":
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | (0x00000001 if an else 0))


def main():
    ab = sys.argv[sys.argv.index("--ab") + 1] if "--ab" in sys.argv else "00"
    schalter = "1" if "--training" in sys.argv else "0"
    karte = "1" if "--training" in sys.argv or "--karte" in sys.argv else "0"
    umgebung = dict(os.environ, LANGLAUF=schalter, NACHTRAG=schalter, KARTIERUNG=karte)   # volles Lernen (Notebook 07) und Vorhersage für das ganze Gebiet (Notebook 12)
    jupyter = Path(sys.executable).with_name("jupyter.exe" if os.name == "nt" else "jupyter")
    wach_bleiben(True)
    protokoll(f"Lauf gestartet (ab {ab}, volles Lernen: {umgebung['LANGLAUF'] == '1'})")
    try:
        for name in [n for n in NOTEBOOKS if n[:2] >= ab]:
            start = dt.datetime.now()
            protokoll(f"START {name}")
            r = subprocess.run([str(jupyter), "nbconvert", "--to", "notebook", "--execute", "--inplace", f"{name}.ipynb",
                                "--ExecutePreprocessor.timeout=-1", "--ExecutePreprocessor.kernel_name=parkplatz"],
                               cwd=HIER, env=umgebung, capture_output=True, text=True, encoding="utf-8", errors="replace")
            minuten = (dt.datetime.now() - start).total_seconds() / 60
            if r.returncode != 0:
                protokoll(f"FEHLER {name} nach {minuten:.1f} min\n{r.stderr[-3000:]}")
                sys.exit(1)
            protokoll(f"FERTIG {name} in {minuten:.1f} min")
        protokoll("Lauf erfolgreich beendet")
    finally:
        wach_bleiben(False)


if __name__ == "__main__":
    main()
