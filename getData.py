import requests
import json 
import csv
from time import sleep
from tqdm import tqdm 

def get_all_manga(included_tags, excluded_tags, total_titles):
    '''Gets data for manga given tags

    Args:
        included_tags: Tags we want to search for
        excluded_tags: Tags we do not want to search for
        total_titles: To check title count for total limit

    Returns:
        List of manga  
    '''

    base_url = 'https://api.mangadex.org'

    limit = 5
    offset = 0
    max_retries = 10

    if (total_titles > 1000):
        total_titles_limit = 1000
    else:
        total_titles_limit = total_titles

    all_manga = []

    included_tag_ids, excluded_tag_ids = get_tag_ids(included_tags, excluded_tags)

    with tqdm(total=total_titles_limit, desc="Fetching manga", unit=" manga") as pbar:
        while len(all_manga) < total_titles_limit:
            params = {'limit': limit, 'offset': offset, 'includedTags[]': included_tag_ids, 'excludedTags[]': excluded_tag_ids}
            retries = 0

            while retries < max_retries:
                response = requests.get(f'{base_url}/manga', params=params)

                if response.status_code == 200:
                    manga_data = response.json()
                    if not manga_data['data']:
                        break

                    all_manga.extend(manga_data['data'])

                    offset += limit
                    pbar.update(len(manga_data['data']))
                    break
                elif response.status_code == 400:
                    retries += 1
                    print(f"Retrying ({retries}/{max_retries}) after receiving a 400 error.")
                    sleep(1)
                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    break

    print(f'Finished fetching manga: {included_tags}')
    return all_manga[:total_titles_limit]

def get_tag_ids(included_tags, excluded_tags):
    '''Gets the tag ids

    Args:
        included_tags: Included tag names 
        excluded_tags: Excluded tag names 

    Returns:
        Included and exluded tag ids 
    '''

    base_url = 'https://api.mangadex.org'
    tags = requests.get(f"{base_url}/manga/tag").json()

    included_tag_ids = [
        tag["id"]
        for tag in tags["data"]
        if tag["attributes"]["name"]["en"] in included_tags
    ]

    excluded_tag_ids = [
        tag["id"]
        for tag in tags["data"]
        if tag["attributes"]["name"]["en"] in excluded_tags
    ]

    return included_tag_ids, excluded_tag_ids

def get_tag_count(tag_name):
    '''Gets the number of titles in a tag

    Args:
        tag_name: Name of the tag we are searching for 

    Returns:
        Integer value for number of manga that fall within a tag 
    '''

    base_url = 'https://api.mangadex.org'
    tags = requests.get(f"{base_url}/manga/tag").json()

    includedTags=[tag_name]
    included_tag_ids = [
        tag["id"]
        for tag in tags["data"]
        if tag["attributes"]["name"]["en"]
            in includedTags
    ]   

    excludedTags=[]
    excluded_tag_ids = [
        tag["id"]
        for tag in tags["data"]
        if tag["attributes"]["name"]["en"]
            in excludedTags
    ]

    params = {"includedTags[]": included_tag_ids, "excludedTags[]": excluded_tag_ids}

    if bool(included_tag_ids):
        response = requests.get(f"{base_url}/manga", params=params)
        manga_data = response.json()
        if response.status_code == 200:
            return int(manga_data["total"])
        else:
            print(f"Failed to fetch tag count for {tag_name}. Status code: {response.status_code}")
            return None
    else:
        print(f"Tag {tag_name} not found.")
        return None

def get_manga_statistics(manga_id):
    '''Separate request to get statistics

    Args:
        manga_id: ID of manga 

    Returns:
        JSON response with statistics 
    '''

    base_url = 'https://api.mangadex.org'
    response = requests.get(f'{base_url}/statistics/manga/{manga_id}')

    if response.status_code == 200:
        statistics_data = response.json().get('statistics', {}).get(manga_id, {})
        return statistics_data
    else:
        print(f"Failed to fetch manga statistics for Manga ID {manga_id}. Status code: {response.status_code}")
        return {}

def write_to_csv(manga_data, output_csv_path, buffer_size=1000):
    '''Writes manga data to csv file

    Args:
        manga_data: Data to be extracted
        output_csv_path: File to add data to 
        buffer_size: Buffer for writing lines

    Returns:
        Nothing
    '''

    fieldnames = ['Manga ID', 'Title (English)', 'Tags', 'Mean Rating', 'Bayesian Rating', 'Follows', 'Publication Demographic']

    with open(output_csv_path, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write headers only if the file is empty
        if csv_file.tell() == 0:
            writer.writeheader()

        buffer_rows = []

        with tqdm(total=len(manga_data), desc="Processing manga", unit=" manga") as pbar:
            for manga in manga_data:
                manga_id = manga['id']
                title_en = manga['attributes']['title'].get('en', 'N/A')
                tags = ', '.join(str(tag['attributes']['name']) for tag in manga['attributes']['tags'])
                statistics_data = get_manga_statistics(manga_id)
                mean_rating = statistics_data.get('rating', {}).get('average')
                bayesian_rating = statistics_data.get('rating', {}).get('bayesian')
                follows = statistics_data.get('follows', 0)
                demographic = manga['attributes'].get('publicationDemographic')

                buffer_rows.append({
                    'Manga ID': manga_id,
                    'Title (English)': title_en,
                    'Tags': tags,
                    'Mean Rating': mean_rating,
                    'Bayesian Rating': bayesian_rating,
                    'Follows': follows,
                    'Publication Demographic': demographic
                })

                # Check if the buffer is full
                if len(buffer_rows) >= buffer_size:
                    writer.writerows(buffer_rows)
                    buffer_rows = []

                pbar.update(1)
                sleep(0.01) 

            # Write any remaining rows in the buffer
            if buffer_rows:
                writer.writerows(buffer_rows)
    print(f"Data for {len(manga_data)} manga written to {output_csv_path}")

if __name__ == "__main__":
    '''
    Get 1000 titles from a given tag, or as many as possible if less than 1000
    Duplicates are thrown out
    '''
    
    output_csv_path = 'manga.csv'

    dexTags = ["Oneshot", "Thriller", "Award Winning", "Reincarnation", "Sci-Fi", "Time Travel", "Genderswap", "Loli", "Traditional Games", "Official Colored", "Historical", "Monsters", "Action", "Demons", "Psychological", "Ghosts", "Animals", "Long Strip", "Romance", "Ninja", "Comedy", "Mecha", "Anthology", "Boys' Love", "Incest", "Crime", "Survival", "Zombies", "Reverse Harem", "Sports", "Superhero", "Martial Arts", "Fan Colored", "Samurai", "Magical Girls", "Mafia", "Adventure", "Self-Published", "Virtual Reality", "Office Workers", "Video Games", "Post-Apocalyptic", "Sexual Violence", "Crossdressing", "Magic", "Girls' Love", "Harem", "Military", "Wuxia", "Isekai", "4-Koma", "Doujinshi", "Philosophical", "Gore", "Drama", "Medical", "School Life", "Horror", "Fantasy", "Villainess", "Vampires", "Deliquents", "Monster Girls", "Shota", "Police", "Web Comic", "Slice of Life", "Aliens", "Cooking", "Supernatural", "Mystery", "Adaptation", "Music", "Full Color", "Tragedy", "Gyaru"] #76 total 

    for tag in dexTags:
        included_tags = tag
        excluded_tags = []

        if tag in ["Reverse Harem", "Magical Girls"]:
            continue

        # Get existing manga IDs from the file
        existing_manga_ids = set()
        try:
            with open(output_csv_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                existing_manga_ids = {row['Manga ID'] for row in reader}
        except FileNotFoundError:
            pass

        # Get total titles for the tag
        total_titles = get_tag_count(included_tags)
        if total_titles is not None:
            # Get new manga details
            all_manga_details = get_all_manga(included_tags, excluded_tags, total_titles)

            # Remove existing manga IDs from the new data
            new_manga_details = [manga for manga in all_manga_details if manga['id'] not in existing_manga_ids]

            # Append new manga details to the CSV file using buffered writing
            write_to_csv(new_manga_details, output_csv_path)