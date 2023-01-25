"""This code uses the threading library to create a new thread for each herotag to be resolved.
Each thread runs the function resolve_herotag which takes the herotag and a list of addresses as
arguments. The function uses the requests library to send a GET request to the MultiversX API to
resolve the herotag into an address. If the status code of the response is not 200, it means the
herotag could not be resolved and it prints an informative message, otherwise, it adds the herotag
and the resolved address to the list of addresses.

The main thread waits for all the worker threads to finish by calling join() method on each thread
object before writing the results to the new file and returning the list of addresses."""
import requests
import threading

def resolve_herotag(herotag, addresses):
    url = f"https://api.multiversx.com/usernames/{herotag}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f'herotag {herotag} could not be resolved')
        return
    address = response.json()["address"]
    addresses.append((herotag, address))

def resolve_herotags(filepath, new_filepath):
    addresses = []
    with open(filepath, "r") as file:
        threads = []
        for line in file:
            herotag = line.strip()
            t = threading.Thread(target=resolve_herotag, args=(herotag, addresses))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    
    with open(new_filepath, "w") as new_file:
        for herotag, address in addresses:
            new_file.write(f"{address}\n")
    return addresses

filepath = "herotags.txt"
new_filepath = "addresses.txt"

print(resolve_herotags(filepath, new_filepath))
