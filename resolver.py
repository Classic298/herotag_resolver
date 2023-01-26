import requests
import threading
import time

def resolve_herotag(herotag, addresses):
    # Resolves each herotag
    url = f"https://api.multiversx.com/usernames/{herotag}"
    response = requests.get(url)
    # Checks, if response is not 200. If that's the case, herotag not found
    if response.status_code != 200:
        print(f'herotag {herotag} could not be resolved')
        return
    # Otherwise, get the address from the reponse and add it to the list of addresses
    address = response.json()["address"]
    addresses.append((herotag, address))

def resolve_herotags(filepath, new_filepath):
    addresses = []
    # Opens the provided file in read only mode
    with open(filepath, "r") as file:
        threads = []
        for line in file:
            # API rate limit
            time.sleep(1.5)
            # Get next line
            herotag = line.strip()
            # Start thread and call the resolve function
            t = threading.Thread(target=resolve_herotag, args=(herotag, addresses))
            # Start thread
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    
    with open(new_filepath, "w") as new_file:
        # Write back the resolved addresses in a new file
        for herotag, address in addresses:
            new_file.write(f"{address}\n")
    # Also return the addresses
    return addresses

# Specifies input and output file
filepath = "herotags.txt"
new_filepath = "addresses.txt"

# Calls the main function and prints the returned, resolved addresses in the end
print(resolve_herotags(filepath, new_filepath))
