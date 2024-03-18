import os
import pandas as pd
import logging
from datetime import datetime, timedelta
from csv_diff import load_csv, compare
import json
import time 

# Configure logging
logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compare_csv_files(path1, path2):
    try:
        diff = compare(load_csv(open(path1), key="INDICATOR"), load_csv(open(path2), key="INDICATOR"))
        return diff
    except Exception as e:
        logging.error(f"Error comparing CSV files: {e}")
        raise

def save_diff_to_json(diff_output, filename):
    try:
        with open(filename, 'w') as json_file:
            json.dump(diff_output, json_file, indent=4)
        logging.info(f"Differences saved to {filename}")

    except Exception as e:
        logging.error(f"Error saving differences to JSON file: {e}")
        raise

def read_csv(filename):
    try:
        df = pd.read_csv(filename, low_memory=False)
        data = df.to_dict(orient='records')
        header = list(df.columns)
        return header, data
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise

def write_differences(differences, filename):
    try:
        df = pd.DataFrame(differences)
        df.to_csv(filename, index=False)
        logging.info(f"Differences saved to {filename}")

    except Exception as e:
        logging.error(f"Error writing differences to CSV file: {e}")
        raise

def main():
    try:
        start_time = time.time()
        today = datetime.now()
        today_date = today.strftime('%d_%m_%Y')
        cwd = os.getcwd()
        today_path_folder = os.path.join(cwd, 'files', today_date)
        yesterday = today - timedelta(days=1)
        yesterday_date = yesterday.strftime('%d_%m_%Y')
        yesterday_path_folder = os.path.join(cwd, 'files', yesterday_date)

        files_today = os.listdir(today_path_folder)
        files_yesterday = os.listdir(yesterday_path_folder)
        yesterday_path = os.path.join(cwd, 'files', yesterday_date, files_yesterday[0])
        today_path = os.path.join(cwd, 'files', today_date, files_today[0])

        print(f'Program running for files {yesterday_date} & {today_date}.')

        diff_output = compare_csv_files(today_path, yesterday_path)
        delta_filename = f"deltalogs_{today_date}.json"
        logs_save_path = os.path.join(cwd, 'delta', f'{delta_filename}.json')
        save_diff_to_json(diff_output, logs_save_path) 
        
        end_time = time.time()
        execution_time = end_time - start_time

        print(f'Change tracking files created between files {today_date} & {yesterday_date} with speed of {execution_time:.2f} seconds')

        file_1_header, file_1_data = read_csv(yesterday_path)
        file_2_header, file_2_data = read_csv(today_path)

        differences = []

        for row in file_2_data:
            if row not in file_1_data:
                differences.append(row)

        filename = os.path.join(cwd, 'delta', f'Delta_{today_date}.csv')
        write_differences(differences, filename)
        end_time = time.time()
        execution_time = end_time - start_time

        print(f'Delta files created between files {today_date} & {yesterday_date} with speed of {execution_time:.2f} seconds')

        print('Program Ended Successfully')

        logging.info("Script execution completed successfully")
    
    except Exception as e:
        print('Program failed, check log files to identify the issue. ')
        logging.error(f"Error in main function: {e}")
        

if __name__ == "__main__":
    main()
