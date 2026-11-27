# ML-Pipeline: Protokoll des Durchgangs mit eigener Ground Truth

Angelegt am 2026-11-26 nach der Regel des Skills `ml-pipeline` (16 Schritte, Freigaben A–D).
**Abweichung vom Skill (Entscheid des Auftraggebers):** Jupyter-Notebooks statt marimo. Die Regeln gelten unverändert.

> **Lesehilfe.** Diese Datei ist ein Protokoll in zeitlicher Reihenfolge: Freigaben, die 16 Schritte mit ihren Ergebnissen, dann die Nachträge vom 27.11.2026. Die gültige Methode steht in `notebooks/01b_methodik_leitfaden.ipynb`, Abschnitt 12; die Ergebnisse stehen in der README. Die frühere Durchsicht vom 26.11.2026 (amtliche DAV-Daten als Lösung, vier Testzonen, Zählung je Strassenabschnitt) ist überholt und wurde am 27.11.2026 aus dieser Datei genommen.
>
> **Zum Wort "Git-Verlauf".** Dieses Repository enthält den veröffentlichten Stand ohne die Geschichte der Arbeit (siehe den letzten Abschnitt). Wo dieses Protokoll vom "Git-Verlauf", von einem "Git-Stand", von Commits oder vom Tag `v0.1.0` spricht, ist das private Arbeitsarchiv des Autors gemeint. Was dort liegt, ist hier nicht öffentlich.

## Freigaben (Durchgang mit eigener Ground Truth, 27.11.2026)

Der Auftraggeber hat am 27.11.2026 die Erfassung der Ground Truth abgeschlossen und den ganzen Durchgang übertragen ("überlasse ich dir das Steuer"; Zeitrahmen vier Stunden, Hochladen eingeschlossen). Die Entscheide stehen in `notebooks/01b_methodik_leitfaden.ipynb`, Abschnitt 11.

- Override: Gate A - user approved the full autonomous run 2026-11-27 - reason: Auftraggeber übergibt Entscheide und Durchführung; Vertrag = Abschnitt 11 im Leitfaden
- Override: Gate B - user approved the full autonomous run 2026-11-27 - reason: wie Gate A; Testblöcke werden in Notebook 02 vor dem Lernen festgelegt
- Override: Gate C - user approved the full autonomous run 2026-11-27 - reason: wie Gate A; Testblöcke werden einmal ausgewertet (Notebooks 08 bis 10)
- Override: final test - user approved a second evaluation 2026-11-27 - reason: beim Lauf A_10cm lag die beste Epoche am Ende (01b, 7.4); Gegenprobe mit 60 Epochen nur für diesen Lauf (Notebook 11); die erste Auswertung bleibt das Ergebnis (01b, Abschnitt 11.2, N2)

Model rationale:
- traits: Bildsegmentierung, zwei Klassen, Parkfläche selten (rund 1 % der Pixel), 691 Ausschnitte von 51,2 m, räumlich abhängig (Blöcke)
- baseline: B0 überall 0; B1 mittlere Zahl sichtbarer Felder je Ausschnitt aus den Lernblöcken
- candidates: Dense-U-Net mit DenseNet-121 (wie Henry 2021, Hellekes 2022), je Versuch (2021, 2024/25) und Auflösung (5 cm, 10 cm) ein Lauf
- ruled out: Suche nach Klassengewicht oder Verlust (kein Zeitbudget, wäre ein geratener Wert); zufällige Aufteilung einzelner Kacheln (räumliche Abhängigkeit)
- metric: IoU der Parkfläche auf der Validierung für die Wahl von Epoche und Schwelle; in den Testblöcken einmal: IoU, MAE und Bias der Zählung je Ausschnitt, Delta zu amtlichen Daten

## Schritte (Durchgang mit eigener Ground Truth, 27.11.2026)

In diesem Durchgang ist die Lösung zum Lernen und Prüfen die von Hand gesetzte Ground Truth; die amtlichen Daten dienen nur für das Delta.

| Nr. | Schritt | Notebook | Status |
| --- | --- | --- | --- |
| 1 | Dateninspektion | 00, 01, `ground_truth_pruefen` | erledigt |
| 2 | Explorative Analyse | 01 (auch Abschnitt 14: Grundstücke), `ground_truth_pruefen` | erledigt |
| 3 | Vorhersageproblem | 01b, Abschnitt 11 (E1 bis E12) | erledigt, im Auftrag entschieden |
| 4 | Bereinigung | 05 (Kategorien: verdeckt, unsicher, Streifen, einzeln = nicht bewertet) | erledigt |
| 5 | Aufbereitung | 03 (Reihen, Platzmasse), 04 (Kästchen) | erledigt |
| 6 | Aufteilung | 02 (62 Blöcke: 38 lernen, 9 validieren, 15 testen; Seed 42; vor dem Lernen) | erledigt |
| 7 | Merkmale | RGB; Infrarot ungenutzt | erledigt |
| 8 | Vorverarbeitung | 05 (Kacheln 512 px; 10 cm = Mittel aus 2 × 2 Pixeln) | erledigt |
| 9 | Baseline | 06 (B0 überall 0; B1 Mittel der Lern-Ausschnitte) | erledigt |
| 10 | Training | 07 (vier Läufe: A/B × 5/10 cm; 16 bzw. 40 Epochen; Nachtrag: `A_10cm_lang` mit 60 Epochen) | erledigt |
| 11 | Hyperparameter | keine Suche; nur die Schwelle, auf der Validierung gewählt | erledigt |
| 12 | Bewertung Validierung | 07, Abschnitte 8 bis 10 | erledigt |
| 13 | Fehleranalyse | 10 (IoU je Block, Fehler je Ausschnitt, Zerlegung des Deltas, Abbildung der Fehler) | erledigt |
| 14 | Endprüfung Test | 08, 09, 10 (einmal ausgewertet); 11 (zweite Auswertung nur für `A_10cm_lang`, als Gegenprobe) | erledigt |
| 15 | Anwendung | 12 (Karte des ganzen Gebiets, GeoPackage je Lauf), 13 (Dashboard); im ersten Lauf nicht gemacht, am 27.11.2026 nachgeholt (01b, 11.3) | erledigt |
| 16 | Überwachung / Nachtraining | offen: Wiederholungsprobe der Ground Truth, Lernkurve über die Datenmenge | offen |

### Ergebnisse je Schritt

- **Ground Truth:** 691 von 691 Ausschnitten abgeschlossen, 3'269 gesetzte Felder (1'029 aus DAV-Vorschlägen übernommen, 2'240 neu). Kontroll-Ausschnitte: 92 % der verborgenen DAV-Felder innerhalb von 2,5 m gefunden.
- **Schritt 5:** Platzbreite aus den Lernblöcken 2,50 m (eng) und 5,61 m (weit); Klasse aus der Reihe der Ringe stimmt an der DAV zu 96 %.
- **Prüfung vor dem Lernen (E8):** Die Zählformel gibt am Lösungsblatt die gesetzten Felder wieder (Verhältnis 1,003 bis 1,008).
- **Schritt 9:** B1 = 3,54 (Bild 2021) und 2,34 (Bild 2024/25) sichtbare Felder je Ausschnitt.
- **Schritt 10 und 12 (Validierung, gewählte Schwelle):** IoU A_5cm 0,566 (Schwelle 0,45), A_10cm 0,530 (0,40), B_5cm 0,466 (0,35), B_10cm 0,434 (0,50). Alle vier Lernkurven sind im letzten Viertel flach; bei A_10cm ist die beste Epoche die letzte (nicht verlängert). Bei Versuch B sinkt die Fehlernote nach der besten Epoche weiter, die IoU nicht (Überanpassung).
- Step 14 final test: 15 Testblöcke, 137 Ausschnitte, einmal ausgewertet am 27.11.2026. IoU / MAE je Ausschnitt / gezählt von wahr: A_5cm 0,618 / 0,86 / 664 von 708; A_10cm 0,582 / 1,11 / 626 von 708; B_5cm 0,569 / 0,85 / 454 von 500; B_10cm 0,487 / 1,26 / 395 von 500. Baseline B0: MAE 5,17 (A) und 3,65 (B). Nur Ausschnitte mit Feldern: MAE 1,34 / 1,82 / 1,49 / 2,42.
- **5 cm gegen 10 cm (Bootstrap über die Testblöcke):** Vorteil von 5 cm +0,25 Plätze je Ausschnitt (A; 95-%-Intervall +0,06 bis +0,46) und +0,42 (B; +0,14 bis +0,66). Ein Lernlauf je Variante; der Zufall des Lernens ist darin nicht enthalten.
- **Delta Methode gegen amtlich (Strassenraum im Gebiet):** A_5cm −3 Plätze (−0,8 %), A_10cm −18 (−5,1 %), B_5cm −17 (−6,2 %), B_10cm −65 (−23,6 %). Die Teile (Fehler der Methode, nicht sichtbar, Ground Truth gegen amtlich) haben verschiedene Vorzeichen und heben sich zum Teil auf.
- **Nach der Auswertung ergänzt (nur Ausweis, nichts eingestellt):** IoU je Testblock, MAE nur in Ausschnitten mit Feldern, zusätzliche Grenzen in Notebook 10.

### Abbildungen dieses Durchgangs

- Figure 07_lernkurven.png: Fehlernote auf den Lernkacheln und IoU auf der Validierung je Epoche für alle vier Läufe; der Punkt ist der gespeicherte beste Stand.
- Figure 07_schwelle.png: IoU auf der Validierung je Schwelle; der Punkt ist die gewählte Schwelle.
- Figure 10_gezaehlt_gegen_wahr.png: gezählte gegen wahre Felder je Testausschnitt; unter der Diagonale wurde zu wenig gezählt.
- Figure 10_bootstrap.png: Verteilung des Vorteils von 5 cm aus 10'000 Ziehungen ganzer Testblöcke; die 0 liegt bei beiden Versuchen ausserhalb des 95-%-Intervalls.
- Figure 10_delta.png: Delta je Lauf, zerlegt in drei Teile.
- Figure 10_fehler.png: ein Testausschnitt in allen vier Läufen (richtig erkannt, Fehlmeldung, übersehen).

### Wiederholung (27.11.2026)

Nach dem Lernen wurde Notebook 05 ein zweites Mal ausgeführt, danach 09 und 10. Der Inhalt der Kacheln und Lösungsblätter (Stichprobe: jede siebte Datei), `kacheln_index.csv`, `zaehlung.csv` und alle Dateien `auswertung_*.csv` waren danach unverändert (Vergleich der Prüfsummen). Das Lernen (Notebook 07) und die Vorhersage (Notebook 08) wurden nicht wiederholt; ob ein zweiter Lernlauf dieselben Zahlen gibt, ist nicht geprüft.

### Nachträge nach der Durchsicht der Entscheide (27.11.2026)

Der Auftraggeber ist die Entscheide E1 bis E12 durchgegangen und hat vier Nacharbeiten freigegeben. Die Regeln dafür stehen in `01b`, Abschnitt 11.2, und wurden vor dem Rechnen geschrieben.

- **N1 Sonderfelder getrennt ausgewiesen (Notebooks 09 und 10):** `01b`, 8.5 D4 hatte das zugesagt; im ersten Lauf fehlte es. Sichtbare Felder der Testblöcke: Bild 2021 708, davon 44 mit ✕ und 7 mit ?; Bild 2024/25 500, davon 30 und 5. Trefferquote der Fläche auf Sonderfeldern gegen gewöhnliche Felder: A_5cm 0,52 gegen 0,76; A_10cm 0,40 gegen 0,72; B_5cm 0,47 gegen 0,71; B_10cm 0,23 gegen 0,62. Alle bisherigen Spalten von `zaehlung.csv` und `auswertung_*.csv` sind unverändert (Spalte für Spalte verglichen).
- **N2 Lauf A_10cm länger gelernt (Notebook 07, Abschnitt 11):** 60 statt 40 Epochen, von vorn, Seed 42. Beste Epoche 55 (erster Lauf: 40). IoU auf der Validierung mit gewählter Schwelle 0,532 (Schwelle 0,40) statt 0,530. In den Epochen 1 bis 40 unterscheiden sich die beiden Läufe in einzelnen Epochen um bis zu 0,018 IoU, obwohl nichts verändert wurde.
- **Zweite Auswertung (Schritt 14, nur A_10cm_lang, Notebook 11):** IoU 0,583 statt 0,582; gezählt 624 statt 626 von 708; MAE je Ausschnitt 1,17 statt 1,11. Vorteil von 5 cm +0,31 Plätze je Ausschnitt (95-%-Intervall +0,13 bis +0,48) statt +0,25 (+0,06 bis +0,46). Delta zu amtlich −14 Plätze (−4,0 %) statt −18 (−5,1 %). Schluss nach der vorab festgelegten Regel: die Aussage "5 cm zählt im Bild 2021 besser als 10 cm" ist bestätigt (das Intervall enthält die 0 auch mit dem länger gelernten Netz nicht). Die erste Auswertung bleibt das Ergebnis.
- **Kontrollen in Notebook 11 (der erste Lauf, neu gerechnet):** Kontrolle 1: 137 von 137 Masken sind Pixel für Pixel gleich | abweichende Pixel: 0 von 35913728. Kontrolle 2: in 137 von 137 Testausschnitten stimmen alle fünf Zahlen mit Notebook 09 überein. Kontrolle 3: Alle acht Zahlen des ersten Laufs stimmen mit Notebook 10 überein. Damit sind Vorhersage (08) und Zählung (09) für diesen Lauf einmal wiederholt. Das Lernen der vier Läufe ist nicht wiederholt.
- **N3 Stichprobe im Strassenraum (Notebook `stichprobe_strassenraum`):** 624 neu gesetzte Felder im Strassenraum; 192 ohne amtliches Objekt in 3 m, davon 65 Streifen; aus den übrigen 127 sind 30 gezogen (Seed 42). Je Bild ein Urteil; die Arten wurden vor dem ersten Urteil einmal verfeinert (01b, 11.2, N3). Urteile des Auftraggebers: 30 von 30 eingetragen (diktiert am 27.11.2026; unklare Lesarten danach bestätigt, dabei Nr. 3 und Nr. 30 geändert). Bild 2021: 3 gewöhnliche Parkfelder, 13 reservierte oder private Felder (12 davon gelb markiert), 10 gelbe Markierungen mit Kreuz (Parkverbot), 1 Sonderfeld (Polizei), 1 Velofeld, 2 kein Parkfeld; Bild 2024/25: 3 / 13 / 10 / 0 / 1 / 3. Die 30 Felder liegen in 19 Ausschnitten. Folgefrage zum Umgang mit gelben Markierungen: offen (01b, 11.2).
- **N4 vorgemerkt, nicht gerechnet:** Klassengewicht oder anderer Verlust gegen das Unterzählen; Schwelle nach dem Zählfehler statt nach der IoU. Beides braucht neue Testblöcke oder eine Kreuzvalidierung.
- **Textkorrekturen in 01b:** 10.2 (Vorschlag a wurde vereinfacht umgesetzt: keine Handprüfung einzeln stehender Felder), 10.3 (der Entscheid steht nicht mehr aus), 11.1 (die Begründung "Zeitrahmen" für das Nicht-Verlängern trägt nicht: der Lauf war nach rund 2 von 4 Stunden fertig).

- Figure 07_nachtrag_lernkurve.png: Fehlernote und IoU auf der Validierung für den ersten Lauf A_10cm (40 Epochen) und den längeren Lauf (60 Epochen); nach Epoche 40 steigt die Kurve nicht mehr.
- Figure 11_nachtrag.png: links die gezählten Plätze je Testausschnitt mit beiden 10-cm-Netzen; rechts die Bootstrap-Verteilung des Vorteils von 5 cm für beide Vergleiche, die 0 liegt beide Male ausserhalb des 95-%-Intervalls.
- Figure stichprobe_strassenraum_1.jpg: zehn der 30 Felder der Stichprobe in beiden Luftbildern (Blätter 2 und 3 ebenso), mit den amtlichen Objekten des jeweiligen Jahres.

### Schlussdurchsicht (27.11.2026)

Auftrag des Auftraggebers: den Leitfaden und den Bestand streng durchgehen (klar, chronologisch, Formeln dokumentiert, keine Annahmen aus früheren Durchgängen, keine überflüssigen Dateien). Er hat zugleich entschieden: Die festgelegte Methodik bleibt; gelbe Markierungen zählen in diesem Durchgang weiter mit (01b, 11.2).

- **Leitfaden (01b):** Zeitleiste und Lesehilfe im Kopf; 24 Kästen "Stand heute" unter Texten vom 26.11.2026, die nicht mehr gelten (unter anderem 7.1, 7.2, 7.3, 7.5, 7.6, 7.7, 7.9: Plan vor der eigenen Ground Truth); neuer Abschnitt 12 mit der gültigen Methode, allen Formeln und einer Tabelle der festen Werte (gesetzt, aus der Norm, aus den Quellen, gemessen).
- **Drei weitere Abweichungen gefunden und in 01b, 11.1 eingetragen:** Der Vergleich zweier Wege für die Parkart (8.4 V3) wurde nicht gemacht; die Zeile "davon Sonderfelder" der Zähltabelle (8.5 D9) fehlt für die amtlichen Daten; Notebook 00 prüfte die Abdeckung nur für das Bild 2024/25.
- **Notebook 00:** prüft jetzt auch das Bild vom Frühjahr 2021 (Abschnitt 6, Schritt 5); Kopf und Schluss nach dem Schema. Neu ausgeführt; danach Notebook 04 neu ausgeführt: `kaestchen.gpkg` und `strassenraum.gpkg` sind inhaltlich gleich geblieben (alle Spalten und Geometrien verglichen). Die Prüfsummen von GeoPackage-Dateien ändern sich bei jedem Schreiben, auch ohne Änderung des Inhalts.
- **formeln_pruefen:** Verweise auf die heutigen Notebooks; Prüfung 7 mit dem heutigen Code; neue Prüfungen 14 bis 18 (Schwelle, mittlere Tiefe, Platz-Äquivalente, Bootstrap über Blöcke, Zerlegung des Deltas). 38 Vergleiche: 37 stimmen, 1 dokumentierter Grenzfall (ein einzeln gemeldetes Querfeld bekommt die Klasse weit).
- **Einstellungen:** 15 Schlüssel aus früheren Durchgängen aus `einstellungen.json` entfernt (Testzonen, Filter, Platzmasse aus Sekundärquellen und weitere); kein Notebook hat sie mehr gelesen. Zwei davon las `ground_truth_erfassen` noch (Seitenlänge, Arten des Strassenraums); sie stehen jetzt mit denselben Werten im Notebook selbst. Dieses Notebook wurde dafür **nicht** neu ausgeführt, weil es das Erfassungswerkzeug startet.
- **Begleitdateien:** `netz.py` ohne die unbenutzte Funktion aus Pilot 1; `.gitignore`, `UMGEBUNG.md` und `DATEN_LIZENZEN.md` auf den Stand dieses Durchgangs gebracht (kein Dashboard, keine Fahrzeugerkennung, beide Luftbilder).
- **Aufgeräumt nach Entscheid des Auftraggebers (27.11.2026).** Aus dem aktuellen Stand des Repositorys genommen: `archiv/pilot1/` (27 Dateien; alle Byte für Byte gleich wie im Git-Stand `v0.1.0`) und die Dokumente 1, 2 und 4 zu Pilot 1 (weiter im Git-Verlauf). Lokal gelöscht: die Kacheln des ersten Durchgangs (2,4 GB), drei Zwischendateien, eine Arbeitsnotiz und 241 von 246 automatischen Sicherungen der Ground Truth. Behalten: der lokale Ordner mit dem zweiten Durchgang (einzige Kopie, nicht im Repository), die Netze von Pilot 1, die letzten fünf Sicherungen. Die fertige Ground Truth war davon nicht berührt (Prüfsumme vorher und nachher gleich).

### Karte des ganzen Gebiets und Dashboard (27.11.2026)

Auftrag des Auftraggebers: ein Dashboard, das zeigt, welche Parkplätze die Methode findet, mit Herunterladen als GeoPackage. Die Regeln stehen in 01b, Abschnitt 11.3 (K1 bis K10) und wurden vor dem Rechnen geschrieben; K10 kam nach dem ersten Lauf von Notebook 12 dazu.

- **Keine Prüfung.** Die vier Netze und Schwellen aus Notebook 07 wurden unverändert auf alle 691 Ausschnitte angewendet, also auch auf Lern- und Validierblöcke. Die Kennzahlen des Pilots bleiben die der Testblöcke (Schritt 14).
- **Kontrollen in Notebook 12:** In den 137 Testausschnitten sind für alle vier Läufe die Masken gleich wie in Notebook 08, die Kategorie je Pixel gleich wie in Notebook 05 und die gezählte Zahl gleich wie in Notebook 09 (548 von 548 Zeilen).
- **Gezählte Plätze im ganzen Gebiet:** A_5cm: gezählt 2700 (Lernen 1694 von 1655 sichtbaren Feldern, Validieren 342 von 345, Testen 664 von 708); A_10cm: gezählt 2693 (Lernen 1739 von 1655 sichtbaren Feldern, Validieren 328 von 345, Testen 626 von 708); B_5cm: gezählt 1866 (Lernen 1175 von 1091 sichtbaren Feldern, Validieren 237 von 242, Testen 454 von 500); B_10cm: gezählt 1616 (Lernen 1018 von 1091 sichtbaren Feldern, Validieren 203 von 242, Testen 395 von 500).
- **Lernblöcke gegen Testblöcke:** In den Lernblöcken zählt die Methode 93 bis 108 % der sichtbaren Felder, in den Testblöcken 79 bis 94 %. Das zeigt, warum die Karte keine Prüfung ist.
- **K10, nachgetragen:** Der erste Lauf ergab 265'651 gemeldete Flächen, rund 99 % davon einzelne Pixel. Einzeln gespeichert werden Flächen ab einem halben Platz-Äquivalent oder mit zugeteiltem Platz (733 bis 926 je Lauf). Die kleineren enthalten 2 bis 6 % der Platz-Äquivalente; sie zählen mit und stehen je Ausschnitt als Summe in der Datei.
- **Dateien:** vier GeoPackages (7 bis 16 MB, vier Ebenen, LV95) und `dashboard.html` (7,5 MB). Für die Anzeige im Dashboard sind die Umrisse vereinfacht (Löcher unter 0,25 m² geschlossen, höchstens 15 cm geglättet); die GeoPackages enthalten die genauen Umrisse.
- **Dashboard geprüft:** in einem Browser ohne Fenster geöffnet und vier Ansichten als Bildschirmfoto angesehen (Übersicht, Sommerbild bei 10 cm mit allen Ebenen, Nahansicht mit Flächen, Info-Teil). Nicht geprüft: Klicks auf einzelne Punkte, die Suche und das Herunterladen von Hand.

- Figure 12_punkte.png: eine gemeldete Fläche, ihr kleinstes umschliessendes Rechteck und die gleichmässig darauf verteilten Punkte.
- Figure 12_karte.png: gezählte Plätze des Laufs A_5cm im ganzen Gebiet, nach Abgleich mit der Ground Truth; dahinter die Blöcke nach ihrer Rolle.
- Figure 13_vorschau.png: ein Testblock mit Luftbild, gezählten Flächen (hell), Punkten und Ringen der Ground Truth, in den Farben und Zeichen des Dashboards.

### Dashboard mit Legende, Version 0.2.0-alpha, Durchsicht des Bestands (27.11.2026)

Auftrag des Auftraggebers: Dem Dashboard fehlt eine Legende, und es soll für Leute verständlich sein, die das Projekt nicht kennen und mit den Geodaten arbeiten. Dazu: den Stand benennen, Methodik, Zielsetzung und Dokumente durchgehen und schlank halten, das Repository prüfen. Gerechnet wurde nichts Neues; keine Regel der Methodik und keine Kennzahl hat sich geändert.

- **Dashboard (Notebook 13, `dashboard_vorlage.html`):** Legende, die nur zeigt, was eingeschaltet ist; Alltagswörter («Programm», «von Hand markiertes Parkfeld», «Prüfgebiet», «Lerngebiet», «Einstellgebiet»), die Namen in den Daten bleiben; neuer Teil «Daten nutzen» mit den vier Ebenen des GeoPackage und ihren Merkmalen. Regel K2 gilt weiter: keine Kennzahlen im Dashboard. Ein erster Entwurf hatte vier Zahlen der Testblöcke im Hinweis; er wurde vor dem Bauen verworfen, weil er K2 widersprach.
- **Farben und Zeichen:** Die drei Farben des Abgleichs (`#00b894`, `#f2a600`, `#c86bfa`) bestehen alle Prüfungen des Prüfskripts für Farbpaletten (Helligkeit, Buntheit, Unterscheidbarkeit bei Rot-Grün- und Blau-Gelb-Schwäche: kleinster Abstand 11,8). Die vorherigen Farben bestanden nicht: Das Orange war zu hell, und Grau («nicht bewertet») war von Grün bei Rot-Grün-Schwäche kaum zu unterscheiden (Abstand 3,1). «Nicht bewertet» ist jetzt weiss gestrichelt. Gemeldete Flächen sind hell statt grün, weil Grün bei den Punkten «bestätigt» heisst.
- **Dashboard geprüft (Browser ohne Fenster, Edge):** elf Ansichten als Bildschirmfoto angesehen (Übersicht, Nahansichten in beiden Bildern mit allen Ebenen, Strassenkarte, leere Karte, drei Teile der Erklärung, kleiner Laptop, schmaler Bildschirm mit und ohne Legende). Per Skript ausgelöst und gelesen: das Fenster beim Klick auf acht Arten von Zeichen, die Legende in drei Zuständen, das Umschalten von Bild und Auflösung, das Herunterladen als GeoJSON (2'094 von 2'094 erwarteten Objekten) und die Suche (eigene Treffer und Suchdienst des Bundes). Kein Fehler der Seite. Nicht geprüft: Bedienung von Hand mit Maus und Tastatur, andere Browser, ein Mobiltelefon.
- **Bezeichnung:** Dieser Stand heisst Version 0.2.0-alpha (`CITATION.cff`, README, Dashboard, 01b Abschnitt 11.3). Der Stand mit den amtlichen Daten als Lösung («Pilot 1») bleibt 0.1.0.
- **README:** neu gegliedert in «Was die Arbeit will», «Was die Arbeit macht», «Was herauskommt». Die drei Fragen aus 01b, Abschnitt 3 stehen jetzt am Anfang und werden einzeln beantwortet. Die Frage «Frühjahr gegen Sommer» war bisher nicht ausdrücklich beantwortet; die Antwort nennt nur Zahlen, die schon in der Tabelle stehen, und sagt, dass dafür kein Intervall gerechnet wurde.
- **Lücke beim Nachrechnen gefunden und geschlossen:** `rohdaten_herunterladen` lud drei Dateien nicht, die die Notebooks 01, 04, 09 und 13 lesen (Strassenparkplätze 2021, Liegenschaften der amtlichen Vermessung, Liegenschafteninventar); sie lagen lokal noch vom ersten Durchgang. Das Notebook ist nach dem Schema neu gebaut und lädt sie jetzt. Kontrolle am Schluss: 56 von 56 Dateien vorhanden und im Manifest. Die drei Adressen wurden beim Dienst der Stadt abgefragt: Die Zahl der Objekte stimmt mit den lokalen Dateien überein (46'282, 5'860, 5'509). Der Ladeweg selbst lief nicht, weil keine Datei fehlte.
- **Schlanker Bestand:** `3_Quellen_und_Daten.md` (Recherche zum ersten Durchgang, zum Teil überholt) ist aus dem aktuellen Stand genommen; Literatur, Normen und Lizenzen stehen in `DATEN_LIZENZEN.md`, Abschnitt 5. Die überholte Durchsicht vom 26.11.2026 ist aus dieser Datei genommen. Beides bleibt im Git-Verlauf.
- **Weitere Korrekturen:** `DATEN_LIZENZEN.md` nennt jetzt auch das Luftbild Sommer 2026 und die Liegenschaften (beide von Notebook 01 verwendet); Notebook 13 liest `aufteilung.csv` nicht, die Angabe im Kopf ist entfernt; Notebook 13 ohne `lambda`, mit einer Funktion je Zelle und einer neuen Kontrolle (jede der 22 Spalten der GeoPackages ist im Dashboard erklärt; dabei fielen zwei fehlende auf und wurden ergänzt); in Notebook 01 hat die Abbildung der späten Daten eine Erklärung, und vier Stilpunkte des Prüfskripts sind behoben (eine Funktion je Zelle, kein `lambda`).
- **Stand online geprüft (über Git; die Seite selbst war nicht einsehbar, weil das Repository privat ist):** kein Personenbezug in den Dateien, Urheber der Commits mit GitHub-Adresse ohne Klarnamen, keine Datei über 50 MB, kein Notebook mit Fehlerausgabe. Notebook 01 war 39 MB gross (13 Abbildungen als PNG eingebettet); so grosse Notebooks zeigt GitHub in der Regel nicht an. Die Bilder werden jetzt im Notebook als JPEG eingebettet: 5,9 MB. Verglichen mit vorher: Alle Text- und Tabellenausgaben sind gleich (dazu eine neue Zeile zur Grösse eines Ausschnitts), es sind weiter 13 Abbildungen, und die 13 gespeicherten PNG-Dateien sind Byte für Byte unverändert. Ein erster Versuch bettete gar keine Bilder ein (falsche Angabe der Bildqualität); der Vergleich hat das gezeigt, bevor es weiterging. Ob GitHub das Notebook nun anzeigt, ist nicht geprüft.
- **Formeln:** `formeln_pruefen` auf einer Kopie neu ausgeführt: 38 Vergleiche, 37 stimmen, 1 dokumentierter Grenzfall, 0 Abweichungen; die Ausgaben sind gleich wie im Repository.
- **Offen nach dieser Runde:** Stilpunkte des Prüfskripts in den Notebooks 05, 07 und 12, in `ground_truth_erfassen` und in `formeln_pruefen`. Die ersten drei sind im nächsten Abschnitt behoben.

### Umbau der Notebooks 05, 07 und 12 (27.11.2026)

Auftrag des Auftraggebers: die drei Notebooks umbauen, in denen das Prüfskript noch Stilpunkte meldete (Zellen mit mehr als 25 Zeilen, mehrere Funktionen in einer Zelle). Geändert wurde nur die Form. Wo ein Teil einer Schleife in eine Funktion wanderte, sind die bestehenden Zeilen wörtlich übernommen.

- **Notebook 05:** Das Speichern der Kacheln eines Ausschnitts ist eine eigene Funktion (`speichere_kacheln`). Neu ausgeführt.
- **Notebook 07:** Was nach jeder Epoche geschieht (lernen, Lernrate verkleinern, auf der Validierung messen), ist eine eigene Funktion (`epoche_mit_messung`); `trainiere` ruft sie auf. Ohne Lernen neu ausgeführt. Die Lernfunktion selbst läuft dabei nicht; sie wurde darum getrennt geprüft: ein Probelauf von einer Epoche (Lauf B bei 10 cm, eigener Name, eigenes Protokoll, gemessen nur auf der Validierung). Fehlernote 0,08633 gegen 0,08635 in der ersten Epoche des echten Laufs, IoU 0,00018 gegen 0,00014. Bitgleich ist das nicht; kleine Unterschiede der Grafikkarte waren schon bei der Gegenprobe zu sehen. Die Probedateien sind gelöscht.
- **Notebook 12:** Pfade und Pakete in zwei Zellen, je eine Zelle für `lies_bild` und `halbiere`, zwei neue Funktionen für das Setzen der Punkte und für die Übersicht je Rolle. Mit den gespeicherten Masken neu ausgeführt; die drei Kontrollen gegen die Notebooks 08, 05 und 09 stimmen weiter. Die zwei Abbildungen tragen jetzt das Grün des Dashboards (`#00b894`).
- **Vorher und nachher verglichen (178 Einträge, alle gleich):** der Inhalt jeder siebten Kachel und jedes siebten Lösungsblatts (von 5'157 und 2'764 Dateien, dazu Zahl und Namen aller Dateien), alle Ergebnisdateien (`*.csv`, `*.json`), `kacheln_index.csv`, `platzmasse.json` und der Inhalt aller vier Ebenen der vier GeoPackages. Die Text- und Tabellenausgaben der drei Notebooks sind gleich wie vorher, dazu vier neue Zeilen (eine Meldung je abgetrennter Zelle). Die Abbildungen der Notebooks 05 und 07 sind Byte für Byte unverändert.
- **GeoPackages:** Notebook 12 schreibt sie bei jedem Lauf neu; dabei ändern sich nur Zeitstempel in der Datei. Weil der Inhalt gleich ist, bleiben im Repository die bisherigen Dateien stehen.
- **Unterwegs korrigiert:** Nach dem ersten Umbau zeigte eine Zelle von Notebook 07 den Rückgabewert von MLflow mit einem Pfad des Rechners an. Das Prüfskript hat es gemeldet; die Zelle endet jetzt mit einer eigenen Meldung. In Notebook 05 zeigt eine Zelle die Zeichenzahl von `einstellungen.json` an; sie ist kleiner als vorher (705 statt 1'748), weil die Einstellungen am 27.11.2026 aufgeräumt wurden.
- **Prüfskript danach:** kein Befund in den Notebooks 00 bis 13 ausser einem in Notebook 07: Die Klasse `Kacheln` hat drei Methoden in einer Zelle. Eine Klasse lässt sich nicht auf mehrere Zellen verteilen; der Befund bleibt stehen. Offen blieben `ground_truth_erfassen` und `formeln_pruefen`; sie sind im nächsten Abschnitt umgebaut.
- **Prüfregel angepasst (Entscheid des Auftraggebers, 27.11.2026):** Das Prüfskript zählt die Methoden einer Klasse nicht mehr einzeln; eine Klasse zählt als eine Einheit, wie eine Funktion. Zuerst wurden neun Testfälle geschrieben; das bisherige Skript scheiterte an den zwei Fällen mit einer Klasse, das neue besteht alle neun. Über alle Notebooks ändert sich genau zweierlei: Der Befund in Notebook 07 (Klasse `Kacheln`) entfällt, und in `ground_truth_erfassen` entfällt einer von vier (die Klasse des Werkzeugs; die Zelle bleibt wegen ihrer Länge gemeldet). Damit haben die Notebooks 00 bis 13 keinen Befund mehr. Das Prüfskript gehört zum lokalen Skill und liegt nicht im Repository.
- **Lokal aufgeräumt (Entscheid des Auftraggebers vom 27.11.2026, nichts davon lag im Repository):** `archiv/pilot1_methodik_neu_aufgebaut`, `archiv/pilot1`, `archiv/dokumente_2026-11-25`, die zwei Netze des ersten Durchgangs und die Notiz `PILOT2_ANFORDERUNGEN.md` sind gelöscht. Geblieben sind der EAGLE-Datensatz und acht kleine Rohdateien des ersten Durchgangs, die kein Notebook mehr liest.

### Umbau von ground_truth_erfassen und formeln_pruefen (27.11.2026)

Auftrag des Auftraggebers: auch die zwei letzten Notebooks mit Stilpunkten umbauen. Danach meldet das Prüfskript in keinem der 20 Notebooks mehr einen Befund.

- **formeln_pruefen:** Prüfung 1 zeigt die vier Schritte jetzt einzeln (Beispiel, unser Code, Bibliothek, Vergleich), je in einer Zelle mit «Vorher → nachher»; die Prüfungen 2 bis 18 gehen gleich vor und bleiben je in einer Zelle. Die Zufallszahlen werden in derselben Reihenfolge gezogen. Neu ausgeführt: dieselbe Tabelle am Schluss (38 Vergleiche: 37 stimmen, 1 dokumentierter Grenzfall, 0 Abweichungen), alle bisherigen Ausgabezeilen gleich, dazu drei neue.
- **ground_truth_erfassen, Text:** Die Schritte tragen Nummern statt Buchstaben. In Abschnitt 3 stehen die zwei Funktionen und die Rechnung je in einer eigenen Zelle.
- **ground_truth_erfassen, Server des Werkzeugs:** Die eine Zelle mit 61 Zeilen ist in fünf Schritte geteilt: was der Browser abholen darf (`antwort_auf_abruf`), ob ein Stand gültig ist (`stand_ist_gueltig`), speichern (`speichere_stand`), die Klasse des Servers, starten. Die Klasse ruft die drei Funktionen auf.
- **Vor dem Einbau geprüft:** alte und neue Fassung des Servers je in einem Wegwerf-Ordner mit einer Kopie der Ground Truth gestartet und mit denselben 35 Anfragen verglichen: Seite, Stand, Bildausschnitt, fehlendes Bild, fremder Pfad, vier ungültige Stände (kein JSON, zu wenige Ausschnitte, Felder keine Liste, Felder fehlen), Speichern am falschen Pfad und 22 gültige Speicherungen. Status, Art des Inhalts, Länge und Inhalt jeder Antwort sind gleich; nach den abgelehnten Ständen ist die Datei unverändert; am Schluss enthalten beide Ordner dieselbe Datei, zwei Sicherungen und keine Zwischendatei.
- **Ausführen ohne Risiko für die Ground Truth:** Das Notebook startet beim Ausführen den Server. `ground_truth_hand.json` war während des Laufs schreibgeschützt. Ihr Fingerabdruck (SHA-256) ist vor dem Umbau, vor dem Lauf und nach dem Lauf derselbe; der Ordner mit den Sicherungen ist unverändert.
- **Ausgaben:** Alle 63 bisherigen Ausgabezeilen von `ground_truth_erfassen` sind gleich, dazu fünf neue (je eine Meldung der neuen Zellen). Die Abbildung `gt_ausschnitte.png` ist unverändert.
- **gt_vorschlag.json:** Das Notebook schreibt die Datei neu. Geändert hatte sich darin nur der Zeitstempel `erstellt`; Einstellungen, Ausschnitte und Felder sind gleich. Im Repository bleibt darum die bisherige Datei stehen.
- **Nicht geprüft:** das Werkzeug im Browser von Hand mit der neuen Fassung des Servers.

### Unbenutzte Rohdaten gelöscht (27.11.2026)

Auftrag des Auftraggebers: den EAGLE-Datensatz und die kleinen unbenutzten Rohdaten löschen. Vorher geprüft: Keine der Dateien wird in einem Notebook oder Skript genannt, keine liegt im Repository.

- **Gelöscht (lokal):** `EAGLE_Dataset_public.zip` (3,2 GB, Fahrzeugdatensatz des ersten Durchgangs) samt Protokolldatei; drei DAV-Ebenen (Güterumschlag, Parkuhren, Punkte zu Streifen), die Behindertenparkplätze, drei Zuschnitte der Vermessung mit `_kreis1` (Bodenbedeckung, Strassenstücke, Baurechte) und ein Protokoll des Herunterladens.
- **Manifest:** Die acht Zeilen zu diesen Dateien sind aus `daten/roh/MANIFEST.csv` genommen (80 → 72 Zeilen). Notebook 01 prüft jede Zeile und hätte sie sonst als fehlend gemeldet. Die Zeilen bleiben im Git-Verlauf.
- **Nachgeführt:** Notebook 01 neu ausgeführt (61 von 61 Rohdateien vorhanden; alle übrigen Ausgaben und die 13 gespeicherten Abbildungen gleich wie vorher); `rohdaten_herunterladen` neu ausgeführt (56 von 56 Dateien vorhanden, nichts nachgeladen); ein Satz in `DATEN_LIZENZEN.md`; in der README die Grösse der Daten (Rohdaten rund 33 GB, Zwischendaten rund 6 GB).
- **Unterwegs korrigiert:** Der Satz zur Grösse stand nach der ersten Änderung doppelt in der README; der Vergleich der Änderungen hat es gezeigt.
- **Beobachtet und danach behoben (Entscheid des Auftraggebers, 27.11.2026):** Das Manifest im Repository führt die Dateien dieses Rechners. Wer das Repository frisch klonte und die Rohdaten lud, bekam für jede Datei eine zweite Zeile dazu; hatte der Anbieter eine Datei seither nachgeführt, hätte Notebook 01 für die alte Zeile eine falsche Grösse gemeldet. Die Funktion `hole` in `rohdaten_herunterladen` ersetzt jetzt eine bestehende Zeile zur selben Datei. Geprüft mit sechs Testfällen in einem Wegwerf-Ordner und einem nachgestellten Server (Zeile schon vorhanden, kein Manifest, Datei schon da, neue Datei, Webseite statt Daten): Die bisherige Funktion scheiterte am ersten Fall, die neue besteht alle sechs. Das Notebook wurde neu ausgeführt; seine Ausgaben und das Manifest sind unverändert. Ein echter Download lief dabei nicht, weil keine Datei fehlte.

### Letzte Durchsicht vor dem Veröffentlichen (27.11.2026)

Auftrag des Auftraggebers: die Methodik noch einmal prüfen und ob sie im Repository sinngemäss beschrieben ist; danach veröffentlicht er das Repository.

- **Leitfaden gegen Code:** `01b`, Abschnitte 12.1 bis 12.12, Zeile für Zeile mit dem Code der Notebooks 02 bis 10 verglichen (Aufteilung, Platzmasse, Kästchen und Kategorien, Lösungsblatt, einfache Schätzungen, Lernen und Schwelle, Vorhersage, Zählung, Auswertung, Zerlegung des Deltas). Die Beschreibung stimmt mit dem Code überein. Drei Angaben standen im Code, aber nicht im Text, und sind ergänzt: der Kreis von 3 m um einzeln stehende Felder (12.3, 12.12), der Vorrang beim Überlappen im Lösungsblatt (12.4) und dass Meldungen an unsicheren Stellen und bei einzeln stehenden Feldern in der Auswertung nicht ausgewiesen werden (12.8).
- **Regeln der Karte gegen Code:** `01b`, 11.3 (K1 bis K10), und die Texte des Dashboards mit Notebook 12 verglichen (erkannt ab der Hälfte des Kästchens, bestätigt bis 1 m, Verteilung der Punkte, Flächen unter einem halben Platz-Äquivalent). Sie stimmen überein.
- **README, Übersicht der Notebooks, Lizenzdatei:** jede Aussage zur Methode mit dem Code oder den Ergebnisdateien verglichen. Eine Angabe war ungenau: Die 3'269 von Hand gesetzten Felder sind nicht alle gewöhnliche Parkfelder. README und Dashboard nennen jetzt, was dazugehört (2'669 Einzelfelder, 361 Sonderfelder mit `✕`, 30 mit `?`, 209 Abschnitte von Parkstreifen). Die README sagt zudem, dass «Auftraggeber» in den Notebooks der Autor des Projekts ist.
- **Nachrechnen:** Notebook 04 las für seine Abbildung Bildausschnitte, die nur `ground_truth_erfassen` herstellt, ein Notebook ausserhalb der Reihe. Nach einem frischen Klonen wäre die Reihe 00 bis 13 dort abgebrochen. Die Abbildung liest jetzt das Luftbild direkt. Neu ausgeführt: `kaestchen.gpkg` und `strassenraum.gpkg` sind inhaltlich gleich wie vorher, alle Ausgaben gleich, dazu eine neue Zeile. Die frühere Prüfung der Abhängigkeiten hatte Bilddateien nicht erfasst.
- **Geschichte des Repositorys** (wird mit veröffentlicht; 11 Commits, zwei Tags): alle Stände aller Textdateien nach Namen, Adressen, Pfaden des Rechners und Zugangsdaten durchsucht: keine Treffer. Urheber aller Commits ist das GitHub-Konto mit seiner Adresse ohne Klarnamen. In der Geschichte liegen keine PDFs, keine Netze und keine Rohdaten. Die zwei Notebooks des ersten Durchgangs zum Datensatz EAGLE enthalten keine Bilder daraus, nur Code, Zahlen und den Lizenztext.
- **Nicht geprüft:** die Seite auf GitHub selbst (das Repository war bis hierher privat), ein vollständiges Nachrechnen auf einem zweiten Rechner, die Bedienung von Dashboard und Erfassungswerkzeug von Hand.

### Veröffentlichung ohne Geschichte (27.11.2026)

Entscheid des Auftraggebers: Aus Sicherheitsgründen soll Pilot 1 nur als Text bestehen, ohne Quellcode.

- **Ausgangslage:** Der Quellcode von Pilot 1 lag nicht mehr im aktuellen Stand, aber in den früheren Commits und unter dem Tag `v0.1.0`. Ein Repository wird mit seiner ganzen Geschichte öffentlich; Dateien oder einen Tag zu löschen hätte den Code darum nicht entfernt.
- **Vorgehen:** Veröffentlicht wird ein neues Repository mit einem einzigen Commit, dem heutigen Stand. Das bisherige Repository bleibt privat; es ist das Arbeitsarchiv des Autors mit der ganzen Geschichte. Gelöscht wurde dabei nichts.
- **Folge für den Eintrag darüber:** Dort steht, die Geschichte werde mit veröffentlicht. Das gilt nicht mehr. Öffentlich ist nur der heutige Stand; die dort beschriebene Suche in allen früheren Ständen bleibt richtig, betrifft aber das private Archiv.
- **Pilot 1 als Text:** `PILOT1.md` beschreibt, was im ersten Durchgang gemacht wurde, was herauskam und warum die Methode geändert wurde. Die Zahlen stammen aus den Ergebnisdateien und der Zusammenfassung des Stands 0.1.0, die Gründe aus `01b` (Abschnitte 1, 4.8, 7.2) und Notebook 01.
- **Verweise:** README, `DATEN_LIZENZEN.md`, `notebooks/README.md` und `01b` verwiesen für Pilot 1 auf den Git-Stand `v0.1.0`; sie verweisen jetzt auf `PILOT1.md`. Dieses Protokoll bleibt, wie es geschrieben wurde; die Lesehilfe am Anfang erklärt, was mit "Git-Verlauf" gemeint ist.
- **Geprüft:** Der veröffentlichte Commit enthält genau die Dateien des letzten Arbeitsstands (derselbe Dateibaum). Von seinem Tag `v0.2.0-alpha` aus ist kein früherer Commit erreichbar.

