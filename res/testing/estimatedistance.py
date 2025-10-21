def estimate_distance(tx_power, rssi, n=2):
    """
    Estimate distance based on TX power and RSSI.

    Parameters:
    tx_power (float): Transmission power in dBm.
    rssi (float): Received signal strength indicator in dBm.
    n (float): Path-loss exponent (default is 2 for free space).

    Returns:
    float: Estimated distance in meters.
    """
    if rssi >= tx_power:
        return 0  # Signal too strong, too close to estimate distance

    # Applying the formula
    distance = 10 ** ((tx_power - rssi) / (10 * n))
    return distance


# Example Usage
tx_power = 12  # dBm
rssi = -92  # dBm

distance_estimate = estimate_distance(tx_power, rssi)
print(f"Estimated Distance: {distance_estimate:.2f} meters")


"""


None, E2:73:E7:E9:BA:CE, rssi -92dBm, tx_power: None, distance: None
None, 7B:15:66:B1:57:8E, rssi -86dBm, tx_power: 12, distance: 8317.64
None, 42:84:8C:F8:DA:77, rssi -76dBm, tx_power: 12, distance: 3311.31
None, 23:94:67:EB:E4:C3, rssi -84dBm, tx_power: None, distance: None
None, 5E:23:BF:FB:C3:E2, rssi -74dBm, tx_power: 12, distance: 2754.23
None, 42:84:8C:F8:DA:77, rssi -74dBm, tx_power: 12, distance: 2754.23
None, 6F:E4:11:CA:D8:1E, rssi -90dBm, tx_power: 12, distance: 12022.64
None, 5E:B1:71:DA:F0:1C, rssi -76dBm, tx_power: None, distance: None
None, 48:E1:5C:92:5F:94, rssi -92dBm, tx_power: 12, distance: 14454.4
None, 5E:B1:71:DA:F0:1C, rssi -88dBm, tx_power: None, distance: None
None, 49:F3:CB:46:FD:80, rssi -96dBm, tx_power: None, distance: None
None, 5E:B1:71:DA:F0:1C, rssi -76dBm, tx_power: None, distance: None
None, 24:E8:53:1A:5A:B0, rssi -94dBm, tx_power: None, distance: None
None, 78:9B:3F:C8:3B:79, rssi -52dBm, tx_power: 12, distance: 363.08
None, 5E:B1:71:DA:F0:1C, rssi -86dBm, tx_power: None, distance: None
None, 7C:D1:C3:30:5A:08, rssi -100dBm, tx_power: None, distance: None
None, 5E:B1:71:DA:F0:1C, rssi -76dBm, tx_power: None, distance: None
None, 5D:61:0A:D4:C2:78, rssi -100dBm, tx_power: 12, distance: 30199.52
None, DA:C7:6C:E1:C9:4B, rssi -52dBm, tx_power: None, distance: None
None, 5E:B1:71:DA:F0:1C, rssi -74dBm, tx_power: None, distance: None
None, 78:9B:3F:C8:3B:79, rssi -106dBm, tx_power: 12, distance: 52480.75
None, E5:A2:50:56:84:8F, rssi -90dBm, tx_power: None, distance: None
None, 56:61:17:75:76:15, rssi -94dBm, tx_power: None, distance: None
None, 5E:B1:71:DA:F0:1C, rssi -86dBm, tx_power: None, distance: None
None, 5D:61:0A:D4:C2:78, rssi -98dBm, tx_power: 12, distance: 25118.86
None, 5E:B1:71:DA:F0:1C, rssi -76dBm, tx_power: None, distance: None
E2 Pro 2912, C7:27:12:39:5F:F6, rssi -98dBm, tx_power: None, distance: None
None, 4A:BE:29:FC:A1:52, rssi -96dBm, tx_power: None, distance: None
None, E2:73:E7:E9:BA:CE, rssi -94dBm, tx_power: None, distance: None
E2 Pro 2912, C7:27:12:39:5F:F6, rssi -96dBm, tx_power: None, distance: None
None, E2:73:E7:E9:BA:CE, rssi -96dBm, tx_power: None, distance: None
None, 49:F3:CB:46:FD:80, rssi -100dBm, tx_power: None, distance: None
None, 5E:B1:71:DA:F0:1C, rssi -86dBm, tx_power: None, distance: None
None, E2:73:E7:E9:BA:CE, rssi -86dBm, tx_power: None, distance: None
None, 5E:B1:71:DA:F0:1C, rssi -76dBm, tx_power: None, distance: None

"""
