import requests

def resolve_herotag(herotags):
    # Resolves each herotag
    url = "https://index.multiversx.com/accounts/_search"
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "userName.keyword": herotags
                        }
                    }
                ]
            }
        },
        "size": 10000
    }
    response = requests.post(url=url, json=body).json()
    
    # Iterates through all hits
    hits = response["hits"]["hits"]
    output = {}

    for hit in hits:
        output[hit["_source"]["userName"]] = hit["_id"]

    return output

# Reads the file herotags.txt and puts its content into a list
with open("herotags.txt", "r") as f:
    herotags = [line.strip().replace('@', '') if line.strip().endswith('.elrond') else line.strip().replace('@', '')+'.elrond' for line in f]

# Calls the main function
resolved = resolve_herotag(herotags)

# Open the file for writing addresses
with open("addresses.txt", "w") as f:
    for herotag in herotags:
        if herotag in resolved:
            # Write the address into the file
            f.write(resolved[herotag] + "\n")
        else:
            # Print the herotag that could not be resolved
            print(f"Could not resolve herotag: {herotag}")
