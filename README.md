# julian-santarsiero

Herramienta para convertir exportaciones de Microsoft Planner al template de Levane.

## Instalación

Se recomienda utilizar un entorno virtual de Python 3.10 o superior:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python -m planner_to_levane.cli \
  path/al/export_planner.xlsx \
  path/a/la_plantilla_levane.xlsx \
  path/de/salida.xlsx \
  --config configs/ejemplo_configuracion.yaml
```

Opcionalmente se pueden aplicar filtros a las filas del Planner enviando el
parámetro `--filters` con un JSON. Ejemplo para limitar a ciertos buckets:

```bash
python -m planner_to_levane.cli planner.xlsx template.xlsx salida.xlsx \
  --config configs/ejemplo_configuracion.yaml \
  --filters '{"Bucket": ["Diseño", "QA"]}'
```

El archivo de configuración define cómo se mapean las columnas del Planner al
template. Puedes duplicar `configs/ejemplo_configuracion.yaml` y ajustarlo a las
cabeceras reales de tu plantilla.

### Transformaciones disponibles

- `identity`: copia el valor tal como viene del Planner.
- `constant`: utiliza el valor definido en `options.value`.
- `date`: convierte fechas al formato deseado (`options.output_format`).
- `datetime`: similar a `date`, pero con hora (`%d/%m/%Y %H:%M` por defecto).
- `duration_hours`: calcula la duración entre dos campos (`start_field`,
  `end_field`) multiplicada por `hours_per_day`.
- `concat`: concatena múltiples columnas del Planner con un separador.

### Extender con transformaciones propias

Puedes registrar transformaciones adicionales en tu propio script antes de
invocar al convertidor:

```python
from planner_to_levane import register_transform

def mi_transformacion(**kwargs):
    # lógica personalizada
    ...

register_transform("mi_transformacion", mi_transformacion)
```

## Dependencias

Las dependencias mínimas se encuentran en `requirements.txt`.

## Ciudad3D lookup (dirección o SMP)

Se agregó un buscador simple que construye URLs de descarga para Ciudad3D a partir

- de un SMP directo, o
- de una dirección usando un CSV de mapeo.

Consulta `docs/ciudad3d_lookup.md` para configurar plantillas y ejemplos de uso.
