import requests
import json


def get_ip_info():
    """Gets IP-based location and related info."""
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}


def get_public_ip():
    """Gets the public IP address."""
    try:
        response = requests.get("https://api.ipify.org?format=json")
        data = response.json()
        return data["ip"]
    except Exception as e:
        return {"error": str(e)}


def get_headers_info():
    """Gets basic information from HTTP headers."""
    try:
        response = requests.get("https://httpbin.org/headers")
        data = response.json()
        return data["headers"]
    except Exception as e:
        return {"error": str(e)}


def get_online_info():
    """Gathers various online information."""
    info = {}

    # Get public IP address
    ip_address = get_public_ip()
    info["Public IP"] = ip_address

    # Get location information based on IP address
    ip_info = get_ip_info()
    info["IP Info"] = ip_info

    # Get HTTP headers information
    headers_info = get_headers_info()
    info["Headers"] = headers_info

    return info


if __name__ == "__main__":
    online_info = get_online_info()

    # Print the information gathered
    print(json.dumps(online_info, indent=4))
