"""Transformaciones reutilizables para columnas del template."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, Mapping

import pandas as pd

TransformFunc = Callable[[Mapping[str, Any], str | None, Mapping[str, Any]], Any]


def identity_transform(
    *, row: Mapping[str, Any], planner_field: str | None, options: Mapping[str, Any]
) -> Any:
    if planner_field is None:
        return None
    return row.get(planner_field, None)


def constant_transform(
    *, row: Mapping[str, Any], planner_field: str | None, options: Mapping[str, Any]
) -> Any:
    return options.get("value")


def date_transform(
    *, row: Mapping[str, Any], planner_field: str | None, options: Mapping[str, Any]
) -> Any:
    if not planner_field:
        return None
    value = row.get(planner_field)
    if value in (None, ""):
        return None

    input_format = options.get("input_format")
    output_format = options.get("output_format", "%d/%m/%Y")

    if isinstance(value, datetime):
        dt = value
    else:
        if input_format:
            dt = datetime.strptime(str(value), input_format)
        else:
            dt = pd.to_datetime(value, dayfirst=False, errors="coerce")
            if pd.isna(dt):
                return None
    return dt.strftime(output_format)


def datetime_transform(
    *, row: Mapping[str, Any], planner_field: str | None, options: Mapping[str, Any]
) -> Any:
    options = {"output_format": "%d/%m/%Y %H:%M"} | options
    return date_transform(row=row, planner_field=planner_field, options=options)


def duration_hours_transform(
    *, row: Mapping[str, Any], planner_field: str | None, options: Mapping[str, Any]
) -> Any:
    start_field = options.get("start_field")
    end_field = options.get("end_field")
    if not start_field or not end_field:
        raise ValueError(
            "Las opciones 'start_field' y 'end_field' son obligatorias para duration_hours"
        )

    hours_per_day = float(options.get("hours_per_day", 8))

    start_value = row.get(start_field)
    end_value = row.get(end_field)
    if not start_value or not end_value:
        return None

    start_dt = pd.to_datetime(start_value, errors="coerce")
    end_dt = pd.to_datetime(end_value, errors="coerce")
    if pd.isna(start_dt) or pd.isna(end_dt):
        return None

    delta = end_dt - start_dt
    days = delta.days + delta.seconds / 86400
    if days < 0:
        return None

    hours = round(days * hours_per_day, 2)
    return hours


def concat_transform(
    *, row: Mapping[str, Any], planner_field: str | None, options: Mapping[str, Any]
) -> Any:
    fields = options.get("fields")
    if not fields:
        raise ValueError("La transformación 'concat' requiere la opción 'fields'")
    separator = options.get("separator", " ")
    values = [str(row.get(field, "")).strip() for field in fields if row.get(field)]
    return separator.join(values)


TRANSFORMS: Dict[str, TransformFunc] = {
    "identity": identity_transform,
    "constant": constant_transform,
    "date": date_transform,
    "datetime": datetime_transform,
    "duration_hours": duration_hours_transform,
    "concat": concat_transform,
}


def register_transform(name: str, func: TransformFunc) -> None:
    """Permite registrar transformaciones personalizadas."""

    if name in TRANSFORMS:
        raise ValueError(f"Ya existe una transformación registrada con el nombre '{name}'")
    TRANSFORMS[name] = func

