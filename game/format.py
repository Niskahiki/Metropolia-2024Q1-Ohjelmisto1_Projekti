# Player dictionary structure
def player_structure(player_name):
    return { "name": player_name, "score": False, "co2": 0, "location": [60.3172, 24.963301], "parcels_picked": [], "parcels_delivered": [], "gameover": False }


# Parcel dictionary structure (not defined, decreed by the database itself!)
#parcel_structure = 


# Item heft classes
heft_classes = {1:(0.1,1), 2:(1,3), 3:(3,10)}


# Transport method speeds (1: km/h, ... rest are multiples of 1)
transport_speed1 = 800
transport_speed2 = 0.50
transport_speed3 = 2.0

transport1_co2 = 0.75
transport2_co2 = 1
transport3_co2 = 2.0

parcel_selection_time_limit = 150
actual_parcel_delivery_time_limit = 80


parcel_delivery_time_limit = 90

