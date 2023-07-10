# WebsiteScapperForChoir

Dies ist eine kleines Python-Framework, um Websiten nach den Wörtern "Chor, Chöre, Schulchor, und Schulchöre" zu durchsuchen. Mit den Daten kann am Ende abgeschätzt werden, wie viele Schulen noch Schulchöre haben.

Als Datenbasis können die Schuldatenbanken der Bundesländer genutzt werden. Zwei Beispiele sind in der config.ini enthalten.

Die Schuldaten müssen dabei als CSV-Datei verfügbar sein, wobei jede Schule einer Zeile entspricht. Mindestens ist der Schulname und die URL der Schulwebseite notwendig.

Der Aufruf erfolgt im Verzeichnis mittels "python3 scapper.py" (nachdem die CSV mit den Schuldaten im Verzeichnis bereitgestellt wurden und die config.ini angepasst wurde).

## bisherige Unzulänglichkeiten

- Es werden keine PDF gecrawled in denen teilweise die Stundenpläne mit "Chor" enthalten sind.
- direkte Redirects der Einstiegsdomain auf eine andere Domain werden meist nicht verfolgt, durch die Verwendung von allow_domains
