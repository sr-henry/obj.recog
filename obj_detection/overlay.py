from win32gui import SetPixel

class Overlay:
    def __init__(self, device_context):
        self.dc = device_context

    def create_pixelmap(self, pixel_cords, color):
        for cord in pixel_cords:
            SetPixel(self.dc, cord[0], cord[1], color)

    def create_box(self, cords, color):
        for t in range(cords[0], cords[2]):
            SetPixel(self.dc, t, cords[1], color)
            SetPixel(self.dc, t, cords[3], color)
        for l in range(cords[1], cords[3]):
            SetPixel(self.dc, cords[0], l, color)
            SetPixel(self.dc, cords[2], l, color)