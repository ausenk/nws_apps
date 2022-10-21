import requests, json

API_KEY = 'AIzaSyCdef3DwKdvBXru6-4inxQdgSOc9lFr-0M'

class GoogleDirections():
    def __init__(self, trip):
        self.trip = trip

    def __ApiCall(self, url, headers, payload):
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            # return json.loads(response.content.decode('utf-8'))
            return response.text
        else:
            return None

    def GetDirections(self):

        origin = self.trip["origin"]
        destination = self.trip["destination"]
        if self.trip["waypoints"] != "":
            waypoints = "&waypoints="
            for waypoint in self.trip["waypoints"]:
                waypoints = waypoints + "|" + waypoint

        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}{waypoints}&key={API_KEY}'
        # url = 'https://maps.googleapis.com/maps/api/staticmap?size=400x400&center=59.900503,-135.478011&zoom=4&path=weight:3%7Ccolor:orange%7Cenc:_fisIp~u%7CU}%7Ca@pytA_~b@hhCyhS~hResU%7C%7Cx@oig@rwg@amUfbjA}f[roaAynd@%7CvXxiAt{ZwdUfbjAewYrqGchH~vXkqnAria@c_o@inc@k{g@i`]o%7CF}vXaj\h`]ovs@?yi_@rcAgtO%7Cj_AyaJren@nzQrst@zuYh`]v%7CGbldEuzd@%7C%7Cx@spD%7CtrAzwP%7Cd_@yiB~vXmlWhdPez\_{Km_`@~re@ew^rcAeu_@zhyByjPrst@ttGren@aeNhoFemKrvdAuvVidPwbVr~j@or@f_z@ftHr{ZlwBrvdAmtHrmT{rOt{Zz}E%7Cc%7C@o%7CLpn~AgfRpxqBfoVz_iAocAhrVjr@rh~@jzKhjp@``NrfQpcHrb^k%7CDh_z@nwB%7Ckb@a{R%7Cyh@uyZ%7CllByuZpzw@wbd@rh~@%7C%7CFhqs@teTztrAupHhyY}t]huf@e%7CFria@o}GfezAkdW%7C}[ocMt_Neq@ren@e~Ika@pgE%7Ci%7CAfiQ%7C`l@uoJrvdAgq@fppAsjGhg`@%7ChQpg{Ai_V%7C%7Cx@mkHhyYsdP%7CxeA~gF%7C}[mv`@t_NitSfjp@c}Mhg`@sbChyYq}e@rwg@atFff}@ghN~zKybk@fl}A}cPftcAite@tmT__Lha@u~DrfQi}MhkSqyWivIumCria@ciO_tHifm@fl}A{rc@fbjAqvg@rrqAcjCf%7Ci@mqJtb^s%7C@fbjA{wDfs`BmvEfqs@umWt_Nwn^pen@qiBr`xAcvMr{Zidg@dtjDkbM%7Cd_@&key=' + API_KEY

        payload={}
        headers = {}

        return self.__ApiCall(url, headers, payload)


trip = {
    "origin" : "Logan, UT",
    "destination" :"Rexburg, ID",
    "waypoints" : ["Preston, ID", "Idaho Falls, ID"]
}

idaho_trip = GoogleDirections(trip)
print(idaho_trip.GetDirections())