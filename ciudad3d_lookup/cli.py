from __future__ import annotations

import argparse
import json
import sys

from .lookup import LookupError, load_config, lookup_downloads


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolver enlaces de descarga de Ciudad3D por dirección o SMP."
    )
    parser.add_argument("--config", required=True, help="Ruta al YAML con plantillas y geocoder.")
    parser.add_argument("--address", help="Dirección a buscar (ej: 'Suipacha 50').")
    parser.add_argument("--smp", help="SMP directo (ej: '051-112-032').")
    parser.add_argument(
        "--address-map",
        help="CSV con columnas 'address' y 'smp' para resolver direcciones sin geocoder.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        result = lookup_downloads(
            config,
            address=args.address,
            smp=args.smp,
            address_map=args.address_map,
        )
    except LookupError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
