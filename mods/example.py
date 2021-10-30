## This is an example mod that renames steini to steino

version = "0.1.0"
name = "Example"

def mod_p_data(p_data):
    p_data.pokes["steini"]["name"] = "Steino"
