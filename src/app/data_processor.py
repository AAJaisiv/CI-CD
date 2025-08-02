"""
Data processing module for sales data.
"""

import pandas as pd
from typing import Dict


class DataProcessor:
    """Process sales data with validation and cleaning."""

    def __init__(self):
        self.processed_data = None

    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from CSV file."""
        try:
            data = pd.read_csv(file_path)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean the data by removing nulls and fixing data types."""
        if data.empty:
            raise ValueError("Data is empty")

        # Remove null values and create a copy to avoid warnings
        cleaned = data.dropna().copy()

        # Convert date column if it exists
        if "date" in cleaned.columns:
            cleaned["date"] = pd.to_datetime(cleaned["date"])

        # Convert amount to numeric if it exists
        if "amount" in cleaned.columns:
            cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce")
            cleaned = cleaned.dropna(subset=["amount"])

        return cleaned

    def calculate_metrics(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate sales metrics."""
        if data.empty:
            return {"total_sales": 0.0, "avg_sales": 0.0, "count": 0}

        if "amount" not in data.columns:
            raise ValueError("Amount column not found in data")

        total_sales = data["amount"].sum()
        avg_sales = data["amount"].mean()
        count = len(data)

        return {
            "total_sales": float(total_sales),
            "avg_sales": float(avg_sales),
            "count": count,
        }

    def process_sales_data(self, file_path: str) -> Dict[str, float]:
        """Complete data processing pipeline."""
        # Load data
        data = self.load_data(file_path)

        # Clean data
        cleaned_data = self.clean_data(data)

        # Calculate metrics
        metrics = self.calculate_metrics(cleaned_data)

        # Store processed data
        self.processed_data = cleaned_data

        return metrics
