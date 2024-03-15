import csv

# Define input and output file paths
input_csv_path = 'rtReadyNoTitle.csv'
output_csv_path = 'longStrip.csv'

# Define the condition columns and their corresponding values for filtering
condition_columns = ['Long Strip']
condition_values = ['1']  # Condition values corresponding to each column

# Open input and output CSV files
with open(input_csv_path, 'r', newline='') as input_file, \
     open(output_csv_path, 'w', newline='') as output_file:
    # Create CSV reader and writer objects
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)

    # Write header to output file
    header = next(csv_reader)
    csv_writer.writerow(header)

    # Iterate over rows in the input CSV file
    for row in csv_reader:
        # Check if all condition columns satisfy their corresponding condition values
        if all(row[header.index(col)] == val for col, val in zip(condition_columns, condition_values)):
            # If all conditions are met, write the row to the output CSV file
            csv_writer.writerow(row)