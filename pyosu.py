import requests
import json

def pnum(n):
    return str(round(float(n)))

class Osu(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://osu.ppy.sh/api/"

    def player(self, username):
        p = {
            "k": self.api_key,
            "u": username,
        }

        data = requests.get(self.api_url+"get_user", params=p).text
        data = json.loads(data)

        print(data)

        if data == []:
            return None
        else:


            output = {
                "profile": {
                    "name": data[0]["username"],
                    "user_id": data[0]['user_id'],
                    "level": pnum(data[0]['level']),
                    "country": data[0]['country'],
                    "top": {
                        "world": data[0]['pp_rank'],
                        "local": data[0]['pp_country_rank'],
                    },
                },
        
                "game": {
                    "pp": pnum(data[0]['pp_raw']),
                    "accuracy": pnum(data[0]['accuracy'])+"%",
                    "playcount": data[0]['playcount'],
                    "gametime": pnum(int(data[0]['total_seconds_played'])/3600),
                    "total": {
                        "ss": data[0]['count_rank_ss'],
                        "s": data[0]['count_rank_s'],
                        "a": data[0]['count_rank_a'],
                    },
                },

                "misc": {
                    "join_date": data[0]['join_date'].split(" ")[0],
                    "image_url": "https://a.ppy.sh/"+data[0]['user_id']
                },
            }

            return output


