import pandas as pd
import os.path
from region_helper import *
import locale

locale.setlocale(locale.LC_ALL, '')

petition_download_link = ""
petition_id = 0
petition_id = input("Petition ID: ")

if petition_id != 0 or petition_id != "":
    petition_download_link = f"https://petition.parliament.uk/petitions/{str(petition_id)}.json"
else:
    print("Invalid petition ID")
    exit()

df = pd.read_json(petition_download_link)

# Output dir
output_directory = "./output"
if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

instance_directory = output_directory + "/" + str(df.get("data").get("id"))
if not os.path.isdir(instance_directory):
    os.mkdir(instance_directory)

# Handle creating the directory, and opening the file using the petition ID
overview_filename = "overview.txt"
overview_file_path = os.path.join(instance_directory, overview_filename)
overview_output_file = open(overview_file_path, "w", encoding='utf-8')

overview_output_file.write(f"Title: {df.get('data').get('attributes').get('action')} (ID: {df.get('data').get('id')}) \n\n")
overview_output_file.write("State: " + df.get("data").get("attributes").get("state") + "\n")
overview_output_file.write("Created at: " + df.get("data").get("attributes").get("created_at") + "\n")
overview_output_file.write("Updated at: " + df.get("data").get("attributes").get("updated_at") + "\n")

## Signatures by country
signatures_by_country = pd.DataFrame(df.get("data").get("attributes").get("signatures_by_country"))

# File creation
signatures_by_country_filename = "signatures_by_country.csv"
signatures_by_country_file_path = os.path.join(instance_directory, signatures_by_country_filename)
signatures_by_country_output_file = open(signatures_by_country_file_path, "w")

## Data writing
signatures_by_country.to_csv(signatures_by_country_output_file, sep='\t', encoding='utf-8')

# File closing
signatures_by_country_output_file.close()

# Analysis
total_signatures_outside_uk = 0
total_signatures = df.get("data").get("attributes").get("signature_count")
total_region_africa = 0
total_region_asia = 0
total_region_carribean = 0
total_region_central_america = 0
total_region_europe = 0
total_region_north_america = 0
total_region_oceania = 0
total_region_south_america = 0
total_region_unknown = 0

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
        print(f"Unknown region: {row.get('name')}")
        total_region_unknown += row.get("signature_count")

# Cleanup
del signatures_by_country

overview_output_file.write("\n-- Global Analysis --\n")
overview_output_file.write(f"Total signatures: {total_signatures:n}\n")
overview_output_file.write(f"Inside UK: {(total_signatures - total_signatures_outside_uk):n} ({str(round((total_signatures - total_signatures_outside_uk) / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Outside UK: {total_signatures_outside_uk:n} ({str(round(total_signatures_outside_uk / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Africa: {total_region_africa:n} ({str(round(total_region_africa / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Asia: {total_region_asia:n} ({str(round(total_region_asia / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Carribean: {total_region_carribean:n} ({str(round(total_region_carribean / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Central America: {total_region_central_america:n} ({str(round(total_region_central_america / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Europe: {total_region_europe:n} ({str(round(total_region_europe / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"North America: {total_region_north_america:n} ({str(round(total_region_north_america / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Oceania: {total_region_oceania:n} ({str(round(total_region_oceania / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"South America: {total_region_south_america:n} ({str(round(total_region_south_america / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Unknown: {total_region_unknown:n} ({str(round(total_region_unknown / total_signatures * 100, 2))}%)\n")

## Signatures by constituency
signatures_by_constituency = pd.DataFrame(df.get("data").get("attributes").get("signatures_by_constituency"))

# File creation
signatures_by_constituency_filename = "signatures_by_constituency.csv"
signatures_by_constituency_file_path = os.path.join(instance_directory, signatures_by_constituency_filename)
signatures_by_constituency_output_file = open(signatures_by_constituency_file_path, "w")

## Data writing
signatures_by_constituency.to_csv(signatures_by_constituency_output_file, sep='\t', encoding='utf-8')

# File closing
signatures_by_constituency_output_file.close()

# Cleanup
del signatures_by_constituency

# Signatures by region
signatures_by_region = pd.DataFrame(df.get("data").get("attributes").get("signatures_by_region"))

# File creation
signatures_by_region_filename = "signatures_by_region.csv"
signatures_by_region_file_path = os.path.join(instance_directory, signatures_by_region_filename)
signatures_by_region_output_file = open(signatures_by_region_file_path, "w")

## Data writing
signatures_by_region.to_csv(signatures_by_region_output_file, sep='\t', encoding='utf-8')

# File closing
signatures_by_region_output_file.close()

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

overview_output_file.write("\n-- Regional Analysis --\n")
overview_output_file.write(f"England: {total_signatures_england:n} ({str(round(total_signatures_england / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Scotland: {total_signatures_scotland:n} ({str(round(total_signatures_scotland / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Wales: {total_signatures_wales:n} ({str(round(total_signatures_wales / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Northern Ireland: {total_signatures_ni:n} ({str(round(total_signatures_ni / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Other: {total_signatures_outside_uk:n} ({str(round(total_signatures_outside_uk / total_signatures * 100, 2))}%)\n")

overview_output_file.close()

print("Output created at: /output/" + str(df.get("data").get("id")))