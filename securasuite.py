import requests
import re
from bs4 import BeautifulSoup

# Function to extract sensitive information from a website
def extract_data(url, save_to_file=False):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Use regular expressions to find sensitive data (e.g., passwords)
            sensitive_data = re.findall(r'password:\s*(\w+)', response.text, re.IGNORECASE)
            
            result = ""
            if sensitive_data:
                result += "Sensitive data found:\n"
                for data in sensitive_data:
                    result += data + "\n"
            else:
                result += "No sensitive data found on the website."

            # Analyze HTTP headers for security issues
            headers = response.headers
            result += "\n\nHTTP Headers:\n"
            for key, value in headers.items():
                result += f"{key}: {value}\n"

            # Parse HTML content and find links
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [link.get('href') for link in soup.find_all('a')]
            result += "\nLinks on the page:\n"
            for link in links:
                result += link + "\n"

            # Check for common vulnerabilities (e.g., SQL injection)
            if 'SQL' in response.text:
                result += "\nPotential SQL injection detected."

            print(result)

            if save_to_file:
                with open("analysis_results.txt", "w") as file:
                    file.write(result)
                print("\nResults saved to 'analysis_results.txt'.")

        else:
            print("Failed to fetch data from the URL.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    website_url = input("Enter the URL to extract data from: ")
    save_option = input("Do you want to save results to a file? (yes/no): ").lower()
    
    if save_option == "yes":
        extract_data(website_url, save_to_file=True)
    else:
        extract_data(website_url)
