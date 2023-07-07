import os.path
import json
from bs4 import BeautifulSoup
from performance_helper import *

def _generate_output_file(output_directory: str, output_filename: str):
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    output_file_path = os.path.join(output_directory, output_filename)
    output_file = open(output_file_path, "w", encoding="utf-8")
    return output_file

def generate_two_column_table_row(column_one_content: str, column_two_content: str):
    return f"<tr><td>{column_one_content}</td><td>{column_two_content or ''}</td></tr>"

def generate_two_column_table_header(header_one: str, header_two: str):
    return f"<tr><th>{header_one}</th><th>{header_two}</th></tr>"

def generate_three_column_table_row(column_one_content: str, column_two_content: str, column_three_content: str):
    return f"<tr><td class='third'>{column_one_content}</td><td class='third'>{column_two_content or ''}</td><td class='third'>{column_three_content or ''}</td></tr>"

def generate_three_column_table_header(header_one: str, header_two: str, header_three: str):
    return f"<tr><th>{header_one}</th><th>{header_two}</th><th>{header_three}</th></tr>"

def format_number(number: int):
    return "{:,}".format(number)

def format_percentage(number: float):
    return f"{number}%"

def convert_to_accordion(title: str, content: str):
    return f"<button class='accordion'>{title}</button><div class='panel'>{content}</div>"

@generate_report_performance_check
def generate_report(df, output_directory, output_filename):
    output_file = _generate_output_file(output_directory, output_filename)

    output_string = "<!DOCTYPE html>"
    output_string += "<html>"
    output_string += "<head>"
    output_string += f"<title>{df.get('data').get('attributes').get('action')} | {df.get('data').get('id')}</title>"
    output_string += "<link rel=\"stylesheet\" href=\"./assets/styles.css\">"
    output_string += "</head>"
    output_string += "<body>"
    output_string += f"<h1>{df.get('data').get('attributes').get('action')}</h1>"
    output_string += f"<p>{df.get('data').get('attributes').get('background')}</p>"
    output_string += f"<p>{df.get('data').get('attributes').get('additional_details')}</p>"

    output_string += generate_overview_table(df.get('data').get('attributes'))

    if (df.get('data').get('attributes').get('debate') != None):
        output_string += generate_debate_table(df.get('data').get('attributes').get('debate'))

    output_string += str(generate_signatures_table(df.get('data').get('id')))

    output_string += "\n\n<p>All data has been gathered from the <a href=\"https://petition.parliament.uk/\" target=\"_blank\">UK Government and Parliament Petition website</a>.</p>"
    output_string += f"<p>All raw data can be found <a href={df.get('links').get('self')} target=\"_blank\">here</a>.</p>"
    output_string += "<script src=\"./assets/index.js\"></script>"
    output_string += "</body>"
    output_string += "</html>"

    output_file.write(BeautifulSoup(output_string, "html.parser").prettify())

    output_file.close()

    generate_stylesheet(output_directory, "styles.css")
    generate_js(output_directory, "index.js")


def generate_overview_table(attributes):
    overview_table_string = "<table>"
    overview_table_string += generate_two_column_table_row("Petition ID", attributes.get('id'))
    overview_table_string += generate_two_column_table_row("Signature count", format_number(attributes.get('signature_count')))
    overview_table_string += generate_two_column_table_row("State", attributes.get('state'))
    overview_table_string += generate_two_column_table_row("Created", attributes.get('created_at'))
    overview_table_string += generate_two_column_table_row("Updated", attributes.get('updated_at'))
    overview_table_string += generate_two_column_table_row("Rejected", attributes.get('rejected_at'))
    overview_table_string += generate_two_column_table_row("Opened", attributes.get('opened_at'))
    overview_table_string += generate_two_column_table_row("Closed", attributes.get('closed_at'))
    overview_table_string += generate_two_column_table_row("Government response", attributes.get('government_response_at'))
    overview_table_string += generate_two_column_table_row("Debate threshold reached", attributes.get('debate_threshold_reached_at'))
    overview_table_string += generate_two_column_table_row("Scheduled debate date", attributes.get('scheduled_debate_date'))
    overview_table_string += generate_two_column_table_row("Moderation threshold reached", attributes.get('moderation_threshold_reached_at'))
    overview_table_string += generate_two_column_table_row("Response threshold reached", attributes.get('response_threshold_reached_at'))
    overview_table_string += generate_two_column_table_row("Creator", attributes.get('creator_name'))
    overview_table_string += "</table>"

    return convert_to_accordion("Overview", overview_table_string)


def generate_debate_table(debate_data):
    debate_table_string = "<table>"
    debate_table_string += generate_two_column_table_row("Debate date", debate_data.get('debated_on'))
    debate_table_string += generate_two_column_table_row("Debate transcript", f"<a href=\"{debate_data.get('transcript_url')}\">Transcript</a>")
    debate_table_string += generate_two_column_table_row("Video", f"<a href=\"{debate_data.get('video_url')}\">Video URL</a>")
    debate_table_string += "</table>"

    return convert_to_accordion("Debate", debate_table_string)


def generate_signatures_table(petition_id):
    with open(f"./output/{petition_id}/data_dump.json", "r") as petition_file:
        petition_data = json.load(petition_file)

    total_signatures = petition_data['total_signatures']
    
    signatures_table = ""

    signatures_table_total = "<table>"
    signatures_table_total += generate_three_column_table_header("Region", "Signatures", "% of total")
    signatures_table_total += generate_three_column_table_row("Inside UK", format_number(petition_data['totals']['inside_uk']), format_percentage(petition_data['totals']['inside_uk_percent']))
    signatures_table_total += generate_three_column_table_row("Outside UK", format_number(petition_data['totals']['outside_uk']), format_percentage(petition_data['totals']['outside_uk_percent']))
    signatures_table_total += generate_three_column_table_row("Total", format_number(total_signatures), "100%")
    signatures_table_total += "</table>"

    signatures_table += convert_to_accordion("Signatures (Total)", signatures_table_total)

    signatures_table_global = "<table>"
    signatures_table_global += generate_three_column_table_header("Region", "Signatures", "% of total")
    signatures_table_global += generate_three_column_table_row("Africa", format_number(petition_data['totals']['global']['africa']), format_percentage(petition_data['totals']['global']['africa_percent']))
    signatures_table_global += generate_three_column_table_row("Asia", format_number(petition_data['totals']['global']['asia']), format_percentage(petition_data['totals']['global']['asia_percent']))
    signatures_table_global += generate_three_column_table_row("Carribean", format_number(petition_data['totals']['global']['carribean']), format_percentage(petition_data['totals']['global']['carribean_percent']))
    signatures_table_global += generate_three_column_table_row("Central America", format_number(petition_data['totals']['global']['central_america']), format_percentage(petition_data['totals']['global']['central_america_percent']))
    signatures_table_global += generate_three_column_table_row("Europe", format_number(petition_data['totals']['global']['europe']), format_percentage(petition_data['totals']['global']['europe_percent']))
    signatures_table_global += generate_three_column_table_row("North America", format_number(petition_data['totals']['global']['north_america']), format_percentage(petition_data['totals']['global']['north_america_percent']))
    signatures_table_global += generate_three_column_table_row("Oceania", format_number(petition_data['totals']['global']['oceania']), format_percentage(petition_data['totals']['global']['oceania_percent']))
    signatures_table_global += generate_three_column_table_row("South America", format_number(petition_data['totals']['global']['south_america']), format_percentage(petition_data['totals']['global']['south_america_percent']))
    signatures_table_global += generate_three_column_table_row("Other/Unknown", format_number(petition_data['totals']['global']['unknown']), format_percentage(petition_data['totals']['global']['unknown_percent']))
    signatures_table_global += generate_three_column_table_row("Total", format_number(total_signatures), "100%")
    
    signatures_table_global += "</table>"

    signatures_table += convert_to_accordion("Signatures (Global)", signatures_table_global)

    signatures_table_uk = "<table>"
    signatures_table_uk += generate_three_column_table_header("Region", "Signatures", "% of total")
    signatures_table_uk += generate_three_column_table_row("England", format_number(petition_data['totals']['uk']['england']), format_percentage(petition_data['totals']['uk']['england_percent']))
    signatures_table_uk += generate_three_column_table_row("Northern Ireland", format_number(petition_data['totals']['uk']['ni']), format_percentage(petition_data['totals']['uk']['ni_percent']))
    signatures_table_uk += generate_three_column_table_row("Wales", format_number(petition_data['totals']['uk']['wales']), format_percentage(petition_data['totals']['uk']['wales_percent']))
    signatures_table_uk += generate_three_column_table_row("Scotland", format_number(petition_data['totals']['uk']['scotland']), format_percentage(petition_data['totals']['uk']['scotland_percent']))
    signatures_table_uk += f"<tr><td colspan='3'><i>*Data may not add up to 100% due to how petition.parliament.uk categorises data</i></td></tr>"
    signatures_table_uk += "</table>"

    signatures_table += convert_to_accordion("Signatures (UK)", signatures_table_uk)

    return signatures_table

def generate_stylesheet(output_directory: str, output_filename: str):
    styles_file = _generate_output_file(f"{output_directory}/assets", output_filename)
    source_file = open("./assets/styles.css", "r")

    styles_file.write(source_file.read())

    source_file.close()
    styles_file.close()

def generate_js(output_directory: str, output_filename: str):
    js_file = _generate_output_file(f"{output_directory}/assets", output_filename)
    source_file = open("./assets/index.js", "r")

    js_file.write(source_file.read())

    source_file.close()
    js_file.close()