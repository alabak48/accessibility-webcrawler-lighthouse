# Accessibility Web Crawler with Lighthouse

A web accessibility crawler that utilizes both JavaScript and Python to assess and generate accessibility reports in JSON format for specified websites.

## Requirements
- Pycharm Community Edition
- Node v20.10.0

## Installation
```python
npm install
```

## Start the project
Run main.py


## Tijek istraživanja (S kao stage)
- Prvo dobiveni popis domena učiniti dostupnim na REST API end point
- Za svaku domenu pronaći stvarni url (S01): http, https, www, ne postoji, drugi razlozi
- Na svakoj pronađenoj domeni pobrati sve poveznice na prvoj razini (S02_L1)
- Na svakoj pronađenoj poveznici na prvoj razini pronaći sve poveznice na drugoj razini (S02_L2)
- Na pronađenim poveznicama prve i druge razine identificirati poddomene
- na svakoj domeni i poddomeni provesti LightHouse magiju i podatke spremiti u bazu
- analizirati podatke

## procjenjeno vrijeme istraživanja
112.64327383041382 seconds za 10 domena, jedna domena 13 sekundi
110.000 domena * 13 = 1430000 sekunde = 398 sati
Jedno računalo u jednom satu odradi ((60 * 60) / 13) 277 domena
Dvije učionice na FFOS ukupno 50 računala u jednom satu 13850 domena
Na bazi 50 računala (110.000 domena / 13850 po satu) daje 8 sati - jedna subota i gotovi smo

# status domene
0. početni status
1. u tijeku je traženje stvarne domene
2. stvarna domena razriješena (ili posotoji ili je NULL)
3. u tijeku traženje poddomena
4. poddomene razriješene
5. u tijeku je lighthouse magija
6. lighthouse magija odrađena
7. KASNIJE
8. KASNIJE
9. KASNIJE
10. Ne pobire se jer stvarna domena vodi izvan .hr domene