README
================
2025-04-21

# Correlaid Projekt Klima-Kollektiv

Code repository für die Erstellung einer “scrollytelling” Karte zur
Visualisierung der Konsequenzen der Renaturierung der Braunkohle-Gruben
im rheinischen Revier.

Die Karte gibt es live hier:

\[…\]

# Setup & workflow

### Daten

Die Rohdaten liegen in diesem [Google Drive
Ordner](https://drive.google.com/drive/u/0/folders/1NIZPTE6bbTeMzjccTsxFNPS_JI491H-i).
Dort liegen auch andere projektrelevante Daten, wie etwa meeting minutes
und Präsentationen.

Die Daten wurden von verschiedenen (Roh-)Datenquellen zusammengeführt:

- Kartenbilder (pdf/png) wurden mithilfe der Digitalisierungstools in
  QGIS digitalisiert und als Geopackage (`.gpkg`) gespeichert. Die
  Tutorials zur Digitalisierung sind im
  [Wiki](https://github.com/CorrelAid/klima-kollektiv/wiki/Tutorials)
  velinkt.
- Von Projektmitgliedern in Google Maps erstellte Daten wurden direkt
  als `.kml` heruntergeladen und weiterverarbitet.

Diese aufbereiteten Daten werden dann im Ordner `data` gespeichert,
sodass der Code in diesem repo mit relativen Pfaden arbeitet. Um die
Größe dieses repos nicht ausufern zulassen, werden diese Daten
allerdings in der Versionskontrolle ignoriert (über die
[`.gitignore`](https://github.com/CorrelAid/klima-kollektiv/blob/main/data/.gitignore)
Datei im Ordner).

Eine Kopie der aufbereiteten Daten liegt ebenfalls im Google Drive
Ordner. Diese müssen dann lokal in den `data` Ordner kopiert werden um
die Karte zu generieren. Die Struktur der Daten im Ordner sieht wie
folgt aus:

``` r
library(fs)

dir_tree("data")
```

    ## data
    ## ├── Daten_Pipelines.csv
    ## ├── Daten_Pipelines.ods
    ## ├── Pumpbauwerk_Ufer.gpkg
    ## ├── Rheinwassertransportleitung.kml
    ## ├── Verteilbauwerk.gpkg
    ## ├── garzweilersee_gp.gpkg
    ## ├── garzweilersee_wasser.gpkg
    ## ├── hambachersee.gpkg
    ## ├── hambachersee_manheim.gpkg
    ## ├── hyperscaler-bedburg.gpkg
    ## ├── hyperscaler-bergheim.gpkg
    ## ├── indersee_gp.gpkg
    ## ├── rodungstrasse.gpkg
    ## ├── suendenwaeldchen.gpkg
    ## └── transportleitung_geom.gpkg

### Kartenvorbereitung

Um die Karte für die Webseite zu generieren wird zuerst das R-Skript
[`closeread/r_scrolly_map/pipe_map.R`](https://github.com/CorrelAid/klima-kollektiv/blob/main/closeread/r_scrolly_map/pipe_map.R)
ausgeführt. In dem Skript wird die Karte als `map.rds` gespeichert.
Diese Datei wird dann im Dokument
[`closeread/r_scrolly_map/das_ende_der_braunkohle.qmd`](https://github.com/CorrelAid/klima-kollektiv/blob/main/closeread/r_scrolly_map/das_ende_der_braunkohle.qmd)
eingelesen und in die scrollytelling Webseite integriert.

### Website generieren

Die eigentliche Webseite wird dann in der oben genannten `.qmd` Datei
generiert. Hierzu wird erstmal eine [Liste mit Koordinaten und Zoom
levels](https://github.com/CorrelAid/klima-kollektiv/blob/main/closeread/r_scrolly_map/das_ende_der_braunkohle.qmd#L25-L94)
erstellt, auf die die Karte beim scrollen der Seite fokussiert werden
soll.

Als “trigger” für die Änderung des Kartenfokus' dienen die jeweiligen
[`:::{focus-on="cr-setup_map"}`](https://github.com/CorrelAid/klima-kollektiv/blob/main/closeread/r_scrolly_map/das_ende_der_braunkohle.qmd#L134-L157)
sections in der `.qmd` Datei, die jeweils mit `:::` beendet werden.

Um die `.qmd` Datei rendern zu können, muss [quarto](https://quarto.org/)
und die zugehörige [closeread](https://closeread.dev/) extension
installiert sein. Letztere ist in diesem repo schon enthalten - im
Ornder
[closeread/r_scrolly_map/\_extensions/qmd-lab/closeread](https://github.com/CorrelAid/klima-kollektiv/tree/main/closeread/r_scrolly_map/_extensions/qmd-lab/closeread).
Daher sollte es genügen `quarto` zu installieren und die Webseite mit

`quarto render das_ende_der_braunkohle.qmd`

zu generieren.

**Wichtig!** <br> [Diese
Codezeilen](https://github.com/CorrelAid/klima-kollektiv/blob/main/closeread/r_scrolly_map/das_ende_der_braunkohle.qmd#L99-L127)
sollten nicht geändert werden! Sie sorgen dafür, dass die Story-sections
beim scrollen die Refokussierung der Karte triggern.

### Webseite erweitern

Um neue Sections zur Karte hinzuzufügen, muss nur ein neuer
Listeneintrag mit Koordinaten und Zoom level, zum Beispiel

``` r
list(
    coords = c(53.919, 8.288) #Neue Section
    , zoom = 14
  )
```

und eine neue `:::{focus-on="cr-setup_map"}` Section im Textteil hinzugefügt werden.
Zum Beispiel: 

    :::{focus-on="cr-setup_map"}

    ## Neue Section

    Hier der neue Text, eventuell mit Absätzen via 

    <br>

    html calls.

    :::

**Wichtig** hierbei ist, dass die Sections **NICHT** nach Namen mit den
Koordinaten in der Liste verbunden sind, sondern nach Position in der
Liste. Soll also eine neue Section nicht am Ende, sondern mittendrin
erstellt werden, müssen die Koordinaten nicht am Ende der Liste anghängt
sondern an der korrekten Stelle innerhalb der Liste eingefügt werden.
