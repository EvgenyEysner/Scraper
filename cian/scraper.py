import random
import requests
import json
import urllib.request
from fake_useragent import UserAgent

from django.core.files import File

from .models import Apartment, Image, Task

ua = UserAgent()

headers = {"User-Agent": ua.random, "Accept": "*/*"}

start_json_template = "window._cianConfig['frontend-offer-card'] = "

# proxy = {
#
#      'https': 'http://186.65.114.25:9898',
#      'http': 'http://186.65.114.25:9898'
# }


def get_page_data(url):
    with requests.get(url, headers=headers, timeout=random.randint(1, 5)) as response:
        html = response.text
        if start_json_template in html:  # get json from website
            start = html.index(start_json_template) + len(start_json_template)
            end = html.index("</script>", start)
            json_raw = html[start:end].strip()[:-1]
            js = json.loads(json_raw)

            for item in js:
                apartments = []
                if item["key"] == "defaultState":
                    try:
                        price = item["value"]["offerData"]["offer"]["bargainTerms"][
                            "price"
                        ]
                    except:
                        price = None
                    try:
                        floor = item["value"]["offerData"]["offer"]["floorNumber"]
                    except:
                        floor = None
                    try:
                        desc = item["value"]["offerData"]["offer"]["description"]
                    except:
                        desc = None
                    try:
                        region = item["value"]["offerData"]["offer"]["geo"]["address"][
                            0
                        ]["fullName"]
                    except:
                        region = None
                    try:
                        town = item["value"]["offerData"]["offer"]["geo"]["address"][1][
                            "fullName"
                        ]
                    except:
                        town = None
                    try:
                        street = item["value"]["offerData"]["offer"]["geo"]["address"][
                            -2
                        ]["fullName"]
                    except:
                        street = None
                    try:
                        house_number = item["value"]["offerData"]["offer"]["geo"][
                            "address"
                        ][-1]["fullName"]
                    except:
                        house_number = None
                    try:
                        address = (
                            region + ", " + town + ", " + street + " " + house_number
                        )
                        # address = item['value']['offerData']['offer']['geo']['address']
                    except:
                        address = None
                    try:
                        rooms = item["value"]["offerData"]["offer"]["roomsCount"]
                    except:
                        rooms = None
                    try:
                        commission = item["value"]["offerData"]["offer"][
                            "bargainTerms"
                        ]["agentFee"]
                    except:
                        commission = None
                    try:
                        photos = []

                        for photo in item["value"]["offerData"]["offer"]["photos"]:
                            photos.append(photo["fullUrl"])
                    except:
                        photos = None
                    apartments.append(
                        {
                            "rooms": rooms,
                            "price": price,
                            "address": address,
                            "desc": desc,
                            "floor": floor,
                            "photos": photos,
                            "commission": commission,
                        }
                    )
                    return apartments


def save_data(apartments_list, user):  # save the scraped data to the database
    for ap in apartments_list:
        try:
            apartment = Apartment.objects.create(
                owner=user,
                rooms=ap["rooms"],
                price=ap["price"],
                address=ap["address"],
                desc=ap["desc"],
                floor=ap["floor"],
                commission=ap["commission"],
            )
            for image in ap["photos"]:
                im = Image()
                pic = urllib.request.urlretrieve(image)[0]  # download images
                im.img.save(
                    image, File(open(pic, "rb"))
                )  # save images to media directory
                im.apartment_id = apartment.pk
                im.save()

        except Exception as e:
            print(e)
            break
