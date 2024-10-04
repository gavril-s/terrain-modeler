import geopy.distance
import requests

BATCH_SIZE = 100


def distance(lat1, lon1, lat2, lon2):
    coords1 = (lat1, lon1)
    coords2 = (lat2, lon2)
    return geopy.distance.geodesic(coords1, coords2).m


def get_elevations_from_open_meteo(coords):
    lats_str = ",".join(str(lat) for lat, _ in coords)
    lons_str = ",".join(str(lon) for _, lon in coords)
    url = f"https://api.open-meteo.com/v1/elevation?latitude={lats_str}&longitude={lons_str}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return data["elevation"]
    else:
        raise(f"Error fetching elevation data: {resp.status_code}")

def get_elevations_from_open_elevation(coords):
    url = "https://api.open-elevation.com/api/v1/lookup"
    data = {"locations": [{"latitude": lat, "longitude": lon} for lat, lon in coords]}
    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        data = resp.json()
        return [item["elevation"] for item in data["results"]]
    else:
        raise(f"Error fetching elesvation data: {resp.status_code}")


apis = {
    'https://api.open-meteo.com': get_elevations_from_open_meteo,
    'https://api.open-elevation.com': get_elevations_from_open_elevation
}


def get_elevations(coords, api):
    handler = apis[api]
    if handler is None:
        raise("Invalid API choice:", api)
    return handler(coords)


def generate_coordinates(
    top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon,
    lat_points, lon_points
):
    lat_step = (top_left_lat - bottom_right_lat) / (lat_points - 1)
    lon_step = (bottom_right_lon - top_left_lon) / (lon_points - 1)

    coordinates = []
    for i in range(lat_points):
        for j in range(lon_points):
            lat = top_left_lat - i * lat_step
            lon = top_left_lon + j * lon_step
            coordinates.append((lat, lon))
    return coordinates


def fetch_elevations(coords, api):
    elevations = []
    for i in range(0, len(coords), BATCH_SIZE):
        batch = coords[i : i + BATCH_SIZE]
        resp = get_elevations(batch, api)
        for j in range(len(batch)):
            if len(elevations) == 0:
                elevations = [[0, 0, resp[j]]]
            else:
                latd = distance(
                    batch[j][0], batch[j][1], coords[0][0], batch[j][1]
                )
                lond = distance(
                    batch[j][0], batch[j][1], batch[j][0], coords[0][1]
                )
                elevations.append([latd, lond, resp[j]])
    return elevations


def fetch_rectangle(top_left, bottom_right, lat_points, lon_points, api):
    coords = generate_coordinates(
        top_left[0], top_left[1], bottom_right[0], bottom_right[1], lat_points, lon_points
    )
    elevations = fetch_elevations(coords, api)
    return elevations
