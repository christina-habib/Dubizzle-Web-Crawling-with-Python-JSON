import requests
import json
import pandas as pd

# Define the starting page
current_page = 400
url = "https://wd0ptz13zs-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.11.0)%3B%20Browser%20(lite)&x-algolia-api-key=cef139620248f1bc328a00fddc7107a6&x-algolia-application-id=WD0PTZ13ZS"

headers = {"Content-Type": "application/json"}
car_details_list = []

while current_page >= 0:
    payload = json.dumps(
        {
            "requests": [
                {
                    "indexName": "motors.com",
                    "query": "",
                    "params": f"page={current_page}&attributesToHighlight=%5B%5D&hitsPerPage=25&attributesToRetrieve=%5B%22is_premium%22%2C%22is_featured_agent%22%2C%22location_list%22%2C%22objectID%22%2C%22name%22%2C%22price%22%2C%22neighbourhood%22%2C%22agent_logo%22%2C%22can_chat%22%2C%22has_whatsapp_number%22%2C%22details%22%2C%22photo_thumbnails%22%2C%22photos%22%2C%22highlighted_ad%22%2C%22absolute_url%22%2C%22id%22%2C%22category_id%22%2C%22uuid%22%2C%22category%22%2C%22has_phone_number%22%2C%22category_v2%22%2C%22photos_count%22%2C%22created_at%22%2C%22site%22%2C%22permalink%22%2C%22has_vin%22%2C%22auto_agent_id%22%2C%22is_trusted_seller%22%2C%22show_trusted_seller_logo%22%2C%22trusted_seller_logo%22%2C%22trusted_seller_id%22%2C%22created_at%22%2C%22added%22%2C%22jobs_logo%22%2C%22vas%22%2C%22seller_type%22%2C%22is_verified_user%22%2C%22has_video%22%2C%22cotd_on%22%2C%22is_super_ad%22%2C%22categories%22%2C%22city%22%2C%22bedrooms%22%2C%22bathrooms%22%2C%22size%22%2C%22neighborhoods%22%2C%22agent%22%2C%22room_type%22%2C%22is_reserved%22%2C%22is_coming_soon%22%2C%22inventory_type%22%5D&filters=(%22category_v2.slug_paths%22%3A%22motors%2Fused-cars%22)",
                }
            ]
        }
    )

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        print(f"Request was successful for page {current_page}!")
        response_json = response.json()
        hits = response_json.get("results", [{}])[0].get("hits", [])
        
        for hit in hits:
            details = hit.get("details", {})
            car_detail = {
                "Year": details.get("Year", {}).get("en", {}).get("value", ""),
                "Kilometers": details.get("Kilometers", {}).get("en", {}).get("value", ""),
                "Regional Specs": details.get("Regional Specs", {}).get("en", {}).get("value", ""),
                "Make": details.get("Make", {}).get("en", {}).get("value", ""),
                "Model": details.get("Model", {}).get("en", {}).get("value", ""),
                "Price": hit.get("price", ""),
            }
            car_details_list.append(car_detail)
    else:
        print(f"Request failed with status code: {response.status_code} for page {current_page}")
        print("Response text:", response.text)

    current_page -= 1

car_details_df = pd.DataFrame(car_details_list)
car_details_df.to_excel("car_details.xlsx", index=False)
print(car_details_df)
