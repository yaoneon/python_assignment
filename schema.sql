CREATE TABLE IF NOT EXISTS financial_data (
  symbol VARCHAR(255),
  date DATE,
  open_price FLOAT(10),
  close_price FLOAT(10),
  volume FLOAT(10),
  PRIMARY KEY (symbol, date)
);