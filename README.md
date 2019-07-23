# Success Rate Report - POC
- This is a POC and is not intended for production use and only as a demo of how to start aggregating data from remote API endpoints.

- Depends on:
  - python>=3.6
  - a hostsfile containing lists of server inventory
- Usage:

##

    git clone https://github.com/M3hran/success_report.git && cd ./success_report && python3 success_report.py hostsfile 4
    
##

- Notes:
  - the application requires python3 
  - if there is an error in executing the command, you will be notified with correct usage parameters.
  - you may specify the number of worker threads to help speed up the scripts data gathering in large deployments.
  - Usage: **python3 success_report.py /path/to/hostsfile optional_number_of_worker_threads**

- Output:
  - Success Rate of responses are calculated by Applicaton by Version's total number of successful responses divided by total number of responses.
  - The results are printed to stdout in the following format:
    - App_Name
      - Version    Success_Rate %
  - A **results.json** file is also created in the $PWD containing the dictionary of the same data.
              
 
 # What's Next:
- Build a frontend API CRUD wrapper for the backend logic. 
- Dockerize the app and make avaialable via http.
- Encrypt the API endpoint traffic with TLS. 
- Store historical timeseries in Redis for persistance, and downstream consumption into a dashboarding tool like grafana, Kibana, Splunk, etc. 


