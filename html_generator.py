import os.path 
import json
from bs4 import BeautifulSoup

def _generate_output_file(output_directory, output_filename):
    output_file_path = os.path.join(output_directory, output_filename)
    output_file = open(output_file_path, "w", encoding="utf-8")
    return output_file

def generate_report(df, output_directory, output_filename):
    output_file = _generate_output_file(output_directory, output_filename)

    output_string = "<!DOCTYPE html>"
    output_string += "<html>"
    output_string += "<head>"
    output_string += f"<title>{df.get('data').get('attributes').get('action')} | {df.get('data').get('id')}</title>"
    output_string += "<style>body { max-width: 50%; margin-left: auto; margin-right: auto; color: black; background-color: white;} @media(prefers-color-scheme:dark){ body{ color: white; background-color: black;} } table,td,tr,th { border: 1px solid black; border-collapse: collapse } @media(prefers-color-scheme:dark){ table,td,tr,th { border: 1px solid white; } } td { padding: 4px 8px; width: 50% } td.third { width: 33%; }</style>"
    output_string += "</head>"
    output_string += "<body>"
    output_string += f"<h1>{df.get('data').get('attributes').get('action')} ({df.get('data').get('id')})</h1>"
    output_string += f"<p>{df.get('data').get('attributes').get('background')}</p>"
    output_string += f"<p>{df.get('data').get('attributes').get('additional_details')}</p>"

    output_string += generate_overview_table(df.get('data').get('attributes'))

    if (df.get('data').get('attributes').get('debate') != None):
        output_string += generate_debate_table(df.get('data').get('attributes').get('debate'))

    output_string += generate_signatures_table(df.get('data').get('id'))

    output_string += "\n\n<p>All data has been gathered from the <a href=\"https://petition.parliament.uk/\">UK Government and Parliament Petition website</a>.</p>"
    output_string += f"<p>All raw data can be found <a href={df.get('links').get('self')}>here</a>.</p>"
    output_string += "</body>"
    output_string += "</html>"

    output_file.write(BeautifulSoup(output_string, "html.parser").prettify())

    output_file.close()

def generate_overview_table(attributes):
    overview_table_string = "<h2>Overview</h2>"
    overview_table_string += "<table style='width:100%'>"
    overview_table_string += f"<tr><td>Signature count</td><td>{attributes.get('signature_count')}</td></tr>"
    overview_table_string += f"<tr><td>State</td><td>{attributes.get('state')}</td></tr>"
    overview_table_string += f"<tr><td>Created at</td><td>{attributes.get('created_at')}</td></tr>"
    overview_table_string += f"<tr><td>Updated at</td><td>{attributes.get('updated_at')}</td></tr>"
    overview_table_string += f"<tr><td>Rejected at</td><td>{attributes.get('rejected_at')}</td></tr>"
    overview_table_string += f"<tr><td>Opened at</td><td>{attributes.get('opened_at')}</td></tr>"
    overview_table_string += f"<tr><td>Closed at</td><td>{attributes.get('closed_at')}</td></tr>"
    overview_table_string += f"<tr><td>Governement response at</td><td>{attributes.get('government_response_at')}</td></tr>"
    overview_table_string += f"<tr><td>Debate threadhold reached</td><td>{attributes.get('debate_threshold_reached_at')}</td></tr>"
    overview_table_string += f"<tr><td>Scheduled debated date</td><td>{attributes.get('scheduled_debate_date')}</td></tr>"
    overview_table_string += f"<tr><td>Moderation threshold reached</td><td>{attributes.get('moderation_threshold_reached_at')}</td></tr>"
    overview_table_string += f"<tr><td>Response threshold reached</td><td>{attributes.get('response_threshold_reached_at')}</td></tr>"
    overview_table_string += f"<tr><td>Creator name</td><td>{attributes.get('creator_name')}</td></tr>"
    overview_table_string += "</table>"

    return overview_table_string

def generate_debate_table(debate_data): 
    debate_table_string = "<h2>Debate</h2>"
    debate_table_string += "<table style='width:100%'>"
    debate_table_string += f"<tr><td>Debate date</td><td>{debate_data.get('debated_on')}</td></tr>"
    debate_table_string += f"<tr><td>Debate transcript</td><td><a href=\"{debate_data.get('transcript_url')}\">Transcript</a></td></tr>"
    debate_table_string += f"<tr><td>Video</td><td><a href=\"{debate_data.get('video_url')}\">Video URL</a></td></tr>"
    debate_table_string += "</table>"

    return debate_table_string

def generate_signatures_table(petition_id):
    with open(f"./output/{petition_id}/data_dump.json", "r") as petition_file:
        petition_data = json.load(petition_file)
    
    total_signatures = petition_data['total_signatures']

    if (total_signatures == 0):
        signatures_table_string = "<h2>Signatures</h2>"
        signatures_table_string += "<i>It looks like there is not enough data found to analyse signatures. This may be due to the age of the petition.</i>"
        return signatures_table_string

    signatures_table_string = "<h2>Signatures (Total)</h2>"
    signatures_table_string += "<table style='width:100%'>"
    signatures_table_string += "<tr><th class='third'>Region</th><th class='third'>Signatures</th><th class='third'>% of total</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Inside UK</td><td class='third'>{(total_signatures - petition_data['total_signatures_outside_uk']):n}</td><td class='third'>{str(round((total_signatures - petition_data['total_signatures_outside_uk']) / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Outside UK</td><td class='third'>{(petition_data['total_signatures_outside_uk']):n}</td><td class='third'>{str(round(petition_data['total_signatures_outside_uk'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Total</td><td class='third'>{total_signatures:n}</td><td class='third'>100%</td></tr>"
    signatures_table_string += "</table>"

    signatures_table_string += "<h2>Signatures (Global)</h2>"
    signatures_table_string += "<table style='width:100%'>"
    signatures_table_string += "<tr><th class='third'>Region</th><th class='third'>Signatures</th><th class='third'>% of total</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Africa</td><td class='third'>{(petition_data['total_region_africa']):n}</td><td class='third'>{str(round(petition_data['total_region_africa'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Asia</td><td class='third'>{(petition_data['total_region_asia']):n}</td><td class='third'>{str(round(petition_data['total_region_asia'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Carribean</td><td class='third'>{(petition_data['total_region_carribean']):n}</td><td class='third'>{str(round(petition_data['total_region_carribean'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Central America</td><td class='third'>{(petition_data['total_region_central_america']):n}</td><td class='third'>{str(round(petition_data['total_region_central_america'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Europe</td><td class='third'>{(petition_data['total_region_europe']):n}</td><td class='third'>{str(round(petition_data['total_region_europe'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>North America</td><td class='third'>{(petition_data['total_region_north_america']):n}</td><td class='third'>{str(round(petition_data['total_region_north_america'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Oceania</td><td class='third'>{(petition_data['total_region_oceania']):n}</td><td class='third'>{str(round(petition_data['total_region_oceania'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>South America</td><td class='third'>{(petition_data['total_region_south_america']):n}</td><td class='third'>{str(round(petition_data['total_region_south_america'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Other/Unknown</td><td class='third'>{(petition_data['total_region_unknown']):n}</td><td class='third'>{str(round(petition_data['total_region_unknown'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Total</td><td class='third'>{total_signatures:n}</td><td class='third'>100%</td></tr>"
    signatures_table_string += "</table>"

    signatures_table_string += "<h2>Signatures (UK)</h2>"
    signatures_table_string += "<table style='width:100%'>"
    signatures_table_string += "<tr><th class='third'>Region</th><th class='third'>Signatures</th><th class='third'>% of total</td></tr>"
    signatures_table_string += f"<tr><td class='third'>England</td><td class='third'>{(petition_data['total_signatures_england']):n}</td><td class='third'>{str(round(petition_data['total_signatures_england'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Northern Ireland</td><td class='third'>{(petition_data['total_signatures_ni']):n}</td><td class='third'>{str(round(petition_data['total_signatures_ni'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Scotland</td><td class='third'>{(petition_data['total_signatures_scotland']):n}</td><td class='third'>{str(round(petition_data['total_signatures_scotland'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td class='third'>Wales</td><td class='third'>{(petition_data['total_signatures_wales']):n}</td><td class='third'>{str(round(petition_data['total_signatures_wales'] / total_signatures * 100, 2))}%</td></tr>"
    signatures_table_string += f"<tr><td colspan='3'><i>*Data may not add up to 100% due to how petition.parliament.uk categorises data</i></td></tr>"
    signatures_table_string += "</table>"

    return signatures_table_string