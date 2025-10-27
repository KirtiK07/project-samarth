import pandas as pd
import os
from typing import Dict, Any

class DataLoader:
    def __init__(self, data_dir: str = "../data"):
        self.data_dir = data_dir
        self.crop_data = None
        self.rainfall_data = None
        self.load_data()

    def load_data(self):
        """Load CSV files into pandas DataFrames"""
        try:
            # Load crop production data
            crop_path = os.path.join(self.data_dir, "crop_production.csv")
            self.crop_data = pd.read_csv(crop_path)
            print(f"Loaded crop data: {len(self.crop_data)} rows")

            # Load rainfall data
            rainfall_path = os.path.join(self.data_dir, "rainfall_data.csv.csv")
            self.rainfall_data = pd.read_csv(rainfall_path)
            print(f"Loaded rainfall data: {len(self.rainfall_data)} rows")

            # Clean up column names
            self.crop_data.columns = self.crop_data.columns.str.strip()
            self.rainfall_data.columns = self.rainfall_data.columns.str.strip()

        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def get_crop_data(self) -> pd.DataFrame:
        """Return crop production data"""
        return self.crop_data

    def get_rainfall_data(self) -> pd.DataFrame:
        """Return rainfall data"""
        return self.rainfall_data

    def get_districts_from_crop_data(self) -> list:
        """Get list of districts from crop data"""
        if self.crop_data is not None:
            return self.crop_data['District Name'].unique().tolist()
        return []

    def get_districts_from_rainfall_data(self) -> list:
        """Get list of districts from rainfall data"""
        if self.rainfall_data is not None:
            return self.rainfall_data['District'].unique().tolist()
        return []

    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of available data"""
        return {
            "crop_data": {
                "rows": len(self.crop_data) if self.crop_data is not None else 0,
                "columns": list(self.crop_data.columns) if self.crop_data is not None else [],
                "districts": self.get_districts_from_crop_data()
            },
            "rainfall_data": {
                "rows": len(self.rainfall_data) if self.rainfall_data is not None else 0,
                "columns": list(self.rainfall_data.columns) if self.rainfall_data is not None else [],
                "districts": self.get_districts_from_rainfall_data()
            }
        }
