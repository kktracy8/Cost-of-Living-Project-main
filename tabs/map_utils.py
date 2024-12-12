from typing import Dict


def get_mapbox_center(location: str) -> Dict[str, float]:
    match location:
        case 'Los Angeles, CA':
            mapbox_center = {"lat": 34.0549, "lon": -118.2426}
        case 'Las Vegas, NV':
            mapbox_center = {"lat": 36.1716, "lon": -115.1391}
        case 'Chicago, IL':
            mapbox_center = {"lat": 41.8781, "lon": -87.6298}
        case 'Dallas, TX':
            mapbox_center = {"lat": 32.7767, "lon": -96.7970}
        case 'Boston, MA':
            mapbox_center = {"lat": 42.3601, "lon": -71.0589}
        case 'New York City, NY':
            mapbox_center = {"lat": 40.7128, "lon": -74.0060}
        case 'Denver, CO':
            mapbox_center = {"lat": 39.7392, "lon": -104.9903}
        case _:
            mapbox_center = {"lat": 34.0549, "lon": -118.2426}
    return mapbox_center
