## flask app for processing files

Created and deployed a flask app for a a friend, which automates a task that used to take hours of his work.
Python and Pandas was used for the backend, while flask was used for the API.
This is a Flask application that processes Excel files and generates a processed Excel file. The application allows  the user to upload an Excel file, performs data processing and aggregation, and then downloads the processed Excel file. The app is deployed and accessible via a public URL using Render.

## Features

- Upload Excel files in .xls or .xlsx format
- Process data based on specific requirements
- Download the processed Excel file

## Deployment

This Flask application is deployed using Render. To access the application, visit the public URL provided by Render.

## Usage

1. Navigate to the public URL provided by Render.
2. Upload your Excel file by clicking the "Choose File" button and selecting your file.
3. Click the "Upload" button to process the file.
4. After processing, the app will prompt you to download the processed Excel file.

## Local Development

To run the application locally, follow these steps:

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
4. Install the required packages: `pip install -r requirements.txt`
5. Run the application: `python app.py`
6. Open your web browser and visit `http://127.0.0.1:5000` to access the application.

## App
![](https://github.com/giorgosrigas/flask_excel_processor/blob/main/flask_gif.gif)
