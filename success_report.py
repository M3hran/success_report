import os
import sys
import json
import traceback
import requests
from concurrent.futures import ThreadPoolExecutor

# fetch url


def get_response(url):
    response = requests.get(url)
    return response

# query the server's status api


def query_servers(hostsfile, num_workers):

    data = []
    # read servernames from hostfile and fetch status
    with open(hostsfile, 'r') as file:
        # for server in file:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for server in file:
                server = server.strip()
                url = "http://"+server+"/status"

                # fetch from remote URL
                try:
                    response = executor.submit(get_response, url)
                    response = response.result()
                    response.raise_for_status()

                # catch failure case for Unavaialble URLs
                except (requests.ConnectionError, requests.Timeout) as e:
                    print("Connection Error: " + url)
                # catch failure case for HTTP response errors (not 200 status code)
                except requests.exceptions.HTTPError as e:
                    print("Error: " + str(e))
                # must have been 200 status code
                else:
                    # save response
                    try:
                        data.append(response.json())
                    except Exception:
                        print("##### There was an Error:")
                        traceback.print_exc()
                        sys.exit()
    return data

# display report on stdout


def print_success_report(d):
    for i in sorted(d):
        print("Application:", i)
        for j in sorted(d[i]):
            print("Version:", j, "     Success Rate:",
                  "{:.0%}".format(d[i][j]["Success_Ratio"]), end="\n")

# aggregate data and calc success ratio per App per Version


def aggregate(data):

    d = {}
    for i in data:
        # find each unique app
        if(i["Application"] not in d):
            app = i["Application"]
            d[app] = {}
            for j in data:
                # find and aggregate each version's stats
                if (j["Application"] == i["Application"]):
                    if (j["Version"] not in d[app]):
                        ver = j["Version"]
                        d[app][ver] = {
                            "Request_Count": j["Request_Count"], "Success_Count": j["Success_Count"]}
                    else:
                        d[app][ver]["Request_Count"] += j["Request_Count"]
                        d[app][ver]["Success_Count"] += j["Success_Count"]
    # calculate success rate based on aggregareted Success_count,Request_Count for each version of each app.
    for j in d:
        for k in d[j]:
            d[j][k]["Success_Ratio"] = round(d[j][k]["Success_Count"] /
                                             d[j][k]["Request_Count"], 2)

    return d

# Main function


def main():

    try:
        hostsfile = sys.argv[1]
    except Exception:
        print(
            "Usage: python3 success_report.py 'hostsfile.txt' optional:'number_of_workers'")
        sys.exit()

    else:
        if(not os.path.isfile(hostsfile)):
            print("hostsfile: "+hostsfile+" was not found!")
            sys.exit()
        try:
            num_workers = sys.argv[2]
        except Exception:
            num_workers = None
            pass
        else:
            if (not num_workers.isdigit() and num_workers is not None):
                print(
                    "Usage: python3 success_report.py 'hostsfile.txt' optional:'number_of_workers'")
                sys.exit()

        # Query the servers' status
        try:
            data = query_servers(
                hostsfile, num_workers=2 if num_workers is None else int(num_workers))
        except Exception:
            print("##### There was an Error:")
            traceback.print_exc()

        # Aggregate data
        else:
            # jsonFile = open('responses.txt', 'r')
            # data = json.load(jsonFile)
            try:
                results = aggregate(data)
            except Exception:
                print("##### There was an Error:")
                traceback.print_exc()

            # Display Success Report on stdout and save to json file
            else:
                # jsonFile.close()

                try:
                    print_success_report(results)
                    with open("results.json", "w") as file:
                        json.dump(results, file, indent=4, sort_keys=True)
                except Exception:
                    print("##### There was an Error:")
                    traceback.print_exc()


if __name__ == "__main__":
    main()
