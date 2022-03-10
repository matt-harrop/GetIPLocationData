import ipaddress
from requests import get
import csv

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Getting IP Addresses...')

    # Get List of IP Addresses

    f = open('ips.txt', 'r')
    lines = f.readlines()

    # Check if IP is single address or CIDR block, either way add them to array of IPs

    ip_addresses = []
    for line in lines:
        if '/' in line:
            try:
                for ip in ipaddress.IPv4Network(line.strip('\n'), False):
                    ip_addresses.append(str(ip))
            except ValueError:
                print(f'***There was an error in a potential address block provided ({line}); maybe host bits were set that shouldn\'t be?\n')
        else:
            stripped_line = line.strip('\n')
            ip_addresses.append(stripped_line)
    print(f'IP Count: {len(ip_addresses)}')

    # Look up IP address data
    # Using a free API: 'ipapi.co'

    print('Looking up location data for list of IP addresses...')
    location_fields = ['ip', 'city', 'region', 'country_name', 'postal', 'timezone', 'org']
    location_dict = {}
    for ip in ip_addresses:
        location_data = get(f'https://ipapi.co/{ip}/json/')
        location_dict[location_data.json()["ip"]] = {}
        for item in location_data.json():
            if item in location_fields:
                location_dict[location_data.json()["ip"]][item] = location_data.json()[item]

    # Report results to output

    summary = {}

    for item in location_dict:
        print(f'\nLocation Results for {item}:')
        for sub_item in location_dict[item]:
            print(f'\t{sub_item}: {location_dict[item][sub_item]}')
            # Check to see if city name is a key in the summary dict:
            # if sub_item == 'city':
            #     city_name = location_dict[item][sub_item]
            #     # if location_dict[item][sub_item] not in summary.keys():
            #     #     summary[location_dict[item][sub_item]] = location_dict[item][sub_item]
            #     if city_name not in summary.keys():
            #         summary[city_name] = 1
            #     else:
            #         summary[city_name] += 1
                    # count = summary[city_name]
                    # summary[city_name] = count + 1
        region = location_dict[item]['city'] + ", " + location_dict[item]['country_name']
        if region not in summary.keys():
            summary[region] = 1
        else:
            summary[region] += 1

    print('\n#######################################')
    print(f'\nResults Summary:')
    print(f'\tIP Count: {len(ip_addresses)}')
    for item in summary:
        print(f'\t{item}: {summary[item]}')



    # Store Results in a file

    with open(f'ip_location_results_{ip_addresses[0]}.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(location_fields)
        for ip in location_dict:
            filewriter.writerow(location_dict[ip].values())
        filewriter.writerow([])
        filewriter.writerow(['Summary:'])
        for region in summary:
            region_formatted = str(region).replace(',', ' -')
            filewriter.writerow([region_formatted, summary[region]])

