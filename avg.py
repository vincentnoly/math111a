import csv

# Initialize variables to store total rating and count of rows
total_rating = 0
row_count = 0

# Open the CSV file
with open("data/rtReadyNoTitle.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Iterate over each row in the CSV file
    for row in reader:
        # Convert 'Mean Rating' to float and add to total rating
        total_rating += float(row['Mean Rating'])
        # Increment row count
        row_count += 1

# Calculate the average rating
average_rating = total_rating / row_count if row_count > 0 else 0

# Print the average rating
print("Average Rating:", average_rating)