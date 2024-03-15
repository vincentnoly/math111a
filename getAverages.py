import csv

csv_file = 'longStrip.csv'
output_file = 'longStripAVG.csv'

dexTags = ["Oneshot", "Thriller", "Award Winning", "Reincarnation", "Sci-Fi", "Time Travel", "Genderswap", "Loli", "Traditional Games", "Official Colored", "Historical", "Monsters", "Action", "Demons", "Psychological", "Ghosts", "Animals", "Long Strip", "Romance", "Ninja", "Comedy", "Mecha", "Anthology", "Boys' Love", "Incest", "Crime", "Survival", "Zombies", "Reverse Harem", "Sports", "Superhero", "Martial Arts", "Fan Colored", "Samurai", "Magical Girls", "Mafia", "Adventure", "Self-Published", "Virtual Reality", "Office Workers", "Video Games", "Post-Apocalyptic", "Sexual Violence", "Crossdressing", "Magic", "Girls' Love", "Harem", "Military", "Wuxia", "Isekai", "4-Koma", "Doujinshi", "Philosophical", "Gore", "Drama", "Medical", "School Life", "Horror", "Fantasy", "Villainess", "Vampires", "Delinquents", "Monster Girls", "Shota", "Police", "Web Comic", "Slice of Life", "Aliens", "Cooking", "Supernatural", "Mystery", "Adaptation", "Music", "Full Color", "Tragedy", "Gyaru","shounen", "seinen", "shoujo", "josei"]

# Create and open the output CSV file for writing
with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
    writer = csv.writer(output_csv)

    # Write the header row
    writer.writerow(['Tag', 'Number of Manga', 'Average Follows', 'Average Rating'])

    # Iterate over each tag
    for tag_to_count in dexTags:
        count = 0
        total = 0
        follows = 0

        # Open the input CSV file and read the rows
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if the tag value is 1 (true)
                if int(row[tag_to_count]):
                    count += 1
                    if 'Mean Rating' in row:
                        total += float(row['Mean Rating'])
                    if 'Follows' in row:
                        follows += float(row['Follows'])

        # Calculate the average rating
        average = total / count if count > 0 else 0
        avg_follows = follows / count if count > 0 else 0

        # Write the tag, number of manga, and average rating to the output CSV file
        writer.writerow([tag_to_count, count, avg_follows, average])

print(f"Results have been written to '{output_file}'.")