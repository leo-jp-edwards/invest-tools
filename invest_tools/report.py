import typing
from datetime import datetime

from fpdf import FPDF

MARGIN = 10
CELL_HEIGHT = 50
PAGE_WIDTH = 210 - 2 * MARGIN
PAGE_HEIGHT = 297 - 2 * MARGIN
TABLE_CELL_HEIGHT = 8


class PDF(FPDF):
    def __init__(self):
        super().__init__()

    def header(self):
        self.set_font("Arial", "B", 20)
        self.cell(
            0, 10, f"Portfolio Report: {datetime.now().strftime('%d/%m/%Y')}", 1, 1, "C"
        )

    def table(self, analysis: typing.Dict[str, float], columns: typing.List[str]):
        # Header
        self.set_font("Arial", "B", 10)
        for i, col in enumerate(columns):
            self.cell(w=40, h=TABLE_CELL_HEIGHT, txt=col, border=1, ln=i, align="L")
        self.set_font("Arial", "", 8)
        for metric, value in analysis.items():
            self.cell(w=40, h=TABLE_CELL_HEIGHT, txt=metric, border=1, ln=0, align="L")
            self.cell(
                w=40, h=TABLE_CELL_HEIGHT, txt=str(value), border=1, ln=1, align="L"
            )

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "", 8)
        self.cell(0, 10, "", 1, 0, "C")
