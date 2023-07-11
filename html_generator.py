import os.path
import json
from bs4 import BeautifulSoup
from utils import *

class HTMLGenerator:
    def __init__(self, petition_id: str, petition_data: any, output_directory: str, output_filename: str):
        self.petition_id = petition_id
        self.petition_data = petition_data
        self.output_directory = output_directory
        self.output_filename = output_filename

    def generate_report(self):
        self._generate_js()
        self._generate_stylesheet()

        output_file = self._generate_output_file(self.output_directory, self.output_filename)

        output_string = "<!DOCTYPE html>"
        output_string += "<html>"
        output_string += "<head>"
        output_string += f"<title>{self.petition_data.get('data').get('attributes').get('action')} | {self.petition_data.get('data').get('id')}</title>"
        output_string += "<link rel=\"stylesheet\" href=\"./assets/styles.css\">"
        output_string += "</head>"
        output_string += "<body>"
        output_string += f"<h1>{self.petition_data.get('data').get('attributes').get('action')}</h1>"
        output_string += f"<p>{self.petition_data.get('data').get('attributes').get('background')}</p>"
        output_string += f"<p>{self.petition_data.get('data').get('attributes').get('additional_details')}</p>"

        output_string += self.generate_overview_table(self.petition_data.get('data').get('attributes'), self.petition_data.get('data').get('id'))

        if (self.petition_data.get('data').get('attributes').get('debate') != None):
            output_string += self.generate_debate_table(self.petition_data.get('data').get('attributes').get('debate'))

        output_string += str(self.generate_signatures_tables(self.petition_data.get('data').get('id')))

        output_string += "\n\n<p>All data has been gathered from the <a href=\"https://petition.parliament.uk/\" target=\"_blank\">UK Government and Parliament Petition website</a>.</p>"
        output_string += f"<p>All raw data can be found <a href={self.petition_data.get('links').get('self')} target=\"_blank\">here</a>.</p>"
        output_string += "<script src=\"./assets/index.js\"></script>"
        output_string += "</body>"
        output_string += "</html>"

        output_file.write(BeautifulSoup(output_string, "html.parser").prettify())

        output_file.close()

    '''
    | Function: generate_overview_table
    | ---
    | Generates the overview table for the petition.
    | ---
    | @param attributes: The attributes of the petition.
    | @return: The overview table as a string of HTML.
    '''
    def generate_overview_table(self, attributes: any, petition_id: int) -> str:
        overview_table_string = generate_two_column_table_row("Petition ID", str(petition_id))
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
    
        return convert_to_accordion("Overview", convert_to_table(overview_table_string))
    
    '''
    | Function: generate_debate_table
    | ---
    | Generates the debate table for the petition.
    | ---
    | @param attributes: The debate details of the petition.
    | @return: The debate table as a string of HTML.
    '''
    def generate_debate_table(self, debate_data: any) -> str:
        debate_table_string = generate_two_column_table_row("Debate date", debate_data.get('debated_on'))
        debate_table_string += generate_two_column_table_row("Debate transcript", f"<a href=\"{debate_data.get('transcript_url')}\">Transcript</a>")
        debate_table_string += generate_two_column_table_row("Video", f"<a href=\"{debate_data.get('video_url')}\">Video URL</a>")
    
        return convert_to_accordion("Debate", convert_to_table(debate_table_string))
    
    '''
    | Function: generate_signatures_tables
    | ---
    | Generates the signatures tables for the petition.
    | ---
    | @param petition_id: The ID of the petition, used to grab the `data_dump.json` file.
    | @return: The signatures tables as a string of HTML.
    '''
    def generate_signatures_tables(self, petition_id: str) -> str:
        with open(f"./output/{petition_id}/data_dump.json", "r") as petition_file:
            petition_data = json.load(petition_file)

        total_signatures = petition_data['total_signatures']

        signatures_table_total = generate_three_column_table_header("Region", "Signatures", "% of total")
        signatures_table_total += generate_three_column_table_row("Inside UK", format_number(petition_data['totals']['inside_uk']), format_percentage(petition_data['totals']['inside_uk_percent']))
        signatures_table_total += generate_three_column_table_row("Outside UK", format_number(petition_data['totals']['outside_uk']), format_percentage(petition_data['totals']['outside_uk_percent']))
        signatures_table_total += generate_three_column_table_row("Total", format_number(total_signatures), "100%")

        signatures_table = convert_to_accordion("Signatures (Total)", convert_to_table(signatures_table_total))

        # Global Signatures
        signatures_table_global = generate_three_column_table_header("Region", "Signatures", "% of total")

        for signature_global in petition_data['totals']['signatures_by_global_region']:
            signatures_table_global += generate_three_column_table_row(signature_global['title'], format_number(signature_global['total']), format_percentage(signature_global['percent']))

        signatures_table_global += generate_three_column_table_row("Total", format_number(total_signatures), "100%")

        signatures_table += convert_to_accordion("Signatures (Global)", convert_to_table(signatures_table_global))

        # UK Signatures
        signatures_table_uk = generate_three_column_table_header("Region", "Signatures", "% of total")

        for signature_uk in petition_data['totals']['signatures_by_uk_region']:
            signatures_table_uk += generate_three_column_table_row(signature_uk['title'], format_number(signature_uk['total']), format_percentage(signature_uk['percent']))

        signatures_table_uk += f"<tr><td colspan='3'><i>*Data may not add up to 100% due to how petition.parliament.uk categorises data</i></td></tr>"

        signatures_table += convert_to_accordion("Signatures (UK)", convert_to_table(signatures_table_uk))

        # Signatures by Country
        signatures_table_country = generate_two_column_table_header("Country", "Signatures")

        for country in petition_data['signatures_by_country']:
            signatures_table_country += generate_two_column_table_row(country['name'], format_number(country['signature_count']))

        signatures_table += convert_to_accordion("Signatures (Countries)", convert_to_table(signatures_table_country))

        # Signatures by Constituency
        signatures_table_constituency = generate_two_column_table_header("Constituency", "Signatures")

        for constituency in petition_data['signatures_by_constituency']:
            signatures_table_constituency += generate_two_column_table_row(constituency['name'], format_number(constituency['signature_count']))

        signatures_table += convert_to_accordion("Signatures (Constituency)", convert_to_table(signatures_table_constituency))
        
        return signatures_table

    def _generate_output_file(self, output_dir: str, output_filename: str):
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        return open(os.path.join(output_dir, output_filename), "w", encoding="utf-8")

    def _generate_stylesheet(self):
        styles_file = self._generate_output_file(f"{self.output_directory}/assets", "styles.css")
        source_file = open("./assets/styles.css", "r")

        styles_file.write(source_file.read())

        source_file.close()
        styles_file.close()

    def _generate_js(self):
       js_file = self._generate_output_file(f"{self.output_directory}/assets", "index.js")
       source_file = open("./assets/index.js", "r")

       js_file.write(source_file.read())

       source_file.close()
       js_file.close()

    
