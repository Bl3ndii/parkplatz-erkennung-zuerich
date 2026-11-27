# Daten, Quellen und Lizenzen

Dieses Repository enthält **Code, Dokumentation und abgeleitete Ergebnisse**. Die Rohdaten sind **nicht** enthalten. Jede Nutzerin und jeder Nutzer lädt sie selbst von den Originalquellen mit dem Notebook `notebooks/rohdaten_herunterladen.ipynb` herunter. Die Datei `daten/roh/MANIFEST.csv` listet jede Quelle mit URL, Lizenz, Abrufdatum und Prüfsumme (SHA-256).

Die Lizenzangaben unten geben die Angaben der Anbieter zum Zeitpunkt des Abrufs (26.11.2026) wieder. Massgebend sind die Lizenztexte der Anbieter. Diese Übersicht ist keine Rechtsberatung.

## 1. Lizenzen dieses Repositorys

Stand 27.11.2026, für den Durchgang mit eigener Ground Truth. Der erste Durchgang (Pilot 1) ist in [PILOT1.md](PILOT1.md) beschrieben; sein Quellcode und seine Modelle sind nicht Teil dieses Repositorys.

| Inhalt | Lizenz |
| --- | --- |
| Code (`notebooks/*.py`, Code-Zellen der Notebooks, `ground_truth_vorlage.html`, `dashboard_vorlage.html`) | [MIT](LICENSE) |
| Texte, Abbildungen, Ergebnisdateien und Dashboard samt GeoPackages (`*.md`, `ergebnisse/`, `daten/ground_truth/`, `daten/verarbeitet/*.json, *.csv, *.geojson`) | [CC BY 4.0](LICENSE-docs): Nutzung frei, mit Namensnennung „Bl3ndii, parkplatz-erkennung-zuerich“ |
| Gelernte Netze dieses Durchgangs | nicht im Repository; siehe Abschnitt 4 |

## 2. Verwendete Daten

| Daten | Anbieter | Lizenz / Bedingung | Im Repository |
| --- | --- | --- | --- |
| Öffentlich zugängliche Parkplätze DAV (2025) | Stadt Zürich, Dienstabteilung Verkehr | CC0 (Open Data Zürich) | nur abgeleitet: als Vorschläge in der Ground Truth und als Vergleichszahl je Testausschnitt (`ergebnisse/zaehlung.csv`) |
| Öffentlich zugängliche Strassenparkplätze OGD (Stand 31.12.2021) | Stadt Zürich, Tiefbauamt | CC0 | nur abgeleitet: als Vergleichszahl je Testausschnitt |
| Amtliche Vermessungsdaten Stadt Zürich, Jahresendstand 2025 | Stadt Zürich, Geomatik + Vermessung | CC0 | nur abgeleitet: Umriss des Gebiets (`daten/verarbeitet/gebiet.geojson`) |
| Stadtkreise | Stadt Zürich | CC0 | nur abgeleitet: Umriss des Gebiets |
| Orthofoto Sommer RGB/Infrarot 2024/25 (OGD) | Kanton Zürich, Amt für Raumentwicklung, Geoinformation | Open Government Data; „Open use. Must provide the source.“ → **Quelle nennen** | nur als Bildausschnitte in den Notebooks und in `ergebnisse/abbildungen/` |
| Orthofoto Frühjahr 2021 (OGD) | Kanton Zürich, Amt für Raumentwicklung, Geoinformation | Open use, Quelle nennen | nur als Bildausschnitte in den Notebooks und in `ergebnisse/abbildungen/` |
| Orthofoto Sommer 2026, 10 cm | Kanton Zürich, Amt für Raumentwicklung, Geoinformation | Open use, Quelle nennen | nur als Bildausschnitte in Notebook 01 (Vergleich dreier Aufnahmen) und in `ergebnisse/abbildungen/` |
| Amtliche Vermessung, Liegenschaften (Jahresendstand 2025) und Liegenschafteninventar OGD | Stadt Zürich | CC0 | nur abgeleitet: Merkmal «Strassenraum» je Feld und Auszählungen in Notebook 01 |
| DenseNet-121, ImageNet-Gewichte | PyTorch / torchvision | Code BSD-3-Clause; Gewichte auf ImageNet trainiert (ImageNet: nicht kommerzielle Forschung) | nein, wird beim ersten Lauf geladen |

Die genaue Liste aller geladenen Dateien steht in `daten/roh/MANIFEST.csv`. Dateien, die nur der erste Durchgang verwendet hat (zum Beispiel der EAGLE-Datensatz der DLR), stehen seit dem 27.11.2026 nicht mehr darin.

**Quellenangabe für Abbildungen:**
> Orthofoto: © Kanton Zürich, Orthofoto Frühjahr 2021, Sommer 2024/25 und Sommer 2026 (OGD). Parkplatzdaten und amtliche Vermessung: Stadt Zürich, Open Data (CC0).

## 3. Dienste im Dashboard

`ergebnisse/dashboard/dashboard.html` lädt beim Öffnen Inhalte aus dem Internet:

| Dienst | Anbieter | Bedingung |
| --- | --- | --- |
| Leaflet 1.9.4 (über unpkg.com) | Volodymyr Agafonkin und Mitwirkende | BSD-2-Clause |
| WMS Orthofoto (`wms.zh.ch/OrthoZHWMS`, Ebenen Frühjahr 2021/22 und Sommer 2024/25) | Kanton Zürich | Quelle nennen |
| Kacheln OpenStreetMap | OpenStreetMap Foundation | Daten ODbL, „© OpenStreetMap-Mitwirkende“; Nutzungsrichtlinie für Kachelserver beachten (keine Massenabrufe) |
| Adresssuche (`api3.geo.admin.ch`) | Bundesamt für Landestopografie swisstopo | Nutzungsbedingungen geo.admin.ch; es wird nur der eingetippte Suchtext gesendet |

Das Dashboard enthält ausserdem die amtlichen Punkte des Gebiets als zuschaltbare Ebene (Stadt Zürich, CC0) und in den GeoPackages die vom Autor erfasste Ground Truth (CC BY 4.0).

## 4. Gelernte Netze

Die Netze dieses Durchgangs (Dense-U-Net, ausgehend von ImageNet-Gewichten aus torchvision) liegen nicht im Repository. Wer sie mit `nachtlauf.py --training` neu lernt, beachte: Weil die Startgewichte auf ImageNet beruhen, dessen Bedingungen nur nicht kommerzielle Forschung erlauben, wird empfohlen, die Netze **nur für nicht kommerzielle Forschung und Lehre** zu verwenden.

## 5. Literatur und Normen (nur zitiert, PDFs nicht enthalten)

Die PDFs liegen nicht im Repository. `python notebooks/quellen_liste.py` lädt sie von den Originalquellen in den Ordner `quellen/`; in der Datei stehen alle Links. Was das Projekt aus welcher Arbeit übernimmt und wo es abweicht, steht mit Fundstelle in `notebooks/01b_methodik_leitfaden.ipynb`, Abschnitt 8.4. Die Platzmasse der Norm stehen dort in Abschnitt 1.

**Arbeiten, auf die sich die Methode stützt**

| Werk | Rolle in diesem Durchgang | Lizenz |
| --- | --- | --- |
| [Henry et al. (2021): Citywide estimation of parking space using aerial imagery and OSM data fusion with deep learning and fine-grained annotation](https://isprs-archives.copernicus.org/articles/XLIII-B2-2021/479/2021/isprs-archives-XLIII-B2-2021-479-2021.pdf), ISPRS Archives XLIII-B2-2021 | Netz (Dense-U-Net mit DenseNet-121) und Einstellungen des Lernens; Lernen, Validieren und Testen räumlich trennen; eine einzige Klasse «Parkfläche» | CC BY 4.0 |
| [Hellekes et al. (2022): Parking space inventory from above: Detection on aerial images and estimation for unobserved regions](https://elib.dlr.de/191145/1/Hellekes_et_al_2022_Parking_space_inventory_from_above.pdf), IET Intelligent Transport Systems | Parkfläche nur dort beschriften, wo sie eindeutig erkennbar ist; Einstellungen des Lernens. Das Zusammenlegen mehrerer Bilder ist in diesem Durchgang nicht gerechnet | CC BY-NC |
| [Kurz et al. (2025): Generating Training Data for Deep Learning-Based Segmentation Algorithms by Projecting Existing Labels onto Additional Aerial Images](https://isprs-archives.copernicus.org/articles/XLVIII-M-6-2025/189/2025/isprs-archives-XLVIII-M-6-2025-189-2025.pdf), ISPRS Archives XLVIII-M-6-2025 | Merkmale «unsicher» und «schwer erkennbar» in der Beschriftung; die Lage der Felder einmal beschriften und für zwei Luftbilder derselben Stelle nutzen | CC BY 4.0 |
| [Rauch et al. (2025): Large-Scale Mapping of Urban Parking from Aerial Images: A Case Study in Berlin, Germany](https://isprs-archives.copernicus.org/articles/XLVIII-4-W16-2025/83/2025/isprs-archives-XLVIII-4-W16-2025-83-2025.pdf), ISPRS Archives XLVIII-4/W16-2025 | Anzahl = Fläche ÷ Platzgrösse; verdeckte Plätze werden nicht ergänzt. Nicht übernommen: die Parkart aus erkannten Fahrzeugen | CC BY 4.0 |

**Vergleichswerte aus diesen Arbeiten** (IoU der Klasse Parkfläche, abgelesen am 25.11.2026): Hellekes 2022 68,2 %; Henry 2021 68,1 bis 69,8 % je nach Netz; Kurz 2025 61,5 % auf Bildern anderer Städte. Andere Städte, andere Bilder und eine andere Lösung: Die Werte sind nur als Grössenordnung mit diesem Projekt vergleichbar.

**Normen und amtliche Unterlagen**

| Unterlage | Wozu | Lizenz |
| --- | --- | --- |
| Tiefbauamt des Kantons Bern: Arbeitshilfe Parkierung (01.01.2026); Stadt Bern: Normalie 2.10.22 Parkfelder; Stadt Zürich, Dienstabteilung Verkehr: Normblätter Längs-, Senkrecht- und Schrägparkfeld (2022, 2024) | Sie geben die Masse der Norm VSS 40 291 wieder (die Norm selbst ist kostenpflichtig und wurde nicht eingesehen). Daraus stammt die Tiefe eines Platzes: 5,00 m und 1,90 m | keine Lizenz angegeben; nur verlinkt |
| Kanton Zürich: Merkblätter zur Nutzung des Orthofotos (Luftbilder ab 2020; Luftbilder 2024 und 2025) | Flugtage und Lagegenauigkeit der Luftbilder (Notebook 01) | keine Lizenz angegeben; nur verlinkt |

**Gelesen, in diesem Durchgang nicht verwendet:** Henry, Fraundorfer, Vig (ICPR 2020), Aerial Road Segmentation in the Presence of Topological Label Noise; Azimi et al. (2020), EAGLE (Fahrzeugdatensatz des ersten Durchgangs); zwei Gerichtsentscheide zu Parkfeldmassen (Aargau 2022, St. Gallen 2004) aus der ersten Recherche, an deren Stelle die amtlichen Unterlagen oben getreten sind.
