**Tag 1: Grundlagen & Setup**  
- [ ] Erstelle neues Projektverzeichnis und initialisiere Virtualenv  
- [ ] Installiere benötigte Bibliotheken: `fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, `python-multipart`  
- [ ] Erstelle `main.py` mit grundlegender App (z.B. `/health`-Endpunkt)  
- [ ] Teste die Installation mit `uvicorn main:app --reload`  
- [ ] Füge `requirements.txt` hin  

---

**Tag 2: Markdown-Rendering**  
- [ ] Implementiere Markdown-Rendering mit `marked`  
- [ ] Füge Endpunkt `/pages` hin (für Seiten mit Markdown-Content)  
- [ ] Teste Markdown-Rendering mit Beispiel-Page (z.B. "Hallo, Welt!")  
- [ ] Füge einfache Formatierungen hin (Header, Listen, Fett)  

---

**Tag 3: Seiten-Struktur (Pages)**  
- [ ] Definiere `Page`-Modell mit Feldern: `id`, `title`, `content`, `created_at`, `updated_at`  
- [ ] Füge Endpunkt `/pages` hin (für Erstellung neuer Seiten)  
- [ ] Teste, ob Seiten korrekt gespeichert werden  
- [ ] Erstelle Testseite mit Beispielinhalt  

---

**Tag 4: Datenbanken (Databases)**  
- [ ] Definiere `Database`-Modell mit Feldern: `id`, `name`, `description`, `page_id`  
- [ ] Füge Endpunkt `/databases` hin (für Erstellung von Datenbanken)  
- [ ] Teste, ob Datenbanken korrekt mit Seiten verknüpft werden  
- [ ] Implementiere einfache Filter- und Sortierfunktionen (z.B. `?filter=tag:projekt`)  

---

**Tag 5: Authentifizierung (JWT)**  
- [ ] Implementiere JWT-System mit `python-jose`  
- [ ] Füge Endpunkt `/login` hin (für Benutzer-Authentifizierung)  
- [ ] Schreibe geschützte Endpunkte (z.B. `/pages` mit `Authorization: Bearer`)  
- [ ] Teste, ob Seiten mit autorisierten Benutzern korrekt geschrieben werden  
- [ ] Erstelle 2 Testbenutzer  

---

**Tag 6: Views & Flexibilität**  
- [ ] Füge Endpunkt `/views` hin (für verschiedene Ansichten)  
- [ ] Teste, ob Seiten mit verschiedenen Ansichten korrekt gespeichert werden  
- [ ] Füge einfache Kategorien hin (z.B. "Projekt", "Notizen")  
- [ ] Teste, ob Seiten mit Kategorien korrekt dargestellt werden  

---

**Tag 7: Testen & Dokumentation**  
- [ ] Schreibe 2-3 unit-tests mit `pytest` (z.B. für `/pages`-Endpunkt)  
- [ ] Füge Endpunkt `/pages` hin (für Suchfunktionen)  
- [ ] Teste, ob Suchfunktionen (z.B. `?query=Projekt`) korrekt funktionieren  
- [ ] Füge einfache Dokumentation hin (z.B. API-Referenz)