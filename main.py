import requests

api_key = "SqlrA0u8IKunPO6cFkbxyxPt0tkauVA4swgayyAs"

response = requests.get(
    "https://api.api-ninjas.com/v1/caloriesburned",
    headers={"X-Api-Key": api_key},
    params={"activity": "running"}  
)

print(response.status_code)
print(response.json())


def träningslogg():
    
    pass