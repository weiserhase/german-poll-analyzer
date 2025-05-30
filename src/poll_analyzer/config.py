
import ssl

# Bypass SSL verification if needed
ssl._create_default_https_context = ssl._create_unverified_context

PARTY_COLORS = {
    "CDU/CSU": "#262626",
    "SPD":     "#ff1507",
    "GRÜNE":   "#00be00",
    "FDP":     "#ffb700",
    "LINKE":   "#c3005d",
    "AfD":     "#0e63cb",
    "Sonstige": "#a0a0a0",
    "FW":      "#5a616c",
    "BSW":     "#9a00ad",
}

PARTIES_TO_PLOT = [
    "CDU/CSU", "SPD", "GRÜNE",
    "FDP", "LINKE", "AfD",
    "BSW", "FW", "Sonstige"
]
# WAHLRECHT_URL = "https://www.wahlrecht.de/umfragen/insa.htm"
URLS = {
    "Allensbach": "https://www.wahlrecht.de/umfragen/allensbach.htm",
    "Emnid": "https://www.wahlrecht.de/umfragen/emnid.htm",
    "Forsa": "https://www.wahlrecht.de/umfragen/forsa.htm",
    # "GMS": "https://www.wahlrecht.de/umfragen/gms.htm",
    "Infratest dimap": "https://www.wahlrecht.de/umfragen/dimap.htm",
    "Insa": "https://www.wahlrecht.de/umfragen/insa.htm",
    "YouGov": "https://www.wahlrecht.de/umfragen/yougov.htm",
}
WAHLRECHT_URL =  URLS["YouGov"] 
