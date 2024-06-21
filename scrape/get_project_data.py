import re
import json
import html
from bs4 import BeautifulSoup
from utils._request import send_request
from utils.logger import logger


def get_project_data(site_url: str, link: str) -> dict | None:
    try:
        project_url = f"{site_url}{link}"
        response = send_request(project_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Get the Script containing the Property Data
            script_content = soup.find("script", id="initialState").string
            json_match = re.search(r'JSON\.parse\("(.+)"\)', script_content)
            json_str = json_match.group(1)
            unescaped_json_str = html.unescape(json_str)
            cleaned_json_str = unescaped_json_str.replace('\\"', '"').replace(
                "\\\\", "\\"
            )
            parsed_json = json.loads(cleaned_json_str)

            # Fetch Property details
            propertyDetails = parsed_json["propertyDetails"]["details"]

            # Get Title
            property_title = propertyDetails["title"]

            # Get BHK units
            bhk_units = propertyDetails["subtitle"]

            # Get Property Cost Range
            property_cost_range = []
            for config in propertyDetails["details"]["config"]["propertyConfig"]:
                property_cost_range.append(
                    {
                        "label": config["label"],
                        "range": config["range"],
                    }
                )

            # Get Launch Date
            launch_date = next(
                (
                    point["description"]
                    for point in propertyDetails["details"]["overviewPoints"]
                    if point["id"] == "launchDate"
                ),
                None,
            )

            # Get Description
            about_project = soup.find("section", {"id": "aboutProject"})
            description = (
                about_project.find("div", {"data-q": "desc"}).text
                if about_project
                else ""
            )

            # Get Amenities
            amenities = list(propertyDetails["clubhouse"]["amenities_hash"].keys())

            # Get Locality Guide
            locality_guide = {"description": "", "read_more": ""}
            # locality_section = soup.find("section", id="locality")
            # if locality_section:
            #     if locality_section.find("div", {"data-q": "desc"}).find_all("span"):
            #         locality_guide["description"] = (
            #             locality_section.find("div", {"data-q": "desc"})
            #             .find_all("span")[1]
            #             .get_text()
            #         )

            #     read_more = locality_section.find("a")
            #     if read_more:
            #         locality_guide["read_more"] = read_more.get("href")

            # Get Map Location
            map_location = {"latitude": "", "longitude": ""}
            coordinates = propertyDetails["coords"]
            if coordinates:
                map_location["latitude"] = coordinates[0]
                map_location["longitude"] = coordinates[1]

            # Get Seller Contacts
            seller_contacts = []
            for seller in propertyDetails["sellers"]:
                seller_contacts.append(
                    {
                        "name": seller["name"],
                        "designation": seller["designation"],
                        "phone": seller["phone"]["partialValue"],
                    }
                )

            return {
                "title": property_title,
                "project_url": project_url,
                "bhk_units": bhk_units,
                "property_cost_range": property_cost_range,
                "launch_date": launch_date,
                "description": description,
                "amenities": amenities,
                "locality_guide": locality_guide,
                "map_location": map_location,
                "seller_contacts": seller_contacts,
            }
        else:
            logger.error(f"{response.status_code}, Project page not working.")
            return None
    except Exception as e:
        logger.error(e)
