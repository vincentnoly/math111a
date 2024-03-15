import csv

# Input and output file paths
input_file = 'tag_counts_and_averages.csv'
output_file = 'tag_counts_and_averages_sort_rating.csv'

# Read the data from the input CSV file and store it in a list
data = []
with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row)

# Sort the data based on a specific column (e.g., column index 0)
sorted_data = sorted(data, key=lambda x: x[3])  # Sort based on the first column

# Write the sorted data to a new CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for row in sorted_data:
        writer.writerow(row)

print("CSV file has been sorted and saved to", output_file)