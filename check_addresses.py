import csv
import requests

# Do POST request with address info and return "resultStatus" from server


def check_address(url, headers, address):
    responce = requests.post(url=url, headers=headers,
                             data={
                                 "companyName": address['Company'],
                                 "address1": address['Street'],
                                 "address2": address['St'],
                                 "city": address['City'],
                                 "state": address['St'],
                                 "urbanCode": "",
                                 "zip": address['ZIPCode']
                             })

    return responce.json()["resultStatus"]


def main():

    # Read addresses into list "addresses" from file and add column "IsValid"
    addresses = []

    with open("addresses.csv", "r") as file:
        reader = csv.DictReader(file)
        for address in reader:
            address["IsValid"] = ""
            addresses.append(address)

    # URL address for get address info from server
    url = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    # Open file for write info
    with open("addresses.csv", "w", newline='') as file:

        # Get titles for each column and write to file
        fieldnames = [key for key in addresses[0].keys()]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Check each address for validity. Address is valid if "resultStatus" = "SUCCESS"
        for address in addresses:
            if check_address(url, headers, address) == "SUCCESS":
                address['IsValid'] = "Yes"
            else:
                address['IsValid'] = "No"
            writer.writerow(address)


if __name__ == "__main__":
    main()
