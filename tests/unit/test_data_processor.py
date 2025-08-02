"""
Unit tests for DataProcessor class.
"""

import pytest
import pandas as pd
import tempfile
import os
from src.app.data_processor import DataProcessor


class TestDataProcessor:
    """Test cases for DataProcessor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.processor = DataProcessor()

        # Create sample data for testing
        self.sample_data = pd.DataFrame(
            {
                "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "amount": [100.0, 200.0, 300.0],
                "product": ["A", "B", "C"],
            }
        )

    def test_load_data_success(self):
        """Test successful data loading."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            self.sample_data.to_csv(f.name, index=False)
            file_path = f.name

        try:
            # Test loading
            data = self.processor.load_data(file_path)
            assert len(data) == 3
            assert list(data.columns) == ["date", "amount", "product"]
            print("✅ Data loading test passed!")
        finally:
            # Clean up
            os.unlink(file_path)

    def test_load_data_file_not_found(self):
        """Test data loading with non-existent file."""
        with pytest.raises(FileNotFoundError):
            self.processor.load_data("nonexistent.csv")
        print("✅ File not found test passed!")

    def test_clean_data_success(self):
        """Test successful data cleaning."""
        # Add some null values
        data_with_nulls = self.sample_data.copy()
        data_with_nulls.loc[1, "amount"] = None

        # Clean data
        cleaned = self.processor.clean_data(data_with_nulls)

        # Check results
        assert len(cleaned) == 2  # One row removed due to null
        assert cleaned["amount"].dtype == "float64"
        assert cleaned["date"].dtype == "datetime64[ns]"
        print("✅ Data cleaning test passed!")

    def test_clean_data_empty(self):
        """Test data cleaning with empty data."""
        empty_data = pd.DataFrame()

        with pytest.raises(ValueError, match="Data is empty"):
            self.processor.clean_data(empty_data)
        print("✅ Empty data test passed!")

    def test_calculate_metrics_success(self):
        """Test metrics calculation."""
        metrics = self.processor.calculate_metrics(self.sample_data)

        # Check expected values
        assert metrics["total_sales"] == 600.0
        assert metrics["avg_sales"] == 200.0
        assert metrics["count"] == 3
        print("✅ Metrics calculation test passed!")

    def test_calculate_metrics_empty(self):
        """Test metrics calculation with empty data."""
        empty_data = pd.DataFrame()
        metrics = self.processor.calculate_metrics(empty_data)

        # Check default values
        assert metrics["total_sales"] == 0.0
        assert metrics["avg_sales"] == 0.0
        assert metrics["count"] == 0
        print("✅ Empty metrics test passed!")

    def test_calculate_metrics_no_amount_column(self):
        """Test metrics calculation without amount column."""
        data_no_amount = pd.DataFrame({"date": ["2024-01-01"], "product": ["A"]})

        with pytest.raises(ValueError, match="Amount column not found"):
            self.processor.calculate_metrics(data_no_amount)
        print("✅ Missing amount column test passed!")

    def test_full_pipeline_success(self):
        """Test complete data processing pipeline."""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            self.sample_data.to_csv(f.name, index=False)
            file_path = f.name

        try:
            # Run full pipeline
            result = self.processor.process_sales_data(file_path)

            # Check results
            assert result["total_sales"] == 600.0
            assert result["avg_sales"] == 200.0
            assert result["count"] == 3
            assert self.processor.processed_data is not None
            print("✅ Full pipeline test passed!")
        finally:
            # Clean up
            os.unlink(file_path)
