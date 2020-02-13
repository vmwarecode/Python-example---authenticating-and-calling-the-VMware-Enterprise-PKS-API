import requests
import json
import urllib3
urllib3.disable_warnings()
​
pks_user = "api-user"
pks_pass = "Super$ecretP@ssword!"
pks_auth_headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
pks_auth_url = "https://pks-api.cmbu.local:8443/oauth/token"
pks_auth_data = { "grant_type": "client_credentials"}
​
do_not_delete = ["cluster-i-want-to-keep-1", "cluster-i-want-to-keep-2"]
​
session = requests.Session()
session.auth = (pks_user, pks_pass)
​
response = session.post(pks_auth_url, headers=pks_auth_headers, data=pks_auth_data, verify=False)
​
if response.status_code == 200:
    json_data = json.loads(response.content.decode("utf-8"))
    pks_api_bearer_token = json_data["access_token"]
else:
    print(response.status_code)
​
# Get all Clusters
pks_api_url = "https://pks-api.cmbu.local:9021/v1/clusters"
pks_api_headers = {"Accept": "application/json", "Authorization": "Bearer %s" %pks_api_bearer_token}
​
response = requests.get(pks_api_url, headers=pks_api_headers, verify=False)
​
if response.status_code == 200:
    json_data = json.loads(response.content.decode("utf-8"))
    #print(json.dumps(json_data, indent=4))
    for cluster in json_data:
        if cluster["name"] in do_not_delete:
            print("Cluster %s will not be deleted" %cluster["name"])
        else:
            print("Deleting cluster %s" %cluster["name"])
            delete_response = requests.delete("%s/%s" %(pks_api_url,cluster["name"]), headers=pks_api_headers, verify=False)
            if delete_response.status_code == 204:
                print("Delete submitted")
else:
    print(response.status_code)