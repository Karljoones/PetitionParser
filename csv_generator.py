import os.path

def _generate_output_file(output_directory, output_filename):
    output_file_path = os.path.join(output_directory, output_filename)
    output_file = open(output_file_path, "w", encoding="utf-8")
    return output_file

def generate_csv(data, output_directory, output_filename):
    output_file = _generate_output_file(output_directory, output_filename)

    data.to_csv(output_file, sep='\t', encoding='utf-8')
    output_file.close()