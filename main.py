from create_ship_layout import init, create_ship_layout, open_dead_end, create_bot_fire_button

#project 1 - bot turns off fire
# init the 2D map of ship
d, ship_map = init()
create_ship_layout(ship_map)
print("ship layout:")
print(ship_map)
open_dead_end(ship_map)
print("ship layout after opening dead ends:")
print(ship_map)
create_bot_fire_button(ship_map)
