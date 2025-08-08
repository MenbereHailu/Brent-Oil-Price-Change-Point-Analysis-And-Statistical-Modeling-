import os
import logging
import pytest
import pandas as pd
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.data_preprocessing import DataPreprocessor

@pytest.fixture
def sample_csv(tmp_path):
    """Creates a sample CSV file for testing."""
    data = """Date,Value
    2023-01-01,100
    2023-01-02,200
    """
    file_path = tmp_path / "test_data.csv"
    file_path.write_text(data)
    return str(file_path)


def test_initialization(sample_csv, tmp_path):
    output_dir = str(tmp_path / "output")
    processor = DataPreprocessor(file_path=sample_csv, output_dir=output_dir)
    
    assert processor.file_path == sample_csv
    assert processor.output_dir == output_dir
    assert processor.output_file == os.path.join(output_dir, "data.csv")
    assert isinstance(processor.logger, logging.Logger)

def test_logging_setup(sample_csv, tmp_path):
    log_file = str(tmp_path / "logfile.log")
    processor = DataPreprocessor(file_path=sample_csv, log_file=log_file)

    # Log a test message
    processor.logger.info("Test log message")

    # Ensure log file exists
    assert os.path.exists(log_file)

    # Read the log file content
    with open(log_file, "r") as f:
        log_content = f.read()

    # Check if the log file contains the expected log message
    assert "Test log message" in log_content


@patch("pandas.read_csv")
def test_load_data(mock_read_csv, sample_csv, tmp_path):
    """Tests if load_data correctly reads the file."""
    mock_df = pd.DataFrame({"Date": ["2023-01-01", "2023-01-02"], "Value": [100, 200]})
    mock_read_csv.return_value = mock_df
    processor = DataPreprocessor(file_path=sample_csv, output_dir=str(tmp_path))
    df = processor.load_data()
    assert isinstance(df, pd.DataFrame)
    assert "Date" in df.columns
    assert df.shape == (2, 2)
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])  # Ensure Date conversion


def test_inspect_with_empty_dataframe():
    processor = DataPreprocessor(file_path="dummy.csv")
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="The DataFrame is empty."):
        processor.inspect(empty_df)


