def get_icons(temp, brightness, volume, battery):
    temp = int(temp.split(".")[0])
    if temp <= 40:
        temp_icon = ""
    elif temp <=50:
        temp_icon = ""
    elif temp <= 70:
        temp_icon = ""
    elif temp <= 80:
        temp_icon = ""
    elif temp <= 90:
        temp_icon = ""
    else:
        temp_icon = ""

    brightness = int(brightness.split("%")[0])
    if brightness <= 40:
        bright_icon = "󰃞"
    elif brightness <= 70:
        bright_icon = "󰃝"
    else:
        bright_icon = "󰃠"

    volume = int(volume.split("%")[0])
    if volume <= 0:
        volume_icon = ""
    elif volume <= 69:
        volume_icon = ""
    else:
        volume_icon = ""
    
    battery = int(battery.split("%")[0])
    if battery <= 15:
        battery_icon = ""
    elif battery <= 30:
        battery_icon = ""
    elif battery <= 60:
        battery_icon = ""
    elif battery <= 70:
        battery_icon = ""
    else:
        battery_icon = ""

    return (temp_icon, bright_icon, volume_icon, battery_icon)
