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