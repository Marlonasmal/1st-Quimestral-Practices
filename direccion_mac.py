import network
red = network.WLAN(network.STA_IF)
red.active(True)
Mac = red.config('mac')
print("Direccion MAC del ESP32:", ':'.join(['{:02x}'.format(b) for b in Mac]))