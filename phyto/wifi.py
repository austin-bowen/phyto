import os
import wifi

WIFI_SSID = os.getenv('WIFI_SSID', None)
WIFI_PASSWORD = os.getenv('WIFI_PASSWORD', None)
WIFI_HOSTNAME = os.getenv('WIFI_HOSTNAME', None)


def setup_wifi(
        ssid: str = WIFI_SSID,
        password: str = WIFI_PASSWORD,
        hostname: str = WIFI_HOSTNAME,
) -> None:
    """Connects to WiFi. Raises ``ConnectionError`` if something goes wrong."""

    print(f'Connecting to WiFi (ssid={ssid}; hostname={hostname})...')

    wifi.radio.hostname = hostname
    try:
        wifi.radio.connect(ssid, password)
    except ConnectionError:
        print('Failed to connect to WiFi')
        raise

    print(f'Connected to WiFi! ip={wifi.radio.ipv4_address}')
