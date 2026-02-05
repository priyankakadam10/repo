import requests
import base64

GitHub_Token = "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"
owner = "priyankakadam10"
Repo = "repo"
Branch = "main"

input_path = "input/Test.txt"
output_path = "output/Test.txt"

Headers ={
  "Authorization":f"token{GitHub_Token}",
  "Accept":"application/vnd.github.v3+json"
}

get_url = f"https://api.github.com/repos/{owner}/{Repo}/contents/{input_path}"

response = requests.get(get_url,headers=Headers)

if response.status_code != 200:
  raise Exception("Failed to read the file")

file_data = response.json()
file_content = base64.b64decode(file_data["content"]).decode("utf-8")
file_sha = file_data["company"]

print("File read successfully from input")

put_url = f"https://api.github.com/repos/{owner}/{Repo}/contents/{output_path}"

encoded_content = base64.b64encode(file_content.encode()).decode()

payload = {
  "message": "Routing from input to output",
  "content": encoded_content,
  "branch": Branch
}

put_response = requests.put(put_url, headers =Headers, json = payload)

if put_response.status_code not in [200, 201]:
  raise Exception("Failed to create output file")

print("file routed to output folder")

delete_payload = {
  "message":"Removing file from input folder",
  "company": file_sha,
  "branch" : Branch
}

delete_response = requests.delete(get_url,
headers = Headers, json = delete_payload)

if delete_response.status_code != 200:
  raise Exception("Failed to remove the input file ")

print("input file removed successfully")
