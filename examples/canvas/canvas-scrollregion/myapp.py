# file: myapp.py
import pathlib
import random
import math

import pygubu


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "myapp.ui"
DEG2RAD = 4 * math.atan(1) * 2 / 360


class MyApplication:

    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow')

        self.canvas = builder.get_object('main_canvas')
        # Connect to Delete event
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.quit)

        builder.connect_callbacks(self)

    def btn_draw_clicked(self):
        figures = ['square', 'cross', 'circle', 'triangle']
        figure = random.choice(figures)
        self._draw_figure(figure)

        # Update Canvas scroll region
        bbox = self.canvas.bbox('all')
        self.canvas.configure(scrollregion=bbox)

    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()

    def _draw_figure(self, figure):
        canvas = self.canvas
        max_iterations = random.randint(3, 10)

        for i in range(0, max_iterations):
            canvasw = canvas.winfo_width()
            canvash = canvas.winfo_height()
            borderw = random.randint(1, 5)
            max_width = int(canvas.winfo_width() * 0.25)
            w = random.randint(20, max_width)
            x = random.randint(0, canvasw) - int(max_width * 0.5)
            y = random.randint(0, canvash) - int(max_width * 0.5)
            start = random.randint(0, 180)

            if figure == 'circle':
                canvas.create_oval(x, y, x + w, y + w,
                                   outline='#FF6666', width=borderw)
            if figure == 'square':
                self.create_regpoly(x, y, x + w, y + w,
                                    sides=4, start=start,
                                    outline='#ED9DE9', width=borderw, fill='')
            if figure == 'triangle':
                self.create_regpoly(x, y, x + w, y + w,
                                    sides=3, start=start,
                                    outline='#40E2A0', width=borderw, fill='')
            if figure == 'cross':
                self.create_regpoly(x, y, x + w, y + w,
                                    sides=2, start=start,
                                    outline='#80B3E7', width=borderw, fill='')
                self.create_regpoly(x, y, x + w, y + w,
                                    sides=2, start=start + 90,
                                    outline='#80B3E7', width=borderw, fill='')

    def create_regpoly(self, x0, y0, x1, y1, sides=0, start=90, extent=360, **kw):
        """Create a regular polygon"""
        coords = self.__regpoly_coords(x0, y0, x1, y1, sides, start, extent)
        return self.canvas.create_polygon(*coords, **kw)

    def __regpoly_coords(self, x0, y0, x1, y1, sides, start, extent):
        """Create the coordinates of the regular polygon specified"""

        coords = []
        if extent == 0:
            return coords

        xm = (x0 + x1) / 2.
        ym = (y0 + y1) / 2.
        rx = xm - x0
        ry = ym - y0

        n = sides
        if n == 0:  # 0 sides => circle
            n = round((rx + ry) * .5)
            if n < 2:
                n = 4

        # Extent can be negative
        dirv = 1 if extent > 0 else -1
        if abs(extent) > 360:
            extent = dirv * abs(extent) % 360

        step = dirv * 360 / n
        numsteps = 1 + extent / float(step)
        numsteps_int = int(numsteps)

        i = 0
        x = y = 0
        while i < numsteps_int:
            rad = (start - i * step) * DEG2RAD
            x = rx * math.cos(rad)
            y = ry * math.sin(rad)
            coords.append((xm + x, ym - y))
            i += 1

        # Figure out where last segment should end
        if numsteps != numsteps_int:
            # Vecter V1 is last drawn vertext (x,y) from above
            # Vector V2 is the edge of the polygon
            rad2 = (start - numsteps_int * step) * DEG2RAD
            x2 = rx * math.cos(rad2) - x
            y2 = ry * math.sin(rad2) - y

            # Vector V3 is unit vector in direction we end at
            rad3 = (start - extent) * DEG2RAD
            x3 = math.cos(rad3)
            y3 = math.sin(rad3)

            # Find where V3 crosses V1+V2 => find j s.t.  V1 + kV2 = jV3
            j = (x * y2 - x2 * y) / (x3 * y2 - x2 * y3)

            coords.append((xm + j * x3, ym - j * y3))

        return coords


if __name__ == '__main__':
    app = MyApplication()
    app.run()
