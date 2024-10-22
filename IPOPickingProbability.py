def calculate_probabilities(subscription_factor, max_applications):
    """
    Calculate the probability of no allotment and at least one allotment
    for a given number of applications, based on the oversubscription factor.
    
    Args:
        subscription_factor (float): The oversubscription factor (e.g., 10 for 10x subscription).
        max_applications (int): The maximum number of applications to calculate for.
    
    Returns:
        list of tuples: A list containing the number of applications, 
                        probability of no allotment, and probability of at least one allotment.
    """
    probabilities = []
    
    # Handle cases where subscription_factor is less than 1
    if subscription_factor < 1:
        for num_applications in range(1, max_applications + 1):
            # Probability of no allotment is 0% in case of undersubscription
            prob_no_allotment = 0
            # Probability of at least one allotment is 100% in case of undersubscription
            prob_at_least_one_allotment = 100
            probabilities.append((num_applications, prob_no_allotment, prob_at_least_one_allotment))
    else:
        # Calculate the probability of no allotment for a single application
        probability_of_no_allotment_single = 1 - (1 / subscription_factor)
        
        for num_applications in range(1, max_applications + 1):
            # Probability of no allotment for multiple applications
            prob_no_allotment = probability_of_no_allotment_single ** num_applications
            # Probability of at least one allotment
            prob_at_least_one_allotment = 1 - prob_no_allotment
            
            probabilities.append((num_applications, round(prob_no_allotment * 100, 2), round(prob_at_least_one_allotment * 100, 2)))
    
    return probabilities

def print_probabilities(probabilities):
    """
    Print the calculated probabilities in a table format.
    
    Args:
        probabilities (list of tuples): A list of calculated probabilities.
    """
    print(f"{'No. of Applications':<20} {'Probability of No Allotment (%)':<30} {'Probability of At Least 1 Allotment (%)':<30}")
    print("-" * 80)
    for num_applications, prob_no, prob_at_least_one in probabilities:
        print(f"{num_applications:<20} {prob_no:<30} {prob_at_least_one:<30}")

# Main function to take inputs and display the table
# Main function to take inputs and display the table
def main():
    try:
        subscription_factor = float(input("Enter the IPO oversubscription factor (can be < 1 for undersubscription): "))
        max_applications = int(input("Enter the maximum number of applications: "))
        
        if max_applications <= 0:
            print("The number of applications must be a positive integer.")
        else:
            probabilities = calculate_probabilities(subscription_factor, max_applications)
            print_probabilities(probabilities)
    except ValueError:
        print("Please enter valid numeric values.")

if __name__ == "__main__":
    main()

