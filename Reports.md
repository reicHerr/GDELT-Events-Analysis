# Detailed Report

## Context and Project Objective

This project aims to extract, structure, and analyze data from the GDELT database (Global Database of Events, Language, and Tone) specific to Benin. GDELT is a global database that records daily media events, detailing interactions between actors (countries, groups, individuals), locations, media tones, and types of events. The project focuses on events and media mentions related to Benin, with in-depth analysis of themes, sentiments, and temporal and geographical trends. It uses tools such as Google BigQuery for extraction, SQLite for storage, and Azure OpenAI for text analysis.

The project is structured into three main steps, each documented in a Jupyter notebook:
1. **Dataset Selection** (`dataset_select.ipynb`): Exploration and selection of relevant datasets and tables in GDELT.
2. **Data Extraction** (`data_extract_to_db.ipynb`): Extraction of data via BigQuery, cleaning, and storage in an SQLite database.
3. **Data Analysis** (`data_analyse.ipynb`): Analysis of the extracted data, including theme identification, sentiment analysis, and creation of an interactive dashboard.

The Python files (`.py`) contain utility functions that support these steps, such as initializing BigQuery clients, calling the Azure OpenAI API, and managing files.

## Step 1: Dataset Selection

The `dataset_select.ipynb` notebook explores the GDELT database to identify relevant datasets and tables for the project. Here are the key steps:
- **Database Exploration**: Use of the Google BigQuery client to understand GDELT's structure.
- **Dataset Identification**: Eight datasets are initially found in the "gdelt-bq" project, with a preselection of five datasets ("extra", "full", "gdeltv2", "gdeltv2_ngrams", "sample_views"). The "full" and "gdeltv2" datasets are finally selected for their relevance.
- **Table Consultation**: Analysis of tables in the selected datasets, for example, "full" contains three tables, and "gdeltv2" contains 62, including `events_partitioned` and `eventmentions_partitioned`.
- **Table Selection**: Two tables are chosen from "gdeltv2":
  - `events_partitioned`: Contains detailed information on global events, such as dates and types of events.
  - `eventmentions_partitioned`: Lists media mentions associated with each event, allowing analysis of media coverage.

This step ensures that the selected data is relevant to the project's analysis objectives.

## Step 2: Data Extraction

The `data_extract_to_db.ipynb` notebook extracts data from the selected tables and stores it in an SQLite database. Here is the detailed process:
- **Data Extraction**:
  - Data specific to Benin is extracted via BigQuery with SQL queries filtering by country codes ('BN' and 'BEN').
  - Necessary libraries (`google-cloud-bigquery`, `pandas`, etc.) are used, and authentication is configured with Google Cloud credentials.
  - The data is saved as CSV files in a directory (e.g., `data/extract_data`).
- **Data Cleaning**:
  - CSV files are loaded into pandas DataFrames.
  - Missing values are handled (rows with NaN are dropped), and duplicates are removed.
  - Cleaned data is saved in another directory (e.g., `data/cleaned_data`).
- **Data Formatting**:
  - Date fields (such as `SQLDATE` and `MentionTimeDate`) are standardized (e.g., YYYY-MM-DD).
  - Formatted files are saved with a "_treated" suffix.
- **Storage in the Database**:
  - An SQLite database (`gdelt_benin.db`) is created with two tables: `events` and `mentions`.
  - Tables are designed with primary and foreign keys (e.g., `GLOBALEVENTID` links the tables).
  - SQLite optimizations (disabling journaling, synchronous mode) are applied to improve performance.
  - Formatted CSV files are loaded into the SQLite tables, with indexes created on key columns to optimize queries.

This step ensures that the data is ready for quick and efficient analysis.

## Step 3: Data Analysis

The `data_analyse.ipynb` notebook performs in-depth analysis of the stored data. Here are the main analyses and results:
- **Theme Identification**:
  - Azure OpenAI is used to identify themes of articles in the `events` table by extracting content from URLs and assigning themes such as "POLITICS", "CRIME", or "SOCIAL CRISIS".
  - Themes are inferred from tone and location if content is inaccessible.
- **Data Exploration**:
  - The `events` and `mentions` tables are explored, with columns such as `GLOBALEVENTID`, `SQLDATE`, `GoldsteinScale`, `AvgTone`, and `MentionSourceName`.
  - Descriptive statistics (mean, standard deviation, etc.) are calculated for numerical columns.
- **Temporal Analysis**:
  - The frequency of events and mentions is analyzed monthly, with line graphs showing trends.
  - Metrics like `GoldsteinScale` and `AvgTone` are tracked to identify seasonal variations.
- **Sentiment Analysis**:
  - Distributions of `AvgTone` (events) and `MentionDocTone` (mentions) are compared via histograms.
  - Azure OpenAI classifies sentiments as "Positive", "Neutral", or "Negative", with explanations considering context.
- **Geographical Analysis**:
  - Events are mapped with `ActionGeo_Lat` and `ActionGeo_Long`, using scatter plots to show locations, sizes (based on `NumMentions`), and colors (based on `AvgTone`).
- **Main Themes**:
  - The most frequent themes include "POLITICS", "CRIME", and "SOCIAL CRISIS", with average tones varying (e.g., "CRIME": -4.85, "TRADITIONAL CULTURE": 5.84).
- **Interactive Dashboard**:
  - A dashboard based on Dash allows filtering data by date, themes, and mention sources, with visualizations such as geographical maps and metric tables.

**Key Results**:
- Dominant themes include "POLITICS" and "CRIME", with sentiments varying over time.
- Temporal trends show peaks in events at certain periods.
- Events are concentrated in specific areas of Benin, with sentiment variations by region.
- Some events lack defined themes, indicating potential data gaps.

## Utility Functions

The Python files support the notebooks with specific functionalities:
- **`call_openai.py`**: Calls the Azure OpenAI API to analyze prompts, used for theme identification.
- **`setup_authentication.py`**: Configures Google Cloud authentication with a service account key.
- **`get_latest_file.py`**: Retrieves the most recent file in a directory based on a keyword and extension.
- **`initialize_client.py`**: Initializes a BigQuery client for queries.
- **`extract_table.py`**: Extracts data from BigQuery and saves it as CSV.

## Project Structure

The following table summarizes the files and their roles:

| File                       | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| `call_openai.py`            | Function to call the Azure OpenAI API for text analysis.                    |
| `setup_authentication.py`   | Configures Google Cloud authentication.                                     |
| `get_latest_file.py`        | Retrieves the most recent file based on a keyword and extension.            |
| `initialize_client.py`      | Initializes a BigQuery client.                                              |
| `extract_table.py`          | Extracts data from BigQuery and saves it as CSV.                            |
| `dataset_select.ipynb`      | Explores and selects relevant GDELT datasets.                               |
| `data_extract_to_db.ipynb`  | Extracts, cleans, and stores data in an SQLite database.                    |
| `data_analyse.ipynb`        | Analyzes data, identifies themes, and creates a dashboard.                  |

The notebooks also generate output files in the `data` directory, including CSV files and an SQLite database (`gdelt_benin.db`).

## Installation and Dependencies

To run the project, install the following dependencies with pip:

```bash
pip install google-cloud-bigquery google-cloud-bigquery-storage pandas pyarrow db-dtypes openai dash plotly numpy matplotlib seaborn
```

Google Cloud and Azure OpenAI credentials must be configured as described in the README. Note that data extraction may incur costs on Google Cloud, and using Azure OpenAI may also incur fees.

## Usage

Run the notebooks in the following order:
1. `dataset_select.ipynb`: Selects the tables `events_partitioned` and `eventmentions_partitioned`.
2. `data_extract_to_db.ipynb`: Extracts data, cleans it, and stores it in `gdelt_benin.db`.
3. `data_analyse.ipynb`: Analyzes data and generates an interactive dashboard.

The Dash dashboard allows interactive exploration of data with filters by date, themes, and sources.

## Considerations

- **Costs**: Extraction via BigQuery and calls to Azure OpenAI can incur costs. Check billing limits in Google Cloud and Azure.
- **Sensitive Data**: GDELT data includes information about media events. Handle it responsibly.
- **License**: See [LICENSE.md](LICENSE.md) file.

## Conclusion

This project provides a comprehensive analysis of events and media mentions in Benin from GDELT data. By combining tools like BigQuery, SQLite, Azure OpenAI, and Dash, it offers valuable insights into themes, sentiments, and trends. The generated README guides users through installation, usage, and understanding of the project structure, making the code accessible and reproducible.

### Key Citations

- [Google Cloud Console for creating service account keys](https://console.cloud.google.com)