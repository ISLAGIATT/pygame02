class MouseEventHandler:
    def __init__(self, interactive_objects, clickable_objects, dropdown_menus):
        # Objects that respond directly to clicks (e.g., buttons)
        self.clickable_objects = clickable_objects
        # Interactive Objects
        self.interactive_objects = interactive_objects
        # Dropdown menus which have specific visibility toggling and option selection
        self.dropdown_menus = dropdown_menus if dropdown_menus is not None else []
        self.last_click_time = 0

    def handle_click(self, mouse_pos, button):
        # Right-click: Toggle dropdown visibility
        if button == 3:
            self.handle_right_click(mouse_pos)
        # Left-click: General click handling (objects and dropdown options)
        elif button == 1:
            if not self.handle_interactive_objects(mouse_pos):
                self.handle_left_click(mouse_pos)

    def handle_interactive_objects(self, mouse_pos):
        for obj in self.interactive_objects:
            if hasattr(obj,
                       'is_visible') and obj.is_visible and obj.current_dialogue_rect and obj.current_dialogue_rect.collidepoint(
                    mouse_pos):
            # if obj.is_visible and obj.current_dialogue_rect and obj.current_dialogue_rect.collidepoint(mouse_pos): code from import
                # Assuming all dialogues are lists, we check the length directly
                if len(obj.dialogue) > 1:
                    print(f'object: {obj}, length of dialogue list: {len(obj.dialogue)}, index: {obj.dialogue_index}')
                    # Advance the dialogue index or reset and hide after the last entry
                    if obj.dialogue_index < len(obj.dialogue) - 1:
                        obj.advance_dialogue()
                        obj.is_visible = False
                    else:
                        obj.dialogue_index = 0  # Reset index for future interactions
                        obj.is_visible = False
                else:
                    # Single entry dialogues are hidden after being clicked
                    obj.is_visible = False


                # Ensure to update the dialogue display to reflect the new index or hide it
                # This might involve redrawing the dialogue text or calling a method to update the game screen

                return True  # Interaction handled
        return False  # No dialogue interaction detected

    def handle_right_click(self, mouse_pos):
        for dropdown in self.dropdown_menus:
            if dropdown.button.is_over(mouse_pos):  # Assuming each dropdown is associated with a button
                dropdown.toggle_visibility()
                return  # Assuming only one dropdown can be toggled at a time

    def handle_left_click(self, mouse_pos):
        # Check for clicks on dropdown options first
        for dropdown in self.dropdown_menus:
            if dropdown.is_visible:
                hovered_option_index = dropdown.is_over_option(mouse_pos)
                if hovered_option_index is not None:
                    # Execute the associated action for the clicked dropdown option
                    selected_option = dropdown.option_list[hovered_option_index]
                    dropdown.execute_action(selected_option)
                    dropdown.is_visible = False  # Hide after selection
                    return  # Exit to avoid further action if dropdown was interacted with

                # If clicked outside any visible dropdown, hide them
                dropdown.is_visible = False
        for obj in self.clickable_objects:
            if obj.is_over(mouse_pos):
                obj.handle_click(mouse_pos)
                break  # Assuming only one object can be clicked at a time