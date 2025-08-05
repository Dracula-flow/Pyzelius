
from pathlib import Path
from src.ReportMaker import DataFeeder, ReportMaker
from typing import Optional
from src.Functions import time_responser

class ReportController:
    """
    Handles logic related to generating test reports.
    """

    def __init__(self, base_path: Path, date_str: Optional[str] = None):
        self.base_path = base_path
        self.date_str = date_str or time_responser('date')

    def generate_report(self) -> None:
        """
        Gathers test results and creates an .xlsx report with two sheets: Passed and Defects.
        """
        daily_folder = self.base_path / self.date_str

        # Create data sources
        passed_data = DataFeeder("Passed", daily_folder)
        defect_data = DataFeeder("Defects", daily_folder)

        # Convert to DataFrames
        df_passed = passed_data.to_dataframe(daily_folder, DataFeeder.passed_headers())
        df_defect = defect_data.to_dataframe(daily_folder, DataFeeder.defect_headers())

        # Generate and save report
        report = ReportMaker(daily_folder / "Report")
        report.data_feed(df_passed, df_defect)