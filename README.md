# 📊 Sales Data Pipeline

A simple and efficient pipeline to extract, clean, transform, and store sales data using Python.

## 🛠 Features

- Data ingestion from CSV files  
- Cleaning and preprocessing of raw sales data  
- Basic transformation logic (e.g., date parsing, value formatting)  
- Load cleaned sales into PostgreSQL


## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/freyawillx/sales_data_pipeline.git
   cd sales_data_pipeline
   ```

2. Install requirements

  ```bash
  pip install -r requirements.txt
  ```
3. Run the pipeline

  ```bash 
  python pipeline.py path/to/sales.csv sales
  ```

## ✅ TODO

- Add unit tests
- Add logging
- Export to database (optional)

📄 License
This project is licensed under the MIT License.

See [the local quickstart](docs/guides/local-quickstart.md) for input data, PostgreSQL setup requirements, and rerun precautions.

Browse the [documentation index](docs/README.md) for all existing guides, tools, and analysis examples.
