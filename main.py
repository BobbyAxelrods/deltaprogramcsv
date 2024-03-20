import os
import pandas as pd
import logging
from datetime import datetime, timedelta
from csv_diff import load_csv, compare
import json
import time 
import configparser

# Configure logging
logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_val(file_path):
    properties = {}
    config = configparser.ConfigParser()
    config.read(file_path)
    for x in config.sections():
        for key,value in config.items(x):
            properties[key]=value.strip()
        return properties

def compare_csv_files(path1, path2):
    try:
        diff = compare(load_csv(open(path1), key="col1"), load_csv(open(path2), key="col1"))
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
        properties_path = 'val.properties'

        #time tracking 
        start_time = time.time()

        # date for naming 
        today = datetime.now()
        today_date = today.strftime('%d_%m_%Y')
        yesterday = today - timedelta(days=1)
        yesterday_date = yesterday.strftime('%d_%m_%Y')

        # properties value management 
        properties = parse_val(properties_path)
        path1=properties.get('today_files_path')
        path2=properties.get('yesterday_files_path')
        delta_path=properties.get('delta_files_path')
        filename_path1 = os.listdir(path1)[0]
        filename_path2 = os.listdir(path2)[0]
        today_path = path1+'\\'+filename_path1
        yesterday_path =  path2+'\\'+filename_path2
        delta_filename = delta_path+'\\'+today_date+'.json'


        # Comparison process function
        diff_output = compare_csv_files(today_path, yesterday_path)
        print(f'Program running for files {filename_path1} & {filename_path1}.')

        # Savings change tracking 
        save_diff_to_json(diff_output, delta_filename) 
        
        #time tracking 
        end_time = time.time()
        execution_time = end_time - start_time

        print(f'Change tracking files created between files {today_date} & {yesterday_date} with speed of {execution_time:.2f} seconds')

        # file reading process function 
        file_1_header, file_1_data = read_csv(today_path)
        file_2_header, file_2_data = read_csv(yesterday_path)
        differences = []

        # Looping overall row and saving delta
        for row in file_2_data:
            if row not in file_1_data:
                differences.append(row)

        # Saving Delta 
        filename = os.path.join(delta_path, f'Delta_{today_date}.csv')
        write_differences(differences, filename)
        end_time = time.time()
        execution_time = end_time - start_time

        print(f'Delta files created between files {filename_path1} & {filename_path2} with speed of {execution_time:.2f} seconds')

        print('Program Ended Successfully')

        logging.info("Script execution completed successfully")
    
    except Exception as e:
        print('Program failed, check log files to identify the issue. ')
        logging.error(f"Error in main function: {e}")
        

if __name__ == "__main__":
    main()
