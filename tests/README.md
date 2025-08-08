# Unit Testing for Data Preprocessing

This document provides instructions for setting up, running, and debugging the unit tests for the `DataPreprocessor` class.

## 📌 Project Structure
```
Brent-Oil-Price-Change-Point-Analysis/
│── scripts/
│   ├── data_preprocessing.py
│── tests/
│   ├── test_data_preprocessing.py
│── requirements.txt
│── README.md
```

## 🛠️ Setup
### 1️⃣ Install Dependencies
Make sure you have Python installed (preferably 3.12+). Then, install the required dependencies:
```pip install -r requirements.txt```
If you don’t have a `requirements.txt` file, install `pytest` manually:
```pip install pytest```

## 🚀 Running the Tests
Navigate to the root of the project and run:
```pytest```
This will discover and run all test files inside the `tests/` directory.

### Running a Specific Test File
To run a specific test file, use:
```pytest tests/test_data_preprocessing.py```

### Running a Specific Test Case
If you want to run a single test function:
```pytest tests/test_data_preprocessing.py::test_function_name```

### Running Tests with Detailed Output
For verbose mode, which shows detailed logs and test progress:
```pytest -v```

For live output (especially useful for debugging `print` statements):
```pytest -s```

## 🛠️ Debugging Failed Tests
If a test fails, you can rerun it with debugging enabled:
```pytest --pdb```
This will drop you into an interactive Python debugger when a test fails.

## ✅ Best Practices for Writing Tests
- **Use meaningful test function names** (e.g., `test_load_data_handles_missing_file`).
- **Mock dependencies properly** using `unittest.mock.patch`.
- **Keep test cases independent**—each should run without relying on others.
- **Run tests frequently** to catch issues early.

## 📜 References
- [pytest Documentation](https://docs.pytest.org/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

## Happy Testing! 🧪🚀

