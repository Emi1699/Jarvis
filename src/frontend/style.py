class Style:

    def __init__(self):

        self.WINDOW_WIDTH = int(1000 * 0.68)
        self.WINDOW_HEIGHT = int(1000 * 0.7)
        self.BOX_RELATIVE_WIDTH = 0.063 * self.WINDOW_WIDTH
        self.INPUT_BOX_RELATIVE_HEIGHT = 0.01 * self.WINDOW_HEIGHT
        self.OUTPUT_BOX_RELATIVE_HEIGHT = 0.02 * self.WINDOW_HEIGHT

        # constants used throughout the program
        self.PADDING = 17
        self.BOX_COLOUR = 'black'
        self.TEXT_COLOUR = 'white'
        self.INPUT_TEXT_COLOUR = '#FF8C00'
        self.OUTPUT_TEXT_COLOUR = '#00CED1'
        self.UNSELECTED_BOX_OUTLINE_COLOUR = '#9417cf'
        self.SELECTED_BOX_OUTLINE_COLOUR = '#9417cf'
