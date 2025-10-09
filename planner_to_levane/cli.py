"""Interfaz de línea de comandos para el convertidor Planner -> Levane."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

import yaml

from .converter import PlannerToLevaneConverter, load_configuration


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Convierte un Excel exportado de Microsoft Planner al formato "
            "esperado por la plantilla de Levane."
        )
    )
    parser.add_argument("planner", help="Ruta al Excel exportado desde Planner")
    parser.add_argument("template", help="Ruta a la plantilla de Levane")
    parser.add_argument(
        "output",
        help="Ruta donde se guardará la copia de la plantilla con los datos proyectados",
    )
    parser.add_argument(
        "--config",
        required=True,
        help=(
            "Archivo YAML/JSON con la configuración de mapeo entre Planner y la plantilla"
        ),
    )
    parser.add_argument(
        "--filters",
        help=(
            "Filtros opcionales en formato JSON. Ej: '{\"Bucket\": [\"Diseño\", \"QA\"]}'"
        ),
    )
    return parser


def load_config_file(path: str | Path) -> Dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as fp:
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(fp)
        return json.load(fp)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    config_data = load_config_file(args.config)
    configuration = load_configuration(config_data)
    converter = PlannerToLevaneConverter(configuration)

    filters: Dict[str, Any] | None = None
    if args.filters:
        filters = json.loads(args.filters)

    converter.convert(
        planner_path=args.planner,
        template_path=args.template,
        output_path=args.output,
        sheet_filters=filters,
    )

    return 0


if __name__ == "__main__":  # pragma: no cover - punto de entrada
    raise SystemExit(main())

