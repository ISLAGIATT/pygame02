class GameStateManager:
    def __init__(self):
        self.current_room_id = None
        self.current_open_dropdown = None
        self.target_alpha_reached = False
        self.navpoint_001_active = False
        self.in_gameplay = True
        self.in_landing_scene = False
        self.rooms = {
            'room1': {  # test room 1
                'exits': ['east door'],
                'door_open': False,
            },
            'room2': {  # test room 2
                'exits': ['west door', 'north door'],
            }
        }

    def switch_to_gameplay(self):
        self.in_gameplay = True
        self.in_landing_scene = False

    def switch_to_landing_scene(self):
        self.in_gameplay = False
        self.in_landing_scene = True

    def set_target_alpha_reached(self, value: bool):
        self.target_alpha_reached = value

    # Exits window stuff below
    def change_room(self, new_room_id):
        # Additional logic to handle room transition could be placed here...
        self.current_room_id = new_room_id

    def get_exits_for_current_room(self):
        # This method retrieves the exits for the current room
        room_info = self.rooms.get(self.current_room_id)
        if room_info:
            return room_info['exits']
        else:
            return []  # Return an empty list if the room ID is not found

    def get_current_room_id(self):
        return self.current_room_id

    def get_clickable_box_data_for_room(self, room_id):
        # Retrieve clickable box data for the current room
        room_data = self.rooms.get(room_id, {})
        return room_data.get('clickable_box', {
            'rect': (0, 0, 0, 0),  # Default to an invisible box
            'color': (255, 255, 255),
            'callback': None,
            'visible': False
        })

    #  Right click menu stuff below
    def open_dropdown(self, dropdown):
        if self.current_open_dropdown and self.current_open_dropdown != dropdown:
            self.current_open_dropdown.close()
        self.current_open_dropdown = dropdown
        dropdown.is_visible = True  # Make the dropdown visible

    def close_dropdown(self, dropdown):
        if self.current_open_dropdown:
            self.current_open_dropdown.close()
            self.current_open_dropdown = None
