"""Literatur (PDF), Originaltitel unverändert. Was das Projekt woraus verwendet, steht in DATEN_LIZENZEN.md, Abschnitt 5.
In diesem Durchgang nicht verwendet: Henry (ICPR), EAGLE und die zwei Gerichtsentscheide (WBE-2021-464, SG VGN).

Die PDFs werden nicht mit dem Projekt weitergegeben (Lizenzen, siehe DATEN_LIZENZEN.md).
Wer sie lesen will, lädt sie selbst von den Originalquellen in den Ordner quellen/:
    .venv/Scripts/python notebooks/quellen_liste.py
"""

QUELLEN_LISTE = [
    # Paper
    ("Hellekes_2022_Parking_space_inventory_from_above.pdf",
     "Parking space inventory from above: Detection on aerial images and estimation for unobserved regions",
     "https://elib.dlr.de/191145/1/Hellekes_et_al_2022_Parking_space_inventory_from_above.pdf"),
    ("Henry_2021_ISPRS_Citywide_estimation_of_parking_space.pdf",
     "Citywide estimation of parking space using aerial imagery and OSM data fusion with deep learning and fine-grained annotation",
     "https://isprs-archives.copernicus.org/articles/XLIII-B2-2021/479/2021/isprs-archives-XLIII-B2-2021-479-2021.pdf"),
    ("Henry_ICPR_Aerial_Road_Segmentation_Topological_Label_Noise.pdf",
     "Aerial Road Segmentation in the Presence of Topological Label Noise",
     "https://elib.dlr.de/136343/1/Henry_et_al_Aerial_Road_Segmentation_Topological_Label_Noise.pdf"),
    ("Rauch_2025_Large-Scale_Mapping_of_Urban_Parking_Berlin.pdf",
     "Large-Scale Mapping of Urban Parking from Aerial Images: A Case Study in Berlin, Germany",
     "https://isprs-archives.copernicus.org/articles/XLVIII-4-W16-2025/83/2025/isprs-archives-XLVIII-4-W16-2025-83-2025.pdf"),
    ("Kurz_2025_Generating_Training_Data_by_Projecting_Existing_Labels.pdf",
     "Generating Training Data for Deep Learning-Based Segmentation Algorithms by Projecting Existing Labels onto Additional Aerial Images",
     "https://isprs-archives.copernicus.org/articles/XLVIII-M-6-2025/189/2025/isprs-archives-XLVIII-M-6-2025-189-2025.pdf"),
    ("Azimi_2020_EAGLE.pdf",
     "EAGLE: Large-scale Vehicle Detection Dataset in Real-World Scenarios using Aerial Imagery",
     "https://arxiv.org/pdf/2007.06124"),
    # Merkblaetter Kanton Zuerich
    ("Merkblatt_Orthofoto_2024_2025.pdf",
     "Merkblatt zur Nutzung des Orthofotos des Kantons Zürich aus Luftbildern, die 2024 und 2025 erstellt wurden",
     "https://www.geolion.zh.ch/geodatensatz/5011/pdf"),
    ("Merkblatt_Nutzung_Orthofoto_ab_2020.pdf",
     "Merkblatt zur Nutzung des Orthofotos des Kantons Zürich aus Luftbildern, die ab 2020 erstellt wurden",
     "https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/planen-bauen/geoinformation/geodaten/Merkblatt_Nutzung_Orthofoto_ab_2020.pdf"),
    # Schweizer Platzmasse (Sekundaerquellen)
    ("WBE-2021-464_2022-03-28.pdf", "WBE-2021-464_2022-03-28",
     "https://files.entscheidsuche.ch/chunks/AG/OG/006/WBE-2021-464_2022-03-28.pdf"),
    ("Bern_2-10-22_Parkfelder_1-2.pdf", "2.10.22 Parkfelder 1/2",
     "https://www.bern.ch/themen/planen-und-bauen/bern-baut/planen-und-projektieren/c-normalien/2-strassenbau/2-10-strassenmarkierungen-1/2-10-22-parkfelder-1-2-auto.pdf"),
    ("SG_VGN_001_B-2004-22_2004-12-02.pdf", "SG VGN 001 B 2004 22 2004 12 02",
     "https://entscheidsuche.ch/docs/SG_Publikationen/SG_VGN_001_B-2004-22_2004-12-02.pdf"),
    # Amtliche Unterlagen, die die Masse der Norm VSS 40 291 wiedergeben
    ("KantonBern_Arbeitshilfe_Parkierung_2026.pdf", "Arbeitshilfe Parkierung (Tiefbauamt Kanton Bern, 01.01.2026)",
     "https://www.bvd.be.ch/content/dam/bvd/dokumente/de/tba/strassen/sm-signalisation-markierung/sm-ah-parkierung.pdf"),
    ("Zuerich_DAV_Normblatt_Laengsparkfeld_2022.pdf", "Normblatt Ausfahrtstyp A, Längsparkfeld (Stadt Zürich, DAV, 06.05.2022)",
     "https://www.stadt-zuerich.ch/content/dam/web/de/planen-bauen/baubewilligungen/dokumente/verkehrssicherheit/normblatt-ausfahrtstyp-a-laengsparkfeld-ohne-trottoir.pdf"),
    ("Zuerich_DAV_Normblatt_Senkrechtparkfeld_2022.pdf", "Normblatt Ausfahrtstyp A, Senkrechtparkfeld (Stadt Zürich, DAV, 12.04.2022)",
     "https://www.stadt-zuerich.ch/content/dam/web/de/planen-bauen/baubewilligungen/dokumente/verkehrssicherheit/normblatt-ausfahrtstyp-a-senkrechtparkfeld-ohne-trottoir.pdf"),
    ("Zuerich_DAV_Normblatt_Schraegparkfeld_2024.pdf", "Normblatt Ausfahrtstyp A, Schrägparkfeld (Stadt Zürich, DAV, 07.08.2024)",
     "https://www.stadt-zuerich.ch/content/dam/web/de/planen-bauen/baubewilligungen/dokumente/verkehrssicherheit/normblatt-ausfahrtstyp-a-schraegparkfeld-ohne-trottoir.pdf"),
]


if __name__ == "__main__":
    from pathlib import Path
    import requests
    ziel = Path(__file__).resolve().parents[1] / "quellen"
    ziel.mkdir(exist_ok=True)
    for datei, titel, url in QUELLEN_LISTE:
        if (ziel / datei).exists():
            print("vorhanden:", datei)
            continue
        try:
            antwort = requests.get(url, timeout=120, headers={"User-Agent": "parkplatz-pilot"})
            antwort.raise_for_status()
            (ziel / datei).write_bytes(antwort.content)
            print("geladen:  ", datei)
        except Exception as fehler:          # weiter mit der nächsten Quelle
            print("FEHLER:   ", datei, fehler)
