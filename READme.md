# CSV Data Cleaning Tool

> ⚡ Quick Start: Clone the repo and run `python main.py input_file.csv output_file.csv --help` to see all available options and get started immediately.

## Overview
Real-world CSV datasets are often messy, duplicated, or contain missing values, which can make data analysis difficult.  
This Python-based tool automates the cleaning process to improve data quality and usability.  

With this tool, you can:  
- Remove duplicate rows (optionally based on specific columns)  
- Fill missing numeric or text values with flexible strategies  
- Smooth numeric data using a moving average  
- Generate a cleaning summary for quick auditing  

---

## Features
- **Duplicate Removal:** Automatically detect and remove duplicates; optionally based on selected columns.  
- **Flexible Missing Value Handling:**  
  - Numeric columns: mean, median, zero, or custom value  
  - Text columns: mode, “Unknown”, or custom value  
- **Optional Numeric Smoothing:** Smooth numeric data using a configurable moving average window.  
- **Command-Line Interface (CLI):** Run the tool easily from the terminal with configurable options.  
- **Logging & Reporting:** Summary of duplicates removed, missing values filled, and columns smoothed.  
- **Built with Python Built-ins:** No external libraries required.  

---

## Installation
1. Clone the repository:
```bash
git clone <your-repo-url>