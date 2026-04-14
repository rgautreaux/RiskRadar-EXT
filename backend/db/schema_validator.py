from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


@dataclass
class SchemaValidationOutcome:
    ok: bool
    issues: list[str]


def validate_required_schema(
    engine: Engine,
    required_schema: dict[str, set[str]],
) -> SchemaValidationOutcome:
    inspector = inspect(engine)
    issues: list[str] = []

    try:
        existing_tables = set(inspector.get_table_names())
    except SQLAlchemyError as error:  # pragma: no cover - defensive runtime capture
        return SchemaValidationOutcome(ok=False, issues=[f"Failed to inspect database tables: {error}"])

    for table_name, required_columns in required_schema.items():
        if table_name not in existing_tables:
            issues.append(f"Missing required table: {table_name}")
            continue

        try:
            existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
        except SQLAlchemyError as error:  # pragma: no cover - defensive runtime capture
            issues.append(f"Failed to inspect columns for table '{table_name}': {error}")
            continue

        missing_columns = sorted(required_columns - existing_columns)
        if missing_columns:
            issues.append(
                f"Missing required columns in '{table_name}': {', '.join(missing_columns)}"
            )

    return SchemaValidationOutcome(ok=not issues, issues=issues)


def build_required_schema_from_models(model_base, table_names: set[str]) -> dict[str, set[str]]:
    required: dict[str, set[str]] = {}
    for table_name in table_names:
        table = model_base.metadata.tables.get(table_name)
        if table is None:
            continue
        required[table_name] = {column.name for column in table.columns}
    return required
