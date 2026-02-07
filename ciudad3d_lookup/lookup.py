from __future__ import annotations

import csv
import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional

import yaml


@dataclass(frozen=True)
class LookupConfig:
    templates: Dict[str, str]
    geocoder_url: Optional[str] = None


class LookupError(RuntimeError):
    pass


def load_config(path: str) -> LookupConfig:
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    templates = data.get("templates", {})
    if not templates:
        raise LookupError("El archivo de configuración no define plantillas 'templates'.")
    return LookupConfig(
        templates=templates,
        geocoder_url=data.get("geocoder_url"),
    )


def resolve_smp_from_csv(address: str, csv_path: str) -> Optional[str]:
    normalized = address.strip().lower()
    with open(csv_path, "r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            addr_value = (row.get("address") or "").strip().lower()
            if addr_value == normalized:
                return (row.get("smp") or "").strip() or None
    return None


def resolve_smp_from_geocoder(address: str, geocoder_url: str) -> Optional[str]:
    url = geocoder_url.format(address=urllib.parse.quote(address))
    with urllib.request.urlopen(url, timeout=20) as response:
        payload = response.read().decode("utf-8")
    data = json.loads(payload)
    for entry in data.get("resultados", []):
        smp = entry.get("smp")
        if smp:
            return smp
    return None


def build_urls(templates: Dict[str, str], smp: str, address: str | None = None) -> Dict[str, str]:
    context = {
        "smp": smp,
        "address": address or "",
    }
    return {key: template.format(**context) for key, template in templates.items()}


def lookup_downloads(
    config: LookupConfig,
    *,
    address: Optional[str] = None,
    smp: Optional[str] = None,
    address_map: Optional[str] = None,
) -> Dict[str, Any]:
    if not address and not smp:
        raise LookupError("Debe enviar 'address' o 'smp'.")

    resolved_smp = smp
    if not resolved_smp and address:
        if address_map:
            resolved_smp = resolve_smp_from_csv(address, address_map)
        if not resolved_smp and config.geocoder_url:
            resolved_smp = resolve_smp_from_geocoder(address, config.geocoder_url)

    if not resolved_smp:
        raise LookupError(
            "No se pudo resolver el SMP. Proporcione 'smp' directamente o configure un mapa/geocodificador."
        )

    urls = build_urls(config.templates, resolved_smp, address=address)
    return {
        "smp": resolved_smp,
        "urls": urls,
    }
