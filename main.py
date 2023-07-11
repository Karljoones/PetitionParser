import pandas as pd
import os.path
import locale
import json
from region_helper import *
from html_generator import *

OUTPUT_DIRECTORY = "./output"

locale.setlocale(locale.LC_ALL, '')

data_dump = {}

'''
| Function: get_user_input
| ---
| Gets the user input for the petition ID
| ---
| @return: The petition ID as an integer
'''
def get_user_input() -> int:
    while True:
        try:
            return int(input("Enter petition ID: "))
        except ValueError:
            print("Please enter a valid petition ID.")

'''
| Function: get_petition_data
| ---
| Returns the petition data from the API
| ---
| @param petition_id: The ID of the petition to get data for
| @return: The petition data as a dataframe from pandas
'''
def get_petition_data(petition_id: int) -> any:
    df = pd.read_json(f"https://petition.parliament.uk/petitions/{str(petition_id)}.json")
    df.fillna(0)
    return df

'''
| Function: generate_output_directory
| ---
| Generates the output directory for the petition
| ---
| @param petition_id: The ID of the petition to generate the directory for
'''
def generate_output_directory(petition_id: int) -> None:
    if not os.path.exists(OUTPUT_DIRECTORY + "/" + str(petition_id)):
        os.makedirs(OUTPUT_DIRECTORY + "/" + str(petition_id))

'''
| Function: generate_initial_values
| ---
| Generates the initial values for the data dump
| ---
| @param df: The dataframe to generate the initial values from
'''
def generate_initial_values(df: any) -> None:
    data_dump["id"] = df.get("data").get("id")
    data_dump["total_signatures"] = df.get("data").get("attributes").get("signature_count")
    data_dump["totals"] = {}

'''
| Function: generate_signatures_by_country
| ---
| Generates the signatures by country data
| ---
| @param signatures_by_country: The signatures by country data
| @param petition_id: The ID of the petition
'''
def generate_signatures_by_country(signatures_by_country: any) -> None:
    if signatures_by_country == None:
        return
    
    # generate_csv(signatures_by_country, OUTPUT_DIRECTORY + f"/{str(petition_id)}", "signatures_by_country.csv")

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

    for country in signatures_by_country:
        if country.get("name") != "United Kingdom":
            total_signatures_outside_uk += country.get("signature_count")

        if country.get("name") in africa_region:
            total_region_africa += country.get("signature_count")
        elif country.get("name") in asia_region:
            total_region_asia += country.get("signature_count")
        elif country.get("name") in carribean_region:
            total_region_carribean += country.get("signature_count")
        elif country.get("name") in central_america_region:
            total_region_central_america += country.get("signature_count")
        elif country.get("name") in europe_region:
            total_region_europe += country.get("signature_count")
        elif country.get("name") in north_america_region:
            total_region_north_america += country.get("signature_count")
        elif country.get("name") in oceania_region:
            total_region_oceania += country.get("signature_count")
        elif country.get("name") in south_america_region:
            total_region_south_america += country.get("signature_count")
        else:
            total_region_unknown += country.get("signature_count")

    data_dump["totals"]["inside_uk"] = data_dump["total_signatures"] - total_signatures_outside_uk
    data_dump["totals"]["inside_uk_percent"] = round((data_dump["totals"]["inside_uk"] / data_dump['total_signatures']) * 100, 2)
    data_dump["totals"]["outside_uk"] = total_signatures_outside_uk
    data_dump["totals"]["outside_uk_percent"] = round((total_signatures_outside_uk / data_dump['total_signatures']) * 100, 2)

    signatures_by_global_region = [
        {"title": "Africa", "total": total_region_africa, "percent": round((total_region_africa / data_dump['total_signatures']) * 100, 2)},
        {"title": "Asia", "total": total_region_asia, "percent": round((total_region_asia / data_dump['total_signatures']) * 100, 2)},
        {"title": "Carribean", "total": total_region_carribean, "percent": round((total_region_carribean / data_dump['total_signatures']) * 100, 2)},
        {"title": "Central America", "total": total_region_central_america, "percent": round((total_region_central_america / data_dump['total_signatures']) * 100, 2)},
        {"title": "Europe", "total": total_region_europe, "percent": round((total_region_europe / data_dump['total_signatures']) * 100, 2)},
        {"title": "North America", "total": total_region_north_america, "percent": round((total_region_north_america / data_dump['total_signatures']) * 100, 2)},
        {"title": "Oceania", "total": total_region_oceania, "percent": round((total_region_oceania / data_dump['total_signatures']) * 100, 2)},
        {"title": "South America", "total": total_region_south_america, "percent": round((total_region_south_america / data_dump['total_signatures']) * 100, 2)},
        {"title": "Unknown", "total": total_region_unknown, "percent": round((total_region_unknown / data_dump['total_signatures']) * 100, 2)}
    ]

    data_dump["totals"]["signatures_by_global_region"] = sorted(signatures_by_global_region, key=lambda k: k['total'], reverse=True)

def generate_signatures_by_uk_region(signatures_by_uk_region: any) -> None:
    if signatures_by_uk_region == None:
        return

    # generate_csv(signatures_by_uk_region, OUTPUT_DIRECTORY + "/" + str(petition_id), "signatures_by_uk_region.csv")

    total_signatures_england = 0
    total_signatures_scotland = 0
    total_signatures_wales = 0
    total_signatures_ni = 0

    for region in signatures_by_uk_region:
        if region.get("name") in england_regions:
            total_signatures_england += region.get("signature_count")
        elif region.get("name") == "Scotland":
            total_signatures_scotland += region.get("signature_count")
        elif region.get("name") == "Wales":
            total_signatures_wales += region.get("signature_count")
        elif region.get("name") == "Northern Ireland":
            total_signatures_ni += region.get("signature_count")

    signatures = [
        {"title": "England", "total": total_signatures_england, "percent": round((total_signatures_england / data_dump['total_signatures']) * 100, 2)},
        {"title": "Scotland", "total": total_signatures_scotland, "percent": round((total_signatures_scotland / data_dump['total_signatures']) * 100, 2)},
        {"title": "Wales", "total": total_signatures_wales, "percent": round((total_signatures_wales / data_dump['total_signatures']) * 100, 2)},
        {"title": "Northern Ireland", "total": total_signatures_ni, "percent": round((total_signatures_ni / data_dump['total_signatures']) * 100, 2)}
    ]

    data_dump["totals"]["signatures_by_uk_region"] = sorted(signatures, key=lambda k: k['total'], reverse=True)

def generate_additional_data_transfer(petition_data: any):
    data_dump["signatures_by_country"] = sorted(petition_data.get('data').get('attributes').get('signatures_by_country'), key=lambda k: k['signature_count'], reverse=True)
    data_dump["signatures_by_constituency"] = sorted(petition_data.get('data').get('attributes').get('signatures_by_constituency'), key=lambda k: k['signature_count'], reverse=True)
    data_dump["signatures_by_region"] = sorted(petition_data.get('data').get('attributes').get('signatures_by_region'), key=lambda k: k['signature_count'], reverse=True)

'''
| Function: generate_data_dump
| ---
| Generate a JSON file with the data_dump variable, used for the HTML generator
| ---
| @param petition_id: the ID of the petition to generate the data dump for
'''
def generate_data_dump(petition_id: int):
    with open(OUTPUT_DIRECTORY + f"/{str(petition_id)}" + "/data_dump.json", "w") as data_dump_file:
        json.dump(data_dump, data_dump_file, indent=4)

    data_dump_file.close()

'''
| Function: main
| ---
| The main function of the program
'''
def main():
    # Grab data
    petition_id = get_user_input()
    petition_data = get_petition_data(petition_id)

    # Generate directories for output
    generate_output_directory(petition_id)

    # Generate initial values for data dump
    generate_initial_values(petition_data)

    # Analyse data
    generate_signatures_by_country(petition_data.get("data").get("attributes").get("signatures_by_country"))
    generate_signatures_by_uk_region(petition_data.get("data").get("attributes").get("signatures_by_region"))
    generate_additional_data_transfer(petition_data)

    generate_data_dump(petition_id)

    # Generate HTML
    generator = HTMLGenerator(petition_id, petition_data, f"{OUTPUT_DIRECTORY}/{petition_id}", "report.html")
    generator.generate_report()

    print(f"Output created at: {OUTPUT_DIRECTORY}/{petition_id}")

if __name__ == "__main__":
    main()