import re
from bs4 import BeautifulSoup
import requests
from stores import stores

def find_total_locations(html_content):
    """
    Finds the "Total locations" number from Wikipedia HTML content.

    Args:
        html_content (str): The HTML content of a Wikipedia page.

    Returns:
        int or None: The number of total locations if found, otherwise None.
    """
    keywords = ["number of locations","operates over"]
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all text content
    text = soup.get_text(separator=' ')

    # Look for keywords and then find the first number after them
    for keyword in keywords:
        # Find keyword position
        keyword_pos = text.lower().find(keyword.lower())
        if keyword_pos != -1:
            # Look at the text after the keyword
            search_text = text[keyword_pos:keyword_pos + 100]  # Look ahead 100 chars
            # Find the first number after the keyword
            number_match = re.search(r'\d+', search_text.replace(",",""))
            print(search_text)
            if number_match:
                return int(number_match.group())

    return None



def find_locations_for_stores(stores):
    """
    Processes an array of store dictionaries to find "Total locations" for each store.

    Args:
        stores (list): List of dictionaries with "store" and "url" keys.

    Returns:
        tuple: Two lists, one for successful results and one for failed results.
    """
    success_results = []
    failed_results = []

    for store in stores:
        #if "decathlon" not in store["store"].lower():
            #continue  # Skip stores that are not Decathlon
        try:
            response = requests.get(store["url"], timeout=10)
            if response.status_code == 200:
                total_locations = find_total_locations(response.content)
                if total_locations is not None:
                    print({
                        "store": store["store"],
                        "url": store["url"],
                        "total_locations": total_locations
                    })
                    success_results.append({
                        "store": store["store"],
                        "url": store["url"],
                        "total_locations": total_locations
                    })
                else:
                    failed_results.append({
                        "store": store["store"],
                        "url": store["url"],
                        "total_locations": None
                    })
            else:
                failed_results.append({
                    "store": store["store"],
                    "url": store["url"],
                    "total_locations": None
                })
        except requests.RequestException as e:
            failed_results.append({
                "store": store["store"],
                "url": store["url"],
                "total_locations": None,
                "error": str(e)
            })

    return success_results, failed_results

# Example usage
if __name__ == "__main__":
    # Example array of stores

    success_results, failed_results = find_locations_for_stores(stores)

    # Save successful results to a file
    with open("successful_results.json", "w") as success_file:
        import json
        json.dump(success_results, success_file, indent=4)

    # Save failed results to a file
    with open("failed_results.json", "w") as failed_file:
        json.dump(failed_results, failed_file, indent=4)

    print(f"Saved {len(success_results)} successful results and {len(failed_results)} failed results.")
