import requests # type: ignore

def analyze_file(file_path, api_url):
    """
    Analyzes a file by sending it to a specified API endpoint.

    Args:
        file_path (str): Path to the file to be analyzed.
        api_url (str): URL of the API endpoint.

    Returns:
        dict: JSON response from the API containing vulnerabilities.

    Raises:
        FileNotFoundError: If the file does not exist.
        requests.exceptions.RequestException: If there is an issue with the API request.
        ValueError: If the API response is not valid JSON.
    """
    try:
        # Open the file in a context manager to ensure it is properly closed
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(api_url, files=files)

            # Raise an exception for HTTP errors (e.g., 4xx, 5xx)
            response.raise_for_status()

            # Parse the JSON response
            vulnerabilities = response.json()
            return vulnerabilities

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to communicate with the API. Details: {e}")
        raise
    except ValueError as e:
        print(f"Error: Invalid JSON response from the API. Details: {e}")
        raise

# Example usage
if __name__ == "__main__":
    file_path = 'vulnerable_app.py'  # Replace with the actual file path
    api_url = 'http://localhost:8000/analyze/file'  # Replace with the actual API URL

    try:
        vulnerabilities = analyze_file(file_path, api_url)
        print("Vulnerabilities found:", vulnerabilities)
    except Exception as e:
        print("Analysis failed:", e)