import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://ipowatch.in/waaree-energies-ipo-subscription-status/"

def retrieve_subscription_rate():
    """
    Retrieve the subscription rate based on the current day of the IPO.
    """
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find and extract IPO start and end dates
        date_paragraphs = soup.find_all('p')
        start_date = None
        end_date = None

        for paragraph in date_paragraphs:
            if 'IPO subscription status started on' in paragraph.text:
                text = paragraph.text
                if 'and will close on' in text:
                    parts = text.split('and will close on')
                    start_date = parts[0].split('on')[-1].strip()
                    end_date = parts[1].strip().split('.')[0]
                    start_date = start_date.replace('day', '').strip()

        if start_date and end_date:
            try:
                start_date_dt = datetime.strptime(start_date, "%B %d, %Y")
                end_date_dt = datetime.strptime(end_date, "%B %d, %Y")
            except ValueError as e:
                print(f"Error parsing dates: {e}")
                return None

            current_date = datetime.now()

            if current_date >= start_date_dt and current_date <= end_date_dt:
                subscription_day = (current_date - start_date_dt).days + 1
            else:
                print("The IPO subscription period is either yet to start or has ended.")
                return None

            # Extract subscription value for the appropriate day
            table = soup.find('figure', {'class': 'wp-block-table'})
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) > 0 and 'RII' in columns[0].text:
                        return float(columns[subscription_day].text.strip())
            else:
                print("Unable to find the subscription rate table.")
                return None
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def generate_html_report(subscription_rate, start_date, end_date):
    """
    Generate a static HTML file with subscription rate and IPO details.
    """
    html_content = f"""
    <html>
    <head>
        <title>IPO Subscription Report</title>
    </head>
    <body>
        <h1>IPO Subscription Details</h1>
        <p><strong>Start Date:</strong> {start_date}</p>
        <p><strong>End Date:</strong> {end_date}</p>
        <p><strong>Subscription Rate on Current Day:</strong> {subscription_rate}x</p>
    </body>
    </html>
    """

    with open("ipo_subscription_report.html", "w") as file:
        file.write(html_content)

    print("HTML report generated: ipo_subscription_report.html")


def main():
    # Retrieve subscription rate automatically
    subscription_factor = retrieve_subscription_rate()

    if subscription_factor is None:
        print("Failed to retrieve the subscription rate.")
        return

    # Dates are hardcoded for demonstration, you can fetch dynamically if required
    start_date = "October 21, 2024"
    end_date = "October 23, 2024"

    print(f"Retrieved subscription rate: {subscription_factor}x")

    # Generate the static HTML report
    generate_html_report(subscription_factor, start_date, end_date)


if __name__ == "__main__":
    main()
