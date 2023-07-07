import pandas as pd
import os.path
import locale
import json
from region_helper import *
from html_generator import *
from csv_generator import *

locale.setlocale(locale.LC_ALL, '')

petition_download_link = ""
petition_id = 0

while petition_id == 0 or petition_id.strip() == "":
    petition_id = input("Petition ID: ")

    if petition_id == 0 or petition_id == "":
        print("Invalid petition ID")

petition_download_link = f"https://petition.parliament.uk/petitions/{str(petition_id)}.json"

df = pd.read_json(petition_download_link)

df.fillna(0)

# Output dir
output_directory = "./output"
if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

instance_directory = output_directory + "/" + str(df.get("data").get("id"))
if not os.path.isdir(instance_directory):
    os.mkdir(instance_directory)

## Signatures by country
signatures_by_country = pd.DataFrame(df.get("data").get("attributes").get("signatures_by_country"))
generate_csv(signatures_by_country, instance_directory, "signatures_by_country.csv")

# Analysis
total_signatures_outside_uk = 0
total_region_africa = 0
total_region_asia = 0
total_region_carribean = 0
total_region_central_america = 0
total_region_europe = 0
total_region_north_america = 0
total_region_oceania = 0
total_region_south_america = 0
total_region_unknown = 0

# Loop through the signatures, drop them into buckets depending on region
for index, row in signatures_by_country.iterrows():
    if row.get("name") != "United Kingdom":
        total_signatures_outside_uk += row.get("signature_count")

    if row.get("name") in africa_region:
        total_region_africa += row.get("signature_count")
    elif row.get("name") in asia_region:
        total_region_asia += row.get("signature_count")
    elif row.get("name") in carribean_region:
        total_region_carribean += row.get("signature_count")
    elif row.get("name") in central_america_region:
        total_region_central_america += row.get("signature_count")
    elif row.get("name") in europe_region:
        total_region_europe += row.get("signature_count")
    elif row.get("name") in north_america_region:
        total_region_north_america += row.get("signature_count")
    elif row.get("name") in oceania_region:
        total_region_oceania += row.get("signature_count")
    elif row.get("name") in south_america_region:
        total_region_south_america += row.get("signature_count")
    else:
        total_region_unknown += row.get("signature_count")

# Cleanup
del signatures_by_country

## Signatures by constituency
signatures_by_constituency = pd.DataFrame(df.get("data").get("attributes").get("signatures_by_constituency"))
generate_csv(signatures_by_constituency, instance_directory, "signatures_by_constituency.csv")

del signatures_by_constituency

# Signatures by region
signatures_by_region = pd.DataFrame(df.get("data").get("attributes").get("signatures_by_region"))
generate_csv(signatures_by_region, instance_directory, "signatures_by_region.csv")

# Analysis
total_signatures_england = 0
total_signatures_scotland = 0
total_signatures_wales = 0
total_signatures_ni = 0

for index, row in signatures_by_region.iterrows():
    if row.get("name") in england_regions:
        total_signatures_england += row.get("signature_count")
    elif row.get("name") == "Scotland":
        total_signatures_scotland += row.get("signature_count")
    elif row.get("name") == "Wales":
        total_signatures_wales += row.get("signature_count")
    elif row.get("name") == "Northern Ireland":
        total_signatures_ni += row.get("signature_count")

# Cleanup
del signatures_by_region

total_signatures = df.get("data").get("attributes").get("signature_count")

data_dump = {
    "total_signatures": total_signatures,
    "totals": {
        "inside_uk": total_signatures - total_signatures_outside_uk,
        "inside_uk_percent": round(((total_signatures - total_signatures_outside_uk) / total_signatures) * 100, 2),
        "outside_uk": total_signatures_outside_uk,
        "outside_uk_percent": round((total_signatures_outside_uk / total_signatures) * 100, 2),
        "uk": {
            "england": total_signatures_england,
            "england_percent": round((total_signatures_england / total_signatures) * 100, 2),
            "scotland": total_signatures_scotland,
            "scotland_percent": round((total_signatures_scotland / total_signatures) * 100, 2),
            "wales": total_signatures_wales,
            "wales_percent": round((total_signatures_wales / total_signatures) * 100, 2),
            "ni": total_signatures_ni,
            "ni_percent": round((total_signatures_ni / total_signatures) * 100, 2),
        },
        "global": {
            "africa": total_region_africa,
            "africa_percent": round((total_region_africa / total_signatures) * 100, 2),
            "asia": total_region_asia,
            "asia_percent": round((total_region_asia / total_signatures) * 100, 2),
            "carribean": total_region_carribean,
            "carribean_percent": round((total_region_carribean / total_signatures) * 100, 2),
            "central_america": total_region_central_america,
            "central_america_percent": round((total_region_central_america / total_signatures) * 100, 2),
            "europe": total_region_europe,
            "europe_percent": round((total_region_europe / total_signatures) * 100, 2),
            "north_america": total_region_north_america,
            "north_america_percent": round((total_region_north_america / total_signatures) * 100, 2),
            "oceania": total_region_oceania,
            "oceania_percent": round((total_region_oceania / total_signatures) * 100, 2),
            "south_america": total_region_south_america,
            "south_america_percent": round((total_region_south_america / total_signatures) * 100, 2),
            "unknown": total_region_unknown,
            "unknown_percent": round((total_region_unknown / total_signatures) * 100, 2),
        }
    }
}

with open(instance_directory + "/data_dump.json", "w") as data_dump_file:
    json.dump(data_dump, data_dump_file, indent=4)

data_dump_file.close()

# Generate HTML report using all data available
generate_report(df, output_directory + "/" + str(df.get("data").get("id")), 'report.html')

print("Output created at: /output/" + str(df.get("data").get("id")))