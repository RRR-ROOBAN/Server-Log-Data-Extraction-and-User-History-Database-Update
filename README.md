
## Problem Statement
The project involves extracting server log data from a raw text file, extracting relevant information like email addresses and timestamps, and storing this data in a MongoDB database. This data is then transferred to a MySQL database for further analysis, where several SQL queries are executed to generate insights, such as the number of logs per email, daily log counts, and more.

## Tools Used
- **Python**: The core programming language for extracting, processing, and analyzing the data.
- **Pandas**: For handling data manipulation and transformation.
- **Regex**: For pattern matching and extracting relevant fields like email addresses and timestamps from the raw log data.
- **MongoDB**: For storing the extracted data in a NoSQL database.
- **MySQL**: For performing structured queries on the processed data to gain insights.
- **Streamlit**: For building an interactive web interface to display the analysis results.
- **SQLAlchemy**: For interacting with MySQL through Python.

## Approach

1. **Log Data Extraction**:
   - Read the raw log file.
   - Use regular expressions to extract email addresses and timestamps from each log entry.

2. **Data Transformation**:
   - Convert the extracted timestamps into a consistent format using Python's `datetime` module.
   - Create a dictionary to store the extracted email addresses and formatted timestamps.

3. **Data Storage in MongoDB**:
   - Store the extracted data into MongoDB for persistence.
   - Use `pymongo` to connect and insert the data.

4. **Data Transfer to MySQL**:
   - Convert the MongoDB data into a Pandas DataFrame.
   - Upload the DataFrame into MySQL using `SQLAlchemy`.

5. **Data Analysis**:
   - Perform various SQL queries to gain insights such as:
     - Count of logs per email.
     - Top emails with the most logs.
     - Daily log counts.
     - Email addresses with logs across multiple distinct days.

6. **Presentation**:
   - Display the analysis results using **Streamlit** as a user-friendly web interface.

## Insights Found
- Insights from SQL queries, such as:
  - The number of logs per email.
  - The top three email addresses with the most logs.
  - Count of logs for each email address grouped by the hour of the day.
  - Day with the highest number of logs.
  - The earliest and latest logs for each email address.

## How to Run
1. Clone the repository.
2. Install the necessary dependencies:
3. Set up MongoDB and MySQL credentials in the `credentials.py` file.
4. Run the Streamlit app:
5. The results will be displayed on the Streamlit interface.
