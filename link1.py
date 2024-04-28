import pdfkit
from urllib.parse import urlparse, parse_qs

def save_html_as_pdf(url):
    # Set the path to the wkhtmltopdf executable
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Update with your actual path
    # Create options for wkhtmltopdf
    options = {
        'quiet': '',
    }

    # Specify the URL of the HTML page
    html_url = url

    try:
        # Extract seat number from the URL
        seat_number = extract_seat_number(html_url)

        # If seat number is not found, use a default name
        if not seat_number:
            seat_number = 'unknown_seat'

        # Combine the seat number and filename to get the full path
        filename = f"{seat_number}.pdf"

        # Convert HTML to PDF and save in the current working directory
        pdfkit.from_url(html_url, filename, options=options, configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path))
        print(f"PDF saved successfully as {filename}")
    except Exception as e:
        print(f"Failed to convert HTML to PDF. Error: {e}")

def extract_seat_number(url):
    # Extract seat number from the 'HtmlURL' parameter in the URL
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    html_url = query_params.get('HtmlURL', [''])[0]

    # Split the 'HtmlURL' parameter and get the second part
    seat_number = html_url.split(',')[1] if ',' in html_url else None

    return seat_number

# Example usage:
html_url = "https://www.phpzag.com/build-content-management-system-with-php-mysql/"
save_html_as_pdf(html_url)
