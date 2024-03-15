import csv
import json

dexTags = ["Oneshot", "Thriller", "Award Winning", "Reincarnation", "Sci-Fi", "Time Travel", "Genderswap", "Loli", "Traditional Games", "Official Colored", "Historical", "Monsters", "Action", "Demons", "Psychological", "Ghosts", "Animals", "Long Strip", "Romance", "Ninja", "Comedy", "Mecha", "Anthology", "Boys' Love", "Incest", "Crime", "Survival", "Zombies", "Reverse Harem", "Sports", "Superhero", "Martial Arts", "Fan Colored", "Samurai", "Magical Girls", "Mafia", "Adventure", "Self-Published", "Virtual Reality", "Office Workers", "Video Games", "Post-Apocalyptic", "Sexual Violence", "Crossdressing", "Magic", "Girls' Love", "Harem", "Military", "Wuxia", "Isekai", "4-Koma", "Doujinshi", "Philosophical", "Gore", "Drama", "Medical", "School Life", "Horror", "Fantasy", "Villainess", "Vampires", 'Delinquents', "Monster Girls", "Shota", "Police", "Web Comic", "Slice of Life", "Aliens", "Cooking", "Supernatural", "Mystery", "Adaptation", "Music", "Full Color", "Tragedy", "Gyaru"]

demographics = ["shounen", "seinen", "shoujo", "josei"]

input_csv_path = 'manga.csv'
output_csv_path = 'rtReadyNoTitle.csv'

def process_line(line):
    manga_id, title, Tags, mean_rating, bayesian_rating, follows, demographic = line

    # Check if mean_rating is empty
    if mean_rating.strip() == '':
        return None  # Skip this line

    # Skip if follows is not a number or less than 50
    if not follows.isdigit() or int(follows) < 100:
        return None

    try:
        # Parse the tags_str into a list of dictionaries using eval
        tags_list = eval(Tags)

        # Extract 'en' values from the dictionaries
        tags = [tag['en'] for tag in tags_list if isinstance(tag, dict) and 'en' in tag]

        # Create a dictionary to store whether each dexTag is present
        tag_presence = {tag: int(tag in tags) for tag in dexTags}

        # Create dummy variables for demographics
        demographic_variables = {d: int(d == demographic) for d in demographics}
    except (NameError, TypeError, SyntaxError) as e:
        # Handle the case where tags_str is not in the expected format
        print(f"Error processing line: {e}")
        tags = []
        tag_presence = {tag: 0 for tag in dexTags}
        demographic_variables = {d: 0 for d in demographics}

    return [mean_rating, follows] + [tag_presence[tag] for tag in dexTags] + [demographic_variables[d] for d in demographics]

with open(input_csv_path, 'r', newline='', encoding='utf-8') as input_csv:
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_csv:
        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)

        # Write header
        header = ["Mean Rating", "Follows"] + dexTags + demographics
        writer.writerow(header)

        for line in reader:
            processed_line = process_line(line)
            if processed_line is not None:
                writer.writerow(processed_line)