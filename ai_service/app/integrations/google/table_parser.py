from typing import Any


class GoogleSheetTableParser:
    """
    Converts Google Sheets rows into dictionaries.

    Input:
        [
            ["product_id", "product_name"],
            ["SUN001", "Elegancea Sunlit"]
        ]

    Output:
        [
            {
                "product_id": "SUN001",
                "product_name": "Elegancea Sunlit"
            }
        ]
    """

    @staticmethod
    def normalize_header(header: Any) -> str:
        return (
            str(header)
            .strip()
            .lower()
            .replace(" ", "_")
        )

    def parse(
        self,
        rows: list[list[Any]],
    ) -> list[dict[str, str]]:
        if not rows:
            return []

        headers = [
            self.normalize_header(header)
            for header in rows[0]
        ]

        if not any(headers):
            raise ValueError(
                "The first row of the sheet must contain headers."
            )

        non_empty_headers = [
            header for header in headers if header
        ]

        if len(non_empty_headers) != len(set(non_empty_headers)):
            raise ValueError(
                "The Google Sheet contains duplicate column headers."
            )

        parsed_rows: list[dict[str, str]] = []

        for raw_row in rows[1:]:
            values = [
                str(value).strip()
                for value in raw_row
            ]

            if not any(values):
                continue

            padded_values = values + [""] * (
                len(headers) - len(values)
            )

            row_data = {
                header: padded_values[index]
                for index, header in enumerate(headers)
                if header
            }

            parsed_rows.append(row_data)

        return parsed_rows