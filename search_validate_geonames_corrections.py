import csv
import argparse
import requests
from thefuzz import fuzz


def parse_args():
    parser = argparse.ArgumentParser(
        description="Enhance CSV with Geonames data.")
    parser.add_argument("-i", "--input_csv", help="Path to the input CSV file")
    parser.add_argument("-o", "--output_csv",
                        help="Path to the output CSV file")
    parser.add_argument("-u", "--geonames_user", help="Geonames API key")
    return parser.parse_args()


def read_csv(file_path):
    with open(file_path, mode='r+', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def query_ror(ror_id):
    url = f"https://api.ror.org/organizations/{ror_id}"
    response = requests.get(url)
    if response.status_code == 200:
        record = response.json()
        try:
            geonames_id = record['addresses'][0]['geonames_city']['id']
            geonames_city = record['addresses'][0]['geonames_city']['city']
            return geonames_id, geonames_city
        except (IndexError, KeyError):
            return None
    return None


def query_geonames(city, user):
    url = f"http://api.geonames.org/searchJSON?q={city}&maxRows=10&username={user}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        best_match_id = None
        best_match_name = None
        highest_score = 0
        for geoname in data['geonames']:
            if geoname['name'] == city:
                return geoname['geonameId'], geoname['name']
            else:
                score = fuzz.ratio(city.lower(), geoname['name'].lower())
                if score > highest_score:
                    highest_score = score
                    best_match_id = geoname['geonameId']
                    best_match_name = geoname['name']
        return best_match_id, best_match_name
    return None, None


def main():
    args = parse_args()
    rows = read_csv(args.input_csv)
    header = ['ror_id', 'city', 'ror_geonames_id', 'ror_geonames_name', 'city_corrected',
              'city_corrected_geonames_id', 'city_corrected_geonames_name']
    with open(args.output_csv, mode='w', encoding='utf-8') as file:
        writer = None
        for row in rows:
            row['ror_geonames_id'], row['ror_geonames_name'] = query_ror(
                row['ror_id'])
            row['city_corrected_geonames_id'], row['city_corrected_geonames_name'] = query_geonames(
                row['city_corrected'], args.geonames_user)
            if writer is None:
                writer = csv.writer(file)
                writer.writerow(header)
            writer.writerow([row[field] for field in header])


if __name__ == "__main__":
    main()
