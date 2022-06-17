# Mods

## Limitations
The purpose and abilities of Mods are restricted to modifying the `pokete_data` module.
But this can be very powerfull, because this enables adding and modifying Poketes, Maps, NPCs, trainers, types, achievemnts and much more.

## Structure
The basic structure of a mod is:

```python
version = "0.1.0"  # The mods version as a string
name = "Example"  # The mods name as a string

def mod_p_data(p_data):  # The functions modifying function
    # p_data is the pokete_data module
    p_data.pokes["steini"]["name"] = "Steino"  # Example modifications happen here
```
