class GoogleSheetRangeBuilder:
    """
    Builds valid Google Sheets A1 notation ranges.

    Examples:
        Product Knowledge + A:Z
        becomes:
        'Product Knowledge'!A:Z
    """

    @staticmethod
    def build(
        sheet_name: str,
        cell_range: str = "A:Z",
    ) -> str:
        normalized_sheet_name = sheet_name.strip()
        normalized_cell_range = cell_range.strip()

        if not normalized_sheet_name:
            raise ValueError("sheet_name cannot be empty.")

        if not normalized_cell_range:
            raise ValueError("cell_range cannot be empty.")

        # Google Sheets escapes a single quote by doubling it.
        escaped_sheet_name = normalized_sheet_name.replace("'", "''")

        return f"'{escaped_sheet_name}'!{normalized_cell_range}"