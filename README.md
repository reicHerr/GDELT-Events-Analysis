**Analysis of Events in Benin using GDELT Data**

## Project Description

This project extracts and analyzes data from the [GDELT database](https://www.gdeltproject.org/), focusing on events and media mentions related to Benin. The analysis includes theme identification using Azure OpenAI, sentiment analysis, and visualization of temporal and geographical trends. The project is structured into three main steps: dataset selection, data extraction to a local SQLite database, and data analysis.

## Table of Contents

- [Project Description](#project-description)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [Setting up Google Cloud Credentials](#setting-up-google-cloud-credentials)
  - [Setting up Azure OpenAI Credentials](#setting-up-azure-openai-credentials)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributor](#contributor)
- [License](#license)

## Installation

To run this project, you need to have Python installed (version 3.8 or higher recommended). You also need to install the following libraries:

- `google-cloud-bigquery`
- `google-cloud-bigquery-storage`
- `pandas`
- `pyarrow`
- `db-dtypes`
- `openai` (for Azure OpenAI)
- `dash`
- `plotly`
- `numpy`
- `matplotlib`
- `seaborn`

You can install these libraries using pip:

```bash
pip install google-cloud-bigquery google-cloud-bigquery-storage pandas pyarrow db-dtypes openai dash plotly numpy matplotlib seaborn
```

**Note**: The `sqlite3` library is usually included with Python, so no additional installation is needed.

You also need to set up credentials for Google Cloud and Azure OpenAI.

### Setting up Google Cloud Credentials

1. Create a service account key in the [Google Cloud Console](https://console.cloud.google.com).
2. Download the JSON key file.
3. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable with the path to the JSON key file.

Run the following command:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service_account_key.json"
```

### Setting up Azure OpenAI Credentials

1. Obtain an API key from Azure OpenAI.
2. Set the `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` environment variables.

Run the following commands:

```bash
export AZURE_OPENAI_API_KEY="your_api_key"
export AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint"
```

## Usage

To run this project, follow these steps:

1. **Dataset Selection**

   Open and run `dataset_select.ipynb`. This notebook explores the GDELT database and selects the relevant datasets and tables for extraction, focusing on events and mentions related to Benin.

2. **Data Extraction**

   Open and run `data_extract_to_db.ipynb`. This notebook extracts the selected data from BigQuery, cleans it, and stores it in a local SQLite database.

   **Note**: Running this notebook may incur costs on Google Cloud, depending on the amount of data extracted.

3. **Data Analysis**

   Open and run `data_analyse.ipynb`. This notebook performs analysis on the extracted data, including:

   - Identifying themes for each event using Azure OpenAI.
   - Performing sentiment analysis, classifying events as positive, neutral, or negative.
   - Visualizing temporal trends, geographical distribution, and main themes.
   - Creating an interactive dashboard with Dash for in-depth exploration.

   **Note**: Using Azure OpenAI may incur costs depending on the number of API calls.

   The analysis notebook also includes code to create an interactive dashboard. To view the dashboard, run the notebook and follow the instructions provided.

## Project Structure

The project is structured as follows:

- `call_openai.py`: Utility function to call the Azure OpenAI API for tasks like theme identification.
- `setup_authentication.py`: Function to set up Google Cloud authentication.
- `get_latest_file.py`: Function to get the latest file based on a keyword and extension.
- `initialize_client.py`: Function to initialize a BigQuery client.
- `extract_table.py`: Function to extract data from BigQuery and save it as CSV.
- `data_analyse.ipynb`: Notebook for data analysis, including theme identification, sentiment analysis, and creating an interactive dashboard.
- `data_extract_to_db.ipynb`: Notebook for data extraction from BigQuery, cleaning, and storing in SQLite.
- `dataset_select.ipynb`: Notebook for selecting relevant GDELT datasets and tables.

Additionally, running the notebooks will generate output files in the `data` directory, including:

- CSV files for raw and cleaned data.
- A SQLite database (`gdelt_benin.db`) containing the extracted data.

## Contributor

- [reicHerr](https://github.com/reicHerr)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

**Citations**:
- The project uses data from the GDELT database, a comprehensive repository of global events and media coverage.
- The analysis relies on Azure OpenAI for theme identification and sentiment analysis.