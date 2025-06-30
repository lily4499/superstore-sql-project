
---

## 🧠 Project Goal

**📊 Business Question:**
*What are the sales trends, most profitable products, and key customer segments?*

---

## 🗂️ Step 1: Project Folder Structure

```bash
superstore-sql-project/
├── data/
│   └── superstore_orders.csv
├── sql/
│   ├── create_table.sql
│   ├── load_data.sql
│   ├── analysis_queries.sql
├── README.md
```

---

## 💾 Step 2: Save Your Dataset

Save the data you provided as:

```
superstore-sql-project/data/superstore_orders.csv

python3 -m venv venv
source venv/bin/activate
pip install kaggle
mkdir data && cd data
kaggle datasets download ...
unzip ...
mv 'Sample - Superstore.csv' superstore_orders.csv
```

## Clean Data
To fix the data before loading using LOAD DATA INFILE, we need to address common formatting issues like:  
Excel-style dates (MM/DD/YYYY)  
Commas in text fields (especially in Product Name)  
Special characters or quotes  
Ensuring correct column count  
We'll handle this by preprocessing the CSV in the CLI or Python before loading it into MySQL.  

Save this script as clean_csv.py in your project root:
```
import pandas as pd

# Load original CSV
# Try encoding='latin1' or 'windows-1252' if 'utf-8' fails
df = pd.read_csv('data/superstore_orders.csv', encoding='latin1')

# Example data check
print(df.head())

# ✅ 1. Fix date format (MM/DD/YYYY → YYYY-MM-DD)
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')

# ✅ 2. Strip whitespace
df.columns = [col.strip() for col in df.columns]
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# ✅ 3. Remove duplicates (optional)
df = df.drop_duplicates()

# ✅ 4. Handle NaNs: fill with zeros or drop
df = df.fillna({
    'Sales': 0,
    'Quantity': 0,
    'Discount': 0,
    'Profit': 0
})

# ✅ 5. Save cleaned version
df.to_csv('data/superstore_orders_cleaned.csv', index=False)
print("✅ Clean CSV saved as: data/superstore_orders_cleaned.csv")

```

Run it from terminal:
```
python3 clean_csv.py

```

---

## 🛠️ Step 3: Set Up MySQL Locally (Ubuntu CLI)

```bash
# Install MySQL
sudo apt update
sudo apt install mysql-server

# Start MySQL
sudo systemctl start mysql

# Log into MySQL
sudo mysql -u root -p
SET GLOBAL validate_password.policy = LOW;
SET GLOBAL validate_password.length = 6;

```

Create a user and database:

```sql
CREATE DATABASE superstore;
CREATE USER 'lili'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON superstore.* TO 'lili'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 🧱 Step 4: Create Table (SQL File)

Save as `sql/create_table.sql`:

```sql
USE superstore;

CREATE TABLE orders (
    Row_ID INT,
    Order_ID VARCHAR(20),
    Order_Date DATE,
    Ship_Date DATE,
    Ship_Mode VARCHAR(50),
    Customer_ID VARCHAR(20),
    Customer_Name VARCHAR(100),
    Segment VARCHAR(50),
    Country VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    Postal_Code VARCHAR(10),
    Region VARCHAR(20),
    Product_ID VARCHAR(20),
    Category VARCHAR(50),
    Sub_Category VARCHAR(50),
    Product_Name TEXT,
    Sales FLOAT,
    Quantity INT,
    Discount FLOAT,
    Profit FLOAT
);
```

Run it:

```bash
mysql -u lili -p superstore < sql/create_table.sql
```

---

## 📥 Step 5: Load Data into MySQL

1. Open MySQL:

```bash
mysql -u lili -p superstore
```

2. Load CSV (first enable `secure_file_priv` folder):

Check value:

```sql
SHOW VARIABLES LIKE "secure_file_priv";
```

Move the CSV to that path and run:
```
sudo cp data/superstore_orders_cleaned.csv /var/lib/mysql-files/
```


```sql
LOAD DATA INFILE '/var/lib/mysql-files/superstore_orders_cleaned.csv'
INTO TABLE orders
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```
![image](https://github.com/user-attachments/assets/b1f84e1d-3e7d-417a-aa85-ac7435a218f2)

---

## 🔍 Step 6: Write Analysis Queries (Save in `sql/analysis_queries.sql`)

### 🔹 Total Sales and Profit

```sql
SELECT SUM(Sales) AS Total_Sales, SUM(Profit) AS Total_Profit FROM orders;
```
![image](https://github.com/user-attachments/assets/9752e144-08ba-4528-87b4-fcdb38081adc)

### 🔹 Top 5 Most Profitable Products

```sql
SELECT Product_Name, SUM(Profit) AS Profit
FROM orders
GROUP BY Product_Name
ORDER BY Profit DESC
LIMIT 5;
```
![image](https://github.com/user-attachments/assets/d0a3b841-248c-46f9-a73e-d17b505fef49)

### 🔹 Monthly Sales Trend

```sql
SELECT DATE_FORMAT(Order_Date, '%Y-%m') AS Month, SUM(Sales) AS Sales
FROM orders
GROUP BY Month
ORDER BY Month;
```
![image](https://github.com/user-attachments/assets/9d94f934-7891-4e53-9f17-167d0dbcfaba)

### 🔹 Segment-wise Revenue

```sql
SELECT Segment, ROUND(SUM(Sales), 2) AS Revenue
FROM orders
GROUP BY Segment
ORDER BY Revenue DESC;
```
![image](https://github.com/user-attachments/assets/23ef838e-4145-4060-9e56-a65305fe1f89)

### 🔹 Discount Impact on Profit

```sql
SELECT Discount, ROUND(AVG(Profit), 2) AS Avg_Profit
FROM orders
GROUP BY Discount
ORDER BY Discount;
```
![image](https://github.com/user-attachments/assets/e863d56e-dd96-4ac4-994e-4022afd71ce6)

---

## 📄 Step 7: README.md Template

````md
# 🛍️ Superstore SQL Analysis

## 🔍 Business Objective
Analyze retail orders to uncover insights on sales performance, top products, and customer segments.

## 🧰 Tools
- MySQL
- CLI
- CSV dataset

## 📊 Key SQL Queries
- Total Sales & Profit
- Top Profitable Products
- Monthly Sales Trend
- Segment Revenue Breakdown
- Discount vs Profit Impact

## 📁 Files
- `data/superstore_orders.csv`: Source data
- `sql/create_table.sql`: Table creation
- `sql/analysis_queries.sql`: Insight queries

## ✅ How to Run
```bash
# Create DB and Table
mysql -u lili -p superstore < sql/create_table.sql

# Load Data from CSV
# Adjust path as per secure_file_priv value
````

```

