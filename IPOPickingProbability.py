import requests
from bs4 import BeautifulSoup
from datetime import datetime

# New URL to check for subscription status
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


def calculate_probabilities(subscription_factor, max_applications):
    """
    Calculate the probability of no allotment and at least one allotment
    for a given number of applications, based on the oversubscription factor.
    """
    probabilities = []

    # Handle cases where subscription_factor is less than 1
    if subscription_factor < 1:
        for num_applications in range(1, max_applications + 1):
            prob_no_allotment = 0
            prob_at_least_one_allotment = 100
            probabilities.append((num_applications, prob_no_allotment, prob_at_least_one_allotment))
    else:
        probability_of_no_allotment_single = 1 - (1 / subscription_factor)

        for num_applications in range(1, max_applications + 1):
            prob_no_allotment = probability_of_no_allotment_single ** num_applications
            prob_at_least_one_allotment = 1 - prob_no_allotment

            probabilities.append((num_applications, round(prob_no_allotment * 100, 2), round(prob_at_least_one_allotment * 100, 2)))

    return probabilities


def print_probabilities(probabilities):
    """
    Print the calculated probabilities in a table format.
    """
    print(f"{'No. of Applications':<20} {'Probability of No Allotment (%)':<30} {'Probability of At Least 1 Allotment (%)':<30}")
    print("-" * 80)
    for num_applications, prob_no, prob_at_least_one in probabilities:
        print(f"{num_applications:<20} {prob_no:<30} {prob_at_least_one:<30}")


def main():
    try:
        # Retrieve subscription rate automatically
        subscription_factor = retrieve_subscription_rate()

        if subscription_factor is None:
            print("Failed to retrieve the subscription rate.")
            return

        print(f"Retrieved subscription rate: {subscription_factor}x")

        max_applications = int(20)

        if max_applications <= 0:
            print("The number of applications must be a positive integer.")
        else:
            probabilities = calculate_probabilities(subscription_factor, max_applications)
            print_probabilities(probabilities)
    except ValueError:
        print("Please enter valid numeric values.")


if __name__ == "__main__":
    main()
