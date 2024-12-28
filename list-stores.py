from stores import stores
import requests

def find_404_stores(stores):
    """
    Filters stores whose URLs return a 404 error.

    Args:
        stores (list): List of dictionaries with "store" and "url" keys.

    Returns:
        list: List of stores with URLs returning 404.
    """
    stores_with_404 = []

    for store in stores:
        try:
            response = requests.get(store["url"], timeout=10)
            if response.status_code == 404:
                stores_with_404.append(store)
            else:
                print(store["url"],"is okay")
        except requests.RequestException as e:
            print(f"Error checking URL {store['url']}: {e}")

    return stores_with_404

# Find stores with 404 URLs
stores_with_404 = find_404_stores(stores)

# Print the filtered array
print(stores_with_404)