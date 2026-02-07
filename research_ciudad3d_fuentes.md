# Fuentes de datos observadas en ciudad3d.buenosaires.gob.ar

Salida relevante de `config.js` (extraída con Playwright) que define las URLs base de servicios y reemplazos usados por la app:

```
var configs = {
  urlConfigBase: 'configBase.json',
  modelBA: 'https://epok.buenosaires.gob.ar/cur3d/modelBA/zip/',
  urlLayers: 'https://epok.buenosaires.gob.ar/mbtiles/',
  includes: {
    urlAPI: 'https://epok.buenosaires.gob.ar',
    urlPhoto: 'https://fotos.usig.buenosaires.gob.ar',
    urlWsUsig: 'https://ws.usig.buenosaires.gob.ar',
    urlApiServicioGeo: 'https://ws.usig.buenosaires.gob.ar',
    urlPDF: 'http://ssplan.buenosaires.gov.ar/man_atipicas/imagenes',
    urlCAD: 'https://epok.buenosaires.gob.ar/cur3d/dxf'
  },
  replaces: [
    {
      key: '{{urlBsAsData}}',
      value: 'https://data.buenosaires.gob.ar/'
    }
  ]
}
```
