"""Global location catalog for continent/country/locality selection."""
from __future__ import annotations

from astronomy.data_models import GeoLocation


def _loc(
    name: str,
    region: str,
    country: str,
    latitude: float,
    longitude: float,
    timezone: str,
) -> GeoLocation:
    return GeoLocation(
        name=name,
        region=region,
        country=country,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
    )


WORLD_LOCATIONS: dict[str, dict[str, list[GeoLocation]]] = {
    "Europe": {
        "Germany": [
            _loc("Berlin", "Berlin", "Germany", 52.5200, 13.4050, "Europe/Berlin"),
            _loc("Hamburg", "Hamburg", "Germany", 53.5511, 9.9937, "Europe/Berlin"),
            _loc("Munich", "Bavaria", "Germany", 48.1351, 11.5820, "Europe/Berlin"),
            _loc("Cologne", "North Rhine-Westphalia", "Germany", 50.9375, 6.9603, "Europe/Berlin"),
            _loc("Frankfurt", "Hesse", "Germany", 50.1109, 8.6821, "Europe/Berlin"),
            _loc("Ulm", "Baden-Wurttemberg", "Germany", 48.4011, 9.9876, "Europe/Berlin"),
            _loc("Freiburg", "Baden-Wurttemberg", "Germany", 47.9990, 7.8421, "Europe/Berlin"),
            _loc("Sasbach am Kaiserstuhl", "Baden-Wurttemberg", "Germany", 48.0847, 7.6372, "Europe/Berlin"),
        ],
        "Norway": [
            _loc("Oslo", "Oslo", "Norway", 59.9139, 10.7522, "Europe/Oslo"),
            _loc("Tromso", "Troms", "Norway", 69.6492, 18.9553, "Europe/Oslo"),
            _loc("Longyearbyen", "Svalbard", "Norway", 78.2232, 15.6469, "Arctic/Longyearbyen"),
            _loc("Bodö", "Nordland", "Norway", 67.2831, 14.4086, "Europe/Oslo"),
            _loc("Trondheim", "Trøndelag", "Norway", 63.4305, 10.3951, "Europe/Oslo"),
            _loc("Svolvaer", "Nordland", "Norway", 68.2232, 14.5667, "Europe/Oslo"),
            _loc("Narvik", "Nordland", "Norway", 68.4344, 17.4265, "Europe/Oslo"),
        ],
        "United Kingdom": [
            _loc("London", "England", "United Kingdom", 51.5074, -0.1278, "Europe/London"),
            _loc("Edinburgh", "Scotland", "United Kingdom", 55.9533, -3.1883, "Europe/London"),
            _loc("Manchester", "England", "United Kingdom", 53.4808, -2.2426, "Europe/London"),
        ],
        "France": [
            _loc("Paris", "Ile-de-France", "France", 48.8566, 2.3522, "Europe/Paris"),
            _loc("Marseille", "Provence-Alpes-Cote d'Azur", "France", 43.2965, 5.3698, "Europe/Paris"),
            _loc("Lyon", "Auvergne-Rhone-Alpes", "France", 45.7640, 4.8357, "Europe/Paris"),
        ],
        "Spain": [
            _loc("Madrid", "Community of Madrid", "Spain", 40.4168, -3.7038, "Europe/Madrid"),
            _loc("Barcelona", "Catalonia", "Spain", 41.3851, 2.1734, "Europe/Madrid"),
            _loc("Seville", "Andalusia", "Spain", 37.3891, -5.9845, "Europe/Madrid"),
        ],
        "Italy": [
            _loc("Rome", "Lazio", "Italy", 41.9028, 12.4964, "Europe/Rome"),
            _loc("Milan", "Lombardy", "Italy", 45.4642, 9.1900, "Europe/Rome"),
            _loc("Naples", "Campania", "Italy", 40.8518, 14.2681, "Europe/Rome"),
            _loc("Genova", "Liguria", "Italy", 44.4056, 8.9463, "Europe/Rome"),
            _loc("Torino", "Piedmont", "Italy", 45.0703, 7.6869, "Europe/Rome"),
            _loc("Vasto", "Abruzzo", "Italy", 42.1803, 14.7121, "Europe/Rome"),
            _loc("Bari", "Apulia", "Italy", 41.1175, 16.8723, "Europe/Rome"),
            _loc("Palermo", "Sicily", "Italy", 38.1156, 13.3615, "Europe/Rome"),
            _loc("Catania", "Sicily", "Italy", 37.4979, 15.0873, "Europe/Rome"),
        ],
        "Sweden": [
            _loc("Stockholm", "Stockholm", "Sweden", 59.3293, 18.0686, "Europe/Stockholm"),
            _loc("Gothenburg", "Vastra Gotaland", "Sweden", 57.7089, 11.9746, "Europe/Stockholm"),
            _loc("Kiruna", "Norrbotten", "Sweden", 67.8558, 20.2253, "Europe/Stockholm"),
            _loc("Abisko", "Norrbotten", "Sweden", 68.3526, 18.8232, "Europe/Stockholm"),
            _loc("Boden", "Norrbotten", "Sweden", 65.3298, 21.6658, "Europe/Stockholm"),
            _loc("Lund", "Scania", "Sweden", 55.7047, 13.1910, "Europe/Stockholm"),
        ],
        "Finland": [
            _loc("Helsinki", "Uusimaa", "Finland", 60.1699, 24.9384, "Europe/Helsinki"),
            _loc("Rovaniemi", "Lapland", "Finland", 66.5039, 25.7294, "Europe/Helsinki"),
        ],
        "Poland": [
            _loc("Warsaw", "Masovian", "Poland", 52.2297, 21.0122, "Europe/Warsaw"),
            _loc("Krakow", "Lesser Poland", "Poland", 50.0647, 19.9450, "Europe/Warsaw"),
            _loc("Gdansk", "Pomeranian", "Poland", 54.3520, 18.6466, "Europe/Warsaw"),
        ],
        "Iceland": [
            _loc("Reykjavik", "Capital Region", "Iceland", 64.1466, -21.9426, "Atlantic/Reykjavik"),
            _loc("Akureyri", "Northeast", "Iceland", 65.6839, -18.1105, "Atlantic/Reykjavik"),
        ],
        "Switzerland": [
            _loc("Basel", "Basel-Stadt", "Switzerland", 47.5596, 7.5886, "Europe/Zurich"),
            _loc("Maisprach", "Basel-Landschaft", "Switzerland", 47.6265, 7.8166, "Europe/Zurich"),
        ],
    },
    "North America": {
        "United States": [
            _loc("New York", "New York", "United States", 40.7128, -74.0060, "America/New_York"),
            _loc("Los Angeles", "California", "United States", 34.0522, -118.2437, "America/Los_Angeles"),
            _loc("Chicago", "Illinois", "United States", 41.8781, -87.6298, "America/Chicago"),
            _loc("Anchorage", "Alaska", "United States", 61.2181, -149.9003, "America/Anchorage"),
            _loc("Honolulu", "Hawaii", "United States", 21.3069, -157.8583, "Pacific/Honolulu"),
        ],
        "Canada": [
            _loc("Toronto", "Ontario", "Canada", 43.6532, -79.3832, "America/Toronto"),
            _loc("Vancouver", "British Columbia", "Canada", 49.2827, -123.1207, "America/Vancouver"),
            _loc("Montreal", "Quebec", "Canada", 45.5017, -73.5673, "America/Toronto"),
            _loc("Iqaluit", "Nunavut", "Canada", 63.7467, -68.5167, "America/Iqaluit"),
        ],
        "Mexico": [
            _loc("Mexico City", "Mexico City", "Mexico", 19.4326, -99.1332, "America/Mexico_City"),
            _loc("Guadalajara", "Jalisco", "Mexico", 20.6597, -103.3496, "America/Mexico_City"),
            _loc("Monterrey", "Nuevo Leon", "Mexico", 25.6866, -100.3161, "America/Monterrey"),
        ],
        "Greenland": [
            _loc("Nuuk", "Sermersooq", "Greenland", 64.1835, -51.7216, "America/Nuuk"),
            _loc("Ilulissat", "Avannaata", "Greenland", 69.2167, -51.1000, "America/Nuuk"),
        ],
    },
    "South America": {
        "Brazil": [
            _loc("Sao Paulo", "Sao Paulo", "Brazil", -23.5505, -46.6333, "America/Sao_Paulo"),
            _loc("Rio de Janeiro", "Rio de Janeiro", "Brazil", -22.9068, -43.1729, "America/Sao_Paulo"),
            _loc("Brasilia", "Federal District", "Brazil", -15.7939, -47.8828, "America/Sao_Paulo"),
            _loc("Manaus", "Amazonas", "Brazil", -3.1190, -60.0217, "America/Manaus"),
        ],
        "Argentina": [
            _loc("Buenos Aires", "Buenos Aires", "Argentina", -34.6037, -58.3816, "America/Argentina/Buenos_Aires"),
            _loc("Cordoba", "Cordoba", "Argentina", -31.4201, -64.1888, "America/Argentina/Cordoba"),
            _loc("Ushuaia", "Tierra del Fuego", "Argentina", -54.8019, -68.3030, "America/Argentina/Ushuaia"),
        ],
        "Chile": [
            _loc("Santiago", "Santiago Metropolitan", "Chile", -33.4489, -70.6693, "America/Santiago"),
            _loc("Antofagasta", "Antofagasta", "Chile", -23.6500, -70.4000, "America/Santiago"),
            _loc("Punta Arenas", "Magallanes", "Chile", -53.1638, -70.9171, "America/Punta_Arenas"),
        ],
        "Peru": [
            _loc("Lima", "Lima", "Peru", -12.0464, -77.0428, "America/Lima"),
            _loc("Cusco", "Cusco", "Peru", -13.5319, -71.9675, "America/Lima"),
        ],
        "Colombia": [
            _loc("Bogota", "Capital District", "Colombia", 4.7110, -74.0721, "America/Bogota"),
            _loc("Medellin", "Antioquia", "Colombia", 6.2442, -75.5812, "America/Bogota"),
        ],
    },
    "Asia": {
        "China": [
            _loc("Beijing", "Beijing", "China", 39.9042, 116.4074, "Asia/Shanghai"),
            _loc("Shanghai", "Shanghai", "China", 31.2304, 121.4737, "Asia/Shanghai"),
            _loc("Guangzhou", "Guangdong", "China", 23.1291, 113.2644, "Asia/Shanghai"),
            _loc("Urumqi", "Xinjiang", "China", 43.8256, 87.6168, "Asia/Shanghai"),
        ],
        "India": [
            _loc("Delhi", "Delhi", "India", 28.6139, 77.2090, "Asia/Kolkata"),
            _loc("Mumbai", "Maharashtra", "India", 19.0760, 72.8777, "Asia/Kolkata"),
            _loc("Bengaluru", "Karnataka", "India", 12.9716, 77.5946, "Asia/Kolkata"),
            _loc("Kolkata", "West Bengal", "India", 22.5726, 88.3639, "Asia/Kolkata"),
        ],
        "Japan": [
            _loc("Tokyo", "Tokyo", "Japan", 35.6762, 139.6503, "Asia/Tokyo"),
            _loc("Osaka", "Osaka", "Japan", 34.6937, 135.5023, "Asia/Tokyo"),
            _loc("Sapporo", "Hokkaido", "Japan", 43.0618, 141.3545, "Asia/Tokyo"),
        ],
        "South Korea": [
            _loc("Seoul", "Seoul", "South Korea", 37.5665, 126.9780, "Asia/Seoul"),
            _loc("Busan", "Busan", "South Korea", 35.1796, 129.0756, "Asia/Seoul"),
        ],
        "Indonesia": [
            _loc("Jakarta", "Jakarta", "Indonesia", -6.2088, 106.8456, "Asia/Jakarta"),
            _loc("Denpasar", "Bali", "Indonesia", -8.6500, 115.2167, "Asia/Makassar"),
            _loc("Jayapura", "Papua", "Indonesia", -2.5916, 140.6690, "Asia/Jayapura"),
        ],
        "Saudi Arabia": [
            _loc("Riyadh", "Riyadh", "Saudi Arabia", 24.7136, 46.6753, "Asia/Riyadh"),
            _loc("Jeddah", "Makkah", "Saudi Arabia", 21.4858, 39.1925, "Asia/Riyadh"),
        ],
        "United Arab Emirates": [
            _loc("Dubai", "Dubai", "United Arab Emirates", 25.2048, 55.2708, "Asia/Dubai"),
            _loc("Abu Dhabi", "Abu Dhabi", "United Arab Emirates", 24.4539, 54.3773, "Asia/Dubai"),
        ],
        "Israel": [
            _loc("Jerusalem", "Jerusalem", "Israel", 31.7683, 35.2137, "Asia/Jerusalem"),
            _loc("Tel Aviv", "Tel Aviv", "Israel", 32.0853, 34.7818, "Asia/Jerusalem"),
        ],
    },
    "Africa": {
        "Egypt": [
            _loc("Cairo", "Cairo", "Egypt", 30.0444, 31.2357, "Africa/Cairo"),
            _loc("Alexandria", "Alexandria", "Egypt", 31.2001, 29.9187, "Africa/Cairo"),
        ],
        "South Africa": [
            _loc("Cape Town", "Western Cape", "South Africa", -33.9249, 18.4241, "Africa/Johannesburg"),
            _loc("Johannesburg", "Gauteng", "South Africa", -26.2041, 28.0473, "Africa/Johannesburg"),
            _loc("Durban", "KwaZulu-Natal", "South Africa", -29.8587, 31.0218, "Africa/Johannesburg"),
        ],
        "Nigeria": [
            _loc("Lagos", "Lagos", "Nigeria", 6.5244, 3.3792, "Africa/Lagos"),
            _loc("Abuja", "FCT", "Nigeria", 9.0765, 7.3986, "Africa/Lagos"),
        ],
        "Kenya": [
            _loc("Nairobi", "Nairobi", "Kenya", -1.2921, 36.8219, "Africa/Nairobi"),
            _loc("Mombasa", "Mombasa", "Kenya", -4.0435, 39.6682, "Africa/Nairobi"),
        ],
        "Morocco": [
            _loc("Casablanca", "Casablanca-Settat", "Morocco", 33.5731, -7.5898, "Africa/Casablanca"),
            _loc("Marrakesh", "Marrakesh-Safi", "Morocco", 31.6295, -7.9811, "Africa/Casablanca"),
        ],
        "Namibia": [
            _loc("Windhoek", "Khomas", "Namibia", -22.5609, 17.0658, "Africa/Windhoek"),
        ],
    },
    "Oceania": {
        "Australia": [
            _loc("Sydney", "New South Wales", "Australia", -33.8688, 151.2093, "Australia/Sydney"),
            _loc("Melbourne", "Victoria", "Australia", -37.8136, 144.9631, "Australia/Melbourne"),
            _loc("Perth", "Western Australia", "Australia", -31.9523, 115.8613, "Australia/Perth"),
            _loc("Darwin", "Northern Territory", "Australia", -12.4634, 130.8456, "Australia/Darwin"),
            _loc("Hobart", "Tasmania", "Australia", -42.8821, 147.3272, "Australia/Hobart"),
        ],
        "New Zealand": [
            _loc("Auckland", "Auckland", "New Zealand", -36.8485, 174.7633, "Pacific/Auckland"),
            _loc("Wellington", "Wellington", "New Zealand", -41.2866, 174.7756, "Pacific/Auckland"),
            _loc("Christchurch", "Canterbury", "New Zealand", -43.5321, 172.6362, "Pacific/Auckland"),
        ],
        "Fiji": [
            _loc("Suva", "Central", "Fiji", -18.1248, 178.4501, "Pacific/Fiji"),
        ],
        "Papua New Guinea": [
            _loc("Port Moresby", "National Capital District", "Papua New Guinea", -9.4438, 147.1803, "Pacific/Port_Moresby"),
        ],
    },
    "Arctic": {
        "Svalbard": [
            _loc("Longyearbyen", "Svalbard", "Svalbard", 78.2232, 15.6469, "Europe/Oslo"),
            _loc("Barentsburg", "Svalbard", "Svalbard", 74.5000, 19.0333, "Europe/Oslo"),
        ],
        "Russia": [
            _loc("Murmansk", "Murmansk Oblast", "Russia", 68.9585, 33.0827, "Europe/Moscow"),
            _loc("Norilsk", "Krasnoyarsk Krai", "Russia", 69.3535, 88.2028, "Asia/Krasnoyarsk"),
            _loc("Yakutsk", "Sakha Yakutia", "Russia", 62.0355, 129.7015, "Asia/Yakutsk"),
            _loc("Magadan", "Magadan Oblast", "Russia", 59.5653, 150.8023, "Asia/Magadan"),
            _loc("Petropavlovsk-Kamchatsky", "Kamchatka Krai", "Russia", 56.3153, 158.6498, "Asia/Kamchatka"),
            _loc("Tiksi", "Sakha Yakutia", "Russia", 71.6428, 128.8638, "Asia/Yakutsk"),
        ],
        "Alaska": [
            _loc("Barrow", "North Slope", "United States", 71.2906, -156.7886, "America/Anchorage"),
            _loc("Prudhoe Bay", "North Slope", "United States", 70.3531, -150.1874, "America/Anchorage"),
            _loc("Utqiagvik", "North Slope", "United States", 71.2906, -156.7886, "America/Anchorage"),
        ],
        "Canada Arctic": [
            _loc("Yellowknife", "Northwest Territories", "Canada", 62.4560, -114.3525, "America/Edmonton"),
            _loc("Inuvik", "Northwest Territories", "Canada", 68.3627, -133.7167, "America/Whitehorse"),
            _loc("Tuktoyaktuk", "Northwest Territories", "Canada", 69.4167, -133.0333, "America/Whitehorse"),
            _loc("Grise Fiord", "Nunavut", "Canada", 76.4333, -82.8833, "America/Toronto"),
            _loc("Arctic Bay", "Nunavut", "Canada", 73.0167, -85.4000, "America/Toronto"),
            _loc("Resolute", "Nunavut", "Canada", 74.7000, -94.8333, "America/Toronto"),
        ],
        "Greenland": [
            _loc("Tasiilaq", "Sermersooq", "Greenland", 65.6143, -37.6267, "America/Nuuk"),
            _loc("Kangerlussaq", "Qeqertarsuaq", "Greenland", 67.0133, -50.9533, "America/Nuuk"),
            _loc("Qaanaaq", "Avannaata", "Greenland", 77.4667, -69.3667, "America/Nuuk"),
            _loc("Grise Fiord", "Canada Arctic", "Greenland", 76.4333, -82.8833, "America/Nuuk"),
        ],
        "Iceland": [
            _loc("Westfjords", "West", "Iceland", 66.0000, -23.0000, "Atlantic/Reykjavik"),
        ],
        "North Pole": [
            _loc("North Pole", "Arctic Ocean", "Arctic", 90.0000, 0.0000, "UTC"),
        ],
    },
    "Antarctica": {
        "Antarctica": [
            _loc("McMurdo Station", "Ross Island", "Antarctica", -77.8419, 166.6863, "Antarctica/McMurdo"),
            _loc("Amundsen-Scott", "South Pole", "Antarctica", -90.0000, 0.0000, "Antarctica/South_Pole"),
            _loc("Rothera", "Adelaide Island", "Antarctica", -67.5670, -68.1230, "Antarctica/Rothera"),
            _loc("Casey", "Wilkes Land", "Antarctica", -66.2818, 110.5276, "Antarctica/Casey"),
            _loc("Vostok", "Polar Plateau", "Antarctica", -78.4642, 106.8360, "UTC"),
            _loc("Concordia", "Polar Plateau", "Antarctica", -75.1000, 123.3500, "UTC"),
            _loc("Mirny", "Wilkes Land", "Antarctica", -66.5301, 93.0097, "Antarctica/Casey"),
            _loc("Neumayer", "Queen Maud Land", "Antarctica", -70.6496, -8.2686, "UTC"),
            _loc("South Pole", "Plateau", "Antarctica", -90.0000, 0.0000, "Antarctica/South_Pole"),
            _loc("Palmer Station", "Antarctic Peninsula", "Antarctica", -64.7743, -64.0592, "America/Anchorage"),
        ],
    },
    "Equatorial": {
        "Ecuador": [
            _loc("Quito", "Pichincha", "Ecuador", -0.2166, -78.5123, "America/Guayaquil"),
            _loc("Mitad del Mundo", "Pichincha", "Ecuador", 0.0000, -78.4562, "America/Guayaquil"),
            _loc("Baños", "Tungurahua", "Ecuador", -1.3975, -78.4258, "America/Guayaquil"),
        ],
        "Kenya": [
            _loc("Nanyuki", "Laikipia", "Kenya", 0.0032, 37.0686, "Africa/Nairobi"),
            _loc("Maralal", "Samburu", "Kenya", 1.0000, 36.7000, "Africa/Nairobi"),
            _loc("Kericho", "Kisii", "Kenya", -0.3667, 35.2833, "Africa/Nairobi"),
        ],
        "Gabon": [
            _loc("Libreville", "Estuaire", "Gabon", 0.4162, 9.4673, "Africa/Libreville"),
            _loc("Lambaréné", "Moyen-Ogooué", "Gabon", -0.6876, 10.2307, "Africa/Libreville"),
        ],
        "Cameroon": [
            _loc("Yaoundé", "Centre", "Cameroon", 3.8667, 11.5167, "Africa/Douala"),
            _loc("Douala", "Littoral", "Cameroon", 4.0511, 9.7679, "Africa/Douala"),
        ],
        "Democratic Republic of Congo": [
            _loc("Kinshasa", "Kinshasa", "Democratic Republic of Congo", -4.3276, 15.3136, "Africa/Kinshasa"),
            _loc("Kisangani", "Oriental", "Democratic Republic of Congo", 0.5000, 25.1833, "Africa/Kinshasa"),
        ],
        "Republic of Congo": [
            _loc("Brazzaville", "Pool", "Republic of Congo", -4.2634, 15.2429, "Africa/Brazzaville"),
        ],
        "Indonesia": [
            _loc("Pontianak", "West Kalimantan", "Indonesia", -0.0276, 109.3252, "Asia/Pontianak"),
            _loc("Tarakan", "North Kalimantan", "Indonesia", 3.3000, 117.6333, "Asia/Tarakan"),
            _loc("Manado", "North Sulawesi", "Indonesia", 1.4748, 124.7625, "Asia/Makassar"),
        ],
        "Singapore": [
            _loc("Singapore", "Singapore", "Singapore", 1.3521, 103.8198, "Asia/Singapore"),
        ],
        "Malaysia": [
            _loc("Kuala Lumpur", "Federal Territory", "Malaysia", 3.1390, 101.6869, "Asia/Kuala_Lumpur"),
            _loc("Kuching", "Sarawak", "Malaysia", 1.5533, 110.3592, "Asia/Kuala_Lumpur"),
        ],
        "Brazil": [
            _loc("Macapá", "Amapá", "Brazil", 0.0352, -51.0697, "America/Manaus"),
            _loc("Santarém", "Pará", "Brazil", -2.4361, -54.7144, "America/Manaus"),
        ],
        "Peru": [
            _loc("Iquitos", "Loreto", "Peru", -3.7492, -73.2844, "America/Lima"),
            _loc("Cruzeiro do Sul", "Acre", "Peru", -7.6290, -72.6692, "America/Lima"),
        ],
        "Colombia": [
            _loc("Leticia", "Amazonas", "Colombia", -4.2156, -69.9412, "America/Bogota"),
            _loc("Puerto Asís", "Putumayo", "Colombia", 0.5067, -76.4789, "America/Bogota"),
        ],
    },
}


class WorldLocationCatalog:
    """Read-only helpers for continent/country/locality navigation."""

    @staticmethod
    def continents() -> list[str]:
        return sorted(WORLD_LOCATIONS.keys())

    @staticmethod
    def countries(continent: str) -> list[str]:
        return sorted(WORLD_LOCATIONS.get(continent, {}).keys())

    @staticmethod
    def localities(continent: str, country: str) -> list[GeoLocation]:
        return list(WORLD_LOCATIONS.get(continent, {}).get(country, []))

    @staticmethod
    def find_location(continent: str, country: str, locality_name: str) -> GeoLocation | None:
        for location in WorldLocationCatalog.localities(continent, country):
            if location.name == locality_name:
                return location
        return None
