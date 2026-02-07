# Buscador simple por dirección o SMP

Esta utilidad construye URLs de descarga para Ciudad3D tomando una dirección o un
SMP (Sección-Manzana-Parcela). La salida depende de plantillas configurables.

## Configuración

Edita `configs/ciudad3d_lookup.yaml` para definir los patrones de descarga reales.
Por ejemplo:

```yaml
templates:
  modelo_zip: "https://epok.buenosaires.gob.ar/cur3d/modelBA/zip/{smp}.zip"
  dxf: "https://epok.buenosaires.gob.ar/cur3d/dxf/{smp}.dxf"
```

Si necesitas resolver dirección → SMP, puedes:

- Pasar un CSV con columnas `address` y `smp` usando `--address-map`.
- O bien habilitar `geocoder_url` cuando tengas acceso al endpoint apropiado.

## Uso

### Con SMP directo

```bash
python -m ciudad3d_lookup.cli \
  --config configs/ciudad3d_lookup.yaml \
  --smp "051-112-032"
```

### Con dirección y CSV de mapeo

```bash
python -m ciudad3d_lookup.cli \
  --config configs/ciudad3d_lookup.yaml \
  --address "Suipacha 50" \
  --address-map datos/direcciones.csv
```

La salida se imprime como JSON con el SMP resuelto y los enlaces construidos.
