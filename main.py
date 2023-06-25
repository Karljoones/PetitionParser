import pandas as pd
import os.path

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

overview_output_file.write("Title: " + df.get("data").get("attributes").get("action") + "\n\n")
overview_output_file.write("State: " + df.get("data").get("attributes").get("state") + "\n")
overview_output_file.write("Created at: " + df.get("data").get("attributes").get("created_at") + "\n")
overview_output_file.write("Updated at: " + df.get("data").get("attributes").get("updated_at") + "\n")

## Signatures by country
signatures_by_country = pd.DataFrame(df.get("data").get("attributes").get("signatures_by_country"))

# File creation
sbc_filename = "signatures_by_country.csv"
sbc_file_path = os.path.join(instance_directory, sbc_filename)
sbc_output_file = open(sbc_file_path, "w")

## Data writing
signatures_by_country.to_csv(sbc_output_file, sep='\t', encoding='utf-8')

# File closing
sbc_output_file.close()

# Analysis
total_signatures_outside_uk = 0
total_signatures = 0
for index, row in signatures_by_country.iterrows():
    total_signatures += row.get("signature_count")
    if row.get("name") != "United Kingdom":
        total_signatures_outside_uk += row.get("signature_count")

# Cleanup
del signatures_by_country

overview_output_file.write("\n-- Global Analysis --\n")
overview_output_file.write("Total signatures: " + str(total_signatures) + "\n")
overview_output_file.write(f"Inside UK: {total_signatures - total_signatures_outside_uk} ({str(round((total_signatures - total_signatures_outside_uk) / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Outside UK: {total_signatures_outside_uk} ({str(round(total_signatures_outside_uk / total_signatures * 100, 2))}%)\n")

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
england_regions = ["North East", "North West", "Yorkshire and the Humber", "East Midlands", "West Midlands", "East of England", "London", "South East", "South West"]
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
overview_output_file.write(f"England: {total_signatures_england} ({str(round(total_signatures_england / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Scotland: {total_signatures_scotland} ({str(round(total_signatures_scotland / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Wales: {total_signatures_wales} ({str(round(total_signatures_wales / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Northern Ireland: {total_signatures_ni} ({str(round(total_signatures_ni / total_signatures * 100, 2))}%)\n")
overview_output_file.write(f"Other: {total_signatures_outside_uk} ({str(round(total_signatures_outside_uk / total_signatures * 100, 2))}%)\n")

overview_output_file.close()

print("Output created at: /output/" + str(df.get("data").get("id")))