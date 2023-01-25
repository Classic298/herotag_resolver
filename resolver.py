"""This code uses the open function to read the file located at the specified filepath and then
uses the requests library to send a GET request to the MultiversX API for each herotag in the file,
one by one. It extracts the "address" field from the JSON response to build a list of addresses."""
import requests

def resolve_herotags(filepath):
    addresses = []
    with open(filepath, "r") as file:
        for line in file:
            herotag = line.strip()
            url = f"https://api.multiversx.com/usernames/{herotag}"
            response = requests.get(url)
            address = response.json()["address"]
            addresses.append(address)
    return addresses

    with open(new_filepath, "w") as new_file:
            for address in addresses:
                new_file.write(address + "\n")
        return addresses

filepath = "herotags.txt"
new_filepath = "addresses.txt"

print(resolve_herotags(filepath, new_filepath))
