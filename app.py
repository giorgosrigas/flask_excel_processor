import os
from flask import Flask, request, send_file,  render_template_string
import pandas as pd
from io import BytesIO
from map_physios import change_excel

# Include the change_excel class definition here

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
   return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Excel File</title>
    <style>
        body {
            background-color: DarkSlateBlue;
            color: white;
        }
        input[type="file"],
        input[type="submit"] {
            font-size: 1.2em;
            padding: 5px;
        }
    </style>
</head>
<body>
    <h1>Upload the excel file</h1>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".xls,.xlsx">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
''')



@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # Create an instance of the change_excel class
        excel_processor = change_excel(file) 

        # Call the change_physio_otputs() method to process the data
        processed_df = excel_processor.change_physio_otputs()

        # Save the processed DataFrame to an Excel file
        output_filename = "processed.xlsx"
        # Use BytesIO to avoid writing to disk
        output_file = BytesIO()
        processed_df.to_excel(output_file, index=False)
        output_file.seek(0)

        # Return the processed file as a response
        return send_file(output_file, download_name=output_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

