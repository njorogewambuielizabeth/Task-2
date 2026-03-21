import csv
import requests

def check_url_status(file_path):
    """
    Reads URLs from a CSV file and prints their HTTP status codes.
    The CSV is expected to have a header 'urls'.
    """
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
            # Use DictReader to handle header
            reader = csv.DictReader(csvfile)
            
            # If the CSV doesn't have a header 'urls', 
            # we check if 'urls' is among the fieldnames.
            if reader.fieldnames and 'urls' not in reader.fieldnames:
                print(f"Error: Header 'urls' not found in {file_path}. Fieldnames: {reader.fieldnames}")
                return

            for row in reader:
                url = row['urls'].strip()
                if not url:
                    continue
                
                try:
                    # Send a HEAD request for efficiency
                    # Some servers might block HEAD, so we can fall back to GET if needed,
                    # but for this task, HEAD is usually preferred for status checks.
                    # We add a timeout to prevent hanging.
                    response = requests.head(url, timeout=10, allow_redirects=True)
                    print(f"({response.status_code}) {url}")
                except requests.exceptions.RequestException as e:
                    # In case of connection errors or timeouts
                    print(f"(Error) {url}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

import sys

if __name__ == "__main__":
    # Path to the input CSV file can be passed as an argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "Task 2 - Intern.csv"
    
    check_url_status(input_file)
