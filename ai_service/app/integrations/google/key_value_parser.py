from typing import Any


class GoogleSheetKeyValueParser:

    def parse(
        self,
        rows: list[list[Any]],
    ) -> dict[str, str]:

        if len(rows) < 2:
            return {}

        result = {}

        for row in rows[1:]:

            if len(row) < 2:
                continue

            key = str(row[0]).strip()

            value = str(row[1]).strip()

            if not key:
                continue

            result[key] = value

        return result