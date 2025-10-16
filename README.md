# Transactions Dashboard

## Main Features

### Overview Tab
- Shows **total number of transactions** and **total spending**.
- Displays **average spending per month**.
- Bar chart of **total spending by category**.
- Highlights the **top spending category**.

### Trends Tab
- Shows spending trends over time (**Daily, Weekly, Monthly**).
- Line chart for **total amount trend**.
- Area chart for **weekly spending by top 5 categories**.

### Merchant & Payment Tab
- Top 10 merchants by total spend.
- Distribution of payment methods using a pie chart.
- Breakdown of spending by merchants within a specific category.

### Data Table Tab
- Filtered data preview (up to 300 rows).
- Highlight negative transactions with warnings (should be cleaned already).
- Option to download the filtered CSV.

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Engulfy/financial_analysis.git
cd financial_analysis
```

2. **Create a virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the Streamlit app:**
```bash
streamlit run app.py
```
