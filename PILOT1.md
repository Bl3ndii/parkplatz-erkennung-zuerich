# Pilot 1 in Worten (Version 0.1.0, 26.11.2026)

Dieser Text beschreibt den ersten Durchgang des Projekts: was gemacht wurde, was herauskam und warum die Methode danach geändert wurde. Der Quellcode von Pilot 1 ist nicht Teil dieses Repositorys. Die Methode ist überholt; was heute gilt, steht in der [README](README.md) und im Leitfaden `notebooks/01b_methodik_leitfaden.ipynb`, Abschnitt 12.

Der Text steht hier aus zwei Gründen. Der Leitfaden verweist an einigen Stellen auf «Vorwissen aus Pilot 1»; man soll nachlesen können, woher es stammt. Und die Änderung der Methode soll nachvollziehbar bleiben.

## Die Frage

Wie gut lassen sich Parkflächen im Strassenraum der Stadt Zürich (Kreis 1) aus Luftbildern erkennen, und was bringt eine Auflösung von 5 cm gegenüber 10 cm?

## Was gemacht wurde

1. **Daten.** Das Luftbild vom Sommer 2024/25 mit 5 cm je Bildpunkt (das 10-cm-Bild daraus gerechnet), die amtlichen Parkfelder der Dienstabteilung Verkehr (DAV, Stand 2025) und die Amtliche Vermessung.
2. **Testzonen.** Vier zufällig gezogene Quadrate von 200 × 200 m in Kreis 1 (Seed 42). Darin lagen 326 amtliche Parkplätze in 39 Strassenabschnitten. Gelernt wurde nur ausserhalb dieser Zonen.
3. **Platzmasse.** Aus den Abständen der amtlichen Punkte gemessen.
4. **Lösung aus amtlichen Daten.** Eine eigene Erfassung von Hand gab es nicht. Aus jedem amtlichen Punkt wurde ein Rechteck gezeichnet: Lage und Parkart aus den Daten, Grösse aus den Platzmassen. Diese Rechtecke waren die Lösung, an der das Netz lernte. Dieselbe amtliche Quelle galt in den Testzonen als Wahrheit.
5. **Netz.** Ein neuronales Netz (Dense-U-Net) je Auflösung lernte, welche Bildpunkte Parkfläche sind.
6. **Zählung je Strassenabschnitt**, auf zwei Arten. *Z0* teilte die erkannte Fläche durch die Fläche eines Standardplatzes. *Z1-B* nahm die Platzgrösse nach der amtlichen Parkart (längs, quer, schräg).
7. **Auswertung.** Fläche (IoU, Genauigkeit, Trefferquote), Anzahl (mittlerer Fehler je Strassenabschnitt, Bias) und der Vergleich 5 cm gegen 10 cm mit einem Bootstrap. Dazu kamen eine Hochrechnung auf Kreis 1 und ein erstes Dashboard.
8. **Fahrzeugerkennung.** Ein zweites Modell, das parkierte Autos erkennen und daraus die Parkart ableiten sollte, war vorbereitet, wurde aber nicht gelernt. Der Grund: Selbst mit der amtlichen, also fehlerfreien Parkart sank der Fehler kaum (siehe Tabelle); es fehlte vor allem erkannte Fläche. Der dafür vorgesehene Fahrzeugdatensatz wurde für keine Zahl verwendet.

## Was herauskam

Grundlage: die vier Testzonen. Als Wahrheit galten die amtlichen DAV-Daten 2025.

| | 5 cm | 10 cm |
| --- | --- | --- |
| IoU Parkfläche | 0,35 | 0,19 |
| Genauigkeit / Trefferquote | 0,66 / 0,43 | 0,69 / 0,21 |
| Fehler je Strassenabschnitt (MAE), Zählung Z0 | 4,5 Plätze | 6,9 Plätze |
| Fehler je Strassenabschnitt (MAE), Zählung Z1-B | 4,4 Plätze | 6,9 Plätze |
| gezählt (Z0) gegenüber amtlich | 205 von 326 (−37 %) | 86 von 326 (−74 %) |

- **5 cm gegen 10 cm:** Der mittlere Fehler war bei 10 cm um 2,1 Plätze grösser als bei 5 cm (95-%-Intervall 0,8 bis 4,0).
- **Beide Auflösungen zählten deutlich zu wenig.** Die damalige Zusammenfassung hielt fest: Das Netz erkannte vor allem parkierte Autos; leere, unmarkierte und von Bäumen verdeckte Felder übersah es oft.
- **Vergleich mit der Literatur:** Die Arbeiten des DLR erreichen in Braunschweig eine IoU von etwa 0,68 bis 0,70.

Diese Zahlen lassen sich **nicht** mit denen des heutigen Stands vergleichen: Die Lösung ist eine andere (amtliche Daten statt eigener Erfassung), die Einheit ist eine andere (Strassenabschnitt statt Ausschnitt von 51,2 m), und geprüft wurde in anderen Gebieten.

## Warum die Methode geändert wurde

- **Dieselbe Quelle zum Lernen und zum Prüfen.** Gemessen wurde, wie gut das Netz die amtlichen Daten trifft, nicht, wie gut es trifft, was im Bild zu sehen ist. Bei einem Unterschied ist keine der beiden Seiten sicher die Wahrheit: Das Netz kann sich irren, die amtlichen Daten können veraltet oder lückenhaft sein (Leitfaden `01b`, Abschnitt 1).
- **Punkte statt Flächen.** Die amtlichen Daten geben Punkte. Die Rechtecke darum waren angenommen, und die Punkte liegen zum Teil um etwa einen Meter neben dem Feld (`01b`, Abschnitt 4.8). Bei einem Meter Versatz und einem 2,5 m breiten Feld ist der grösste Teil des Feldes falsch beschriftet (`01b`, Abschnitt 7.2; nachgerechnet in `formeln_pruefen`, Prüfung 9).
- **Zeitlicher Abstand.** Bei 461 von 1'252 amtlichen Feldern in Kreis 1 liegt das Datum der Inbetriebnahme nach dem letzten Flugtag des Luftbilds. Was dieses Datum bedeutet, ist nicht dokumentiert (Notebook 01, Abschnitt 13).
- **Nur ein Luftbild**, aufgenommen im Sommer mit Laub.

Seit Version 0.2.0-alpha gilt darum: Die Lösung zum Lernen und Prüfen ist eine eigene, von Hand auf zwei Luftbildern gesetzte Ground Truth. Die amtlichen Daten dienen nur noch für den Vergleich am Schluss (das Delta).

## Was aus Pilot 1 weiterverwendet wird

- **Das Vorgehen aus der Literatur** und das Netz (Dense-U-Net) mit seinen Einstellungen.
- **Vorwissen, als solches gekennzeichnet.** Im Leitfaden tragen Zahlen aus Pilot 1 den Vermerk «Vorwissen aus Pilot 1». Sie waren Anlass für eine Frage oder eine Einstellung, nie ein Ergebnis des heutigen Stands. Zwei Beispiele: Die beste Epoche lag bei 5 cm bei 14, bei 10 cm bei 43 von 60; das floss zusammen mit dem Zeitrahmen in die Wahl von 16 und 40 Epochen ein. Und die Felder quer zur Strasse standen im Mittel 2,33 m auseinander statt der 2,50 m der Norm; daraus kam die Frage, ob die Normbreite zu Zürich passt.
