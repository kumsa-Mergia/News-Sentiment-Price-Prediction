# 📰 News-Sentiment-Price-Prediction

This project aims to analyze financial news sentiment and its correlation with stock market movements. By leveraging Natural Language Processing (NLP) and financial data analysis tools, it predicts potential price shifts based on sentiment trends extracted from news headlines.

---

## 📂 Project Structure

```
News-Sentiment-Price-Prediction/
├── .github/workflows/     # GitHub Actions workflows for CI/CD
├── notebooks/             # Jupyter notebooks for exploratory analysis
├── scripts/               # Executable scripts
├── src/                   # Core source code (classes, functions, modules)
├── test/                  # Unit and integration tests
├── requirements.txt       # List of required Python packages
├── .gitignore             # Files/folders to ignore in Git
└── README.md              # Project documentation
```

---

## 🚀 Features

* Clean and preprocess large volumes of financial news data.
* Perform sentiment analysis using **TextBlob** and **VADER**.
* Merge sentiment data with historical stock price data.
* Apply technical indicators with **TA-Lib**.
* Visualize sentiment trends and stock movements.
* Continuous Integration (CI) with GitHub Actions.

---

## 🛠️ Environment Setup

Set up the development environment with the following steps:

### 1. Clone the Repository

```bash
git clone git@github.com:kumsa-Mergia/News-Sentiment-Price-Prediction.git
cd News-Sentiment-Price-Prediction
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv  # Use python3 on Linux/Mac
```

* **Windows:**

  ```bash
  venv\Scripts\activate
  ```

* **Mac/Linux:**

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Running Tests

Ensure your changes don’t break anything by running the test suite:

```bash
python -m unittest discover test
```

---

## ✅ CI/CD

This project uses **GitHub Actions** for Continuous Integration. Automated workflows run on every push to ensure code quality and functionality.

---

## 📬 Contact

For feedback, issues, or contributions, feel free to reach out via GitHub: [kumsa-Mergia](https://github.com/kumsa-Mergia)

---

