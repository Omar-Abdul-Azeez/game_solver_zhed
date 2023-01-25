import tkinter as tk

from enum import Enum
from tkinter.messagebox import showerror


# TODO IMPLEMENTATION
class Zhed:
    class Grid:

        class Constants(Enum):
            GOAL = -1
            EMPTY = 0

        GOAL = Constants.GOAL
        EMPTY = Constants.EMPTY

        def __init__(self, cells):
            self.w = len(cells)
            self.h = len(cells[0])
            self.cells = []
            self.goals = []
            for iw in range(self.w):
                cells_w = []
                self.cells.append(cells_w)
                for ih in range(self.h):
                    cell = cells[iw][ih]
                    if cell == Zhed.Grid.GOAL:
                        self.goals.append([iw, ih])
                    cells_w.append(cell)

    def __init__(self, cells):
        self.grid = Zhed.Grid(cells)
        self.sol = ''

    def solve(self):
        pass

    def __str__(self):
        pass


class Grid(tk.Frame):
    # TODO create a grid of frames then pack each widget inside with expand=true
    def __init__(self, w, h, widget_init, master=None, *args, **kwargs):
        super().__init__(master)
        self.widget_init = widget_init
        self.args = args
        self.kwargs = kwargs.copy()
        self.dummy = tk.Frame(self)
        self.dummy.grid()
        self.widgets = []
        self._mkgrid(0, 0, w, h)

    def _mkgrid(self, oldw, oldh, neww, newh):
        # TODO current implementation creates only the bottom right section of the new, bigger, grid.
        # It should also create the top right and bottom left sections.
        # Also doesn't make the grid smaller.
        self.w = neww
        self.h = newh
        for iw in range(oldw, neww):
            widgets_w = []
            self.widgets.append(widgets_w)
            for ih in range(oldh, newh):
                widget = self.widget_init(*self.args, **dict(self.kwargs, master=self.dummy))
                widgets_w.append(widget)
                widget.grid(column=iw, row=ih)

    @staticmethod
    def reset(widget, w, h):
        raise NotImplementedError

    def change_dim(self, w, h, identical, reset=None, *args, **kwargs):
        if self.w == w and self.h == h:
            for iw in range(w):
                for ih in range(h):
                    if reset is None:
                        reset = self.reset
                    reset(self.widgets[iw][ih], iw, ih)
        else:
            if identical:
                self._mkgrid(self.w, self.h, w, h)
            else:
                self.dummy.destroy()
                self.dummy = tk.Frame(self)
                self.dummy.grid()
                self.widgets.clear()
                self.args = args
                self.kwargs = kwargs.copy()
                self._mkgrid(0, 0, w, h)

    def apply(self, func):
        for iw in range(self.w):
            for ih in range(self.h):
                func(self.widgets[iw][ih], iw, ih)


class EntryGrid(Grid):
    def __init__(self, w, h, master=None, *args, **kwargs):
        super().__init__(w, h, tk.Entry, master=master, *args, **kwargs)

    @staticmethod
    def reset(entry, w, h):
        entry.delete(0, tk.END)

    def clear(self):
        self.apply(EntryGrid.reset)

    # TODO REWRITE
    def get(self):
        cells = []
        for iw in range(self.w):
            cells_w = []
            cells.append(cells_w)
            for ih in range(self.h):
                value = self.widgets[iw][ih].get().strip().lower()
                if 'goal' == value:
                    cells_w.append(Zhed.Grid.GOAL)
                elif value == '':
                    cells_w.append(Zhed.Grid.EMPTY)
                else:
                    try:
                        value = int(value)
                        if value == -1:
                            cells_w.append(Zhed.Grid.GOAL)
                        elif value == 0:
                            cells_w.append(Zhed.Grid.EMPTY)
                        else:
                            cells_w.append(value)
                    except ValueError:
                        showerror(title='', message='')
                        return None
        return cells


class LabelGrid(Grid):
    def __init__(self, w, h, master=None, *args, **kwargs):
        super().__init__(w, h, tk.Label, master=master, *args, **kwargs)

    @staticmethod
    def reset(label, w, h):
        pass


class App(tk.Frame):
    # TODO figure out how to lay this thing correctly...
    def __init__(self, title, master=None):
        super().__init__(master)
        self.master.title(title)
        self.master.minsize(width=200, height=80)
        self.grid(sticky='news')
        self.grid_columnconfigure(0, weight=1)

        self.upper = tk.Frame(self)
        self.upper.grid(column=0, row=0, sticky='new')

        self.label_dims = tk.Label(self.upper, text='Grid dimensions')
        self.entry_dimw = tk.Entry(self.upper, width=5)
        self.label_dimxdim = tk.Label(self.upper, text=' X')
        self.entry_dimh = tk.Entry(self.upper, width=5)
        self.label_dims.grid(column=0, columnspan=3, row=0)
        self.entry_dimw.grid(column=0, row=1, sticky='ew')
        self.label_dimxdim.grid(column=1, row=1, sticky='ew')
        self.entry_dimh.grid(column=2, row=1, sticky='ew')

        def command_clear():
            self.gridgame.clear()

        def command_solve():
            res = self.gridgame.get()
            # TODO CHECK RESULT
            zhed = Zhed(res)
            zhed.solve()
            print(zhed)
            self.gridsol.grid()

        def command_reset():
            try:
                w = int(self.entry_dimw.get())
                h = int(self.entry_dimh.get())
                if w < 1 or h < 1:
                    raise ValueError
            except ValueError:
                showerror('Dimension Error', 'Please enter positive integer dimensions!')
                return
            self.gridgame.change_dim(w, h, True)
            self.gridsol.change_dim(w, h, True)

        def command_start():
            try:
                w = int(self.entry_dimw.get())
                h = int(self.entry_dimh.get())
                if w < 1 or h < 1:
                    raise ValueError
            except ValueError:
                showerror('Dimension Error', 'Please enter positive integer dimensions!')
                return

            self.lower = tk.Frame(self)
            self.lower.grid(column=0, row=1, sticky='ews')

            self.gridgame = EntryGrid(w, h, self.lower, width=5)
            self.gridsol = LabelGrid(w, h, master=self.lower, text='cell')
            self.button_clear = tk.Button(self.lower, text='Clear', command=command_clear)
            self.button_solve = tk.Button(self.lower, text='Solve', command=command_solve)

            self.gridgame.grid(column=1, columnspan=1, row=0, sticky='nws')
            self.gridsol.grid(column=4, columnspan=1, row=0, sticky='nes')
            # self.gridsol.grid_remove()
            self.button_clear.grid(column=0, columnspan=3, row=1, sticky='new')
            self.button_solve.grid(column=3, columnspan=3, row=1, sticky='new')
            self.button_startreset.configure(text='Reset', command=command_reset)

        self.button_startreset = tk.Button(self.upper, text='Start', command=command_start)
        self.button_startreset.grid(column=0, columnspan=3, row=2, sticky='new')


if __name__ == '__main__':
    app = App('Zhed')
    app.mainloop()
