import tkinter as tk

from enum import Enum
from tkinter.messagebox import showerror
from tkinter import font


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
    class Constants(Enum):
        CELL = 'cell'
        GRID = 'grid'
    CELL = Constants.CELL
    GRID = Constants.GRID

    def __init__(self, dim, widget_init, size=None, size_type=None, master=None, *args, **kwargs):
        super().__init__(master)
        self.widget_init = widget_init
        self.args = args
        self.kwargs = kwargs.copy()
        self.dummy = tk.Frame(self)
        self.dummy.grid()
        if size is None or size_type is None:
            size = None
            size_type = None
        self._mkgrid((0, 0), dim, size=size, size_type=size_type)

    def _mkwidget(self, iw, ih, size_cell=None):
        if size_cell is not None:
            frame = tk.Frame(master=self.dummy, width=size_cell[0], height=size_cell[1])
            frame.grid_propagate(False)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)
        else:
            frame = tk.Frame(master=self)
        widget = self.widget_init(master=frame, *self.args, **self.kwargs)
        frame.grid(column=iw, row=ih)
        widget.grid(sticky='news')
        return widget

    def _mkgrid(self, dim_old, dim_new, size=None, size_type=None):
        self.dim = tuple(dim_new)
        if size is not None:
            self.size = tuple(size)
            self.size_type = size_type
            if size_type == Grid.GRID:
                size_cell = (size[0] // dim_new[0], size[1] // dim_new[1])
            elif size_type == Grid.CELL:
                size_cell = size
        if dim_new[0] > dim_old[0]:
            for iw in range(dim_old[0], dim_new[0]):
                for ih in range(min(dim_old[1], dim_new[1])):
                    self._mkwidget(iw, ih, size_cell=size_cell)
        if dim_new[1] > dim_old[1]:
            for iw in range(min(dim_old[0], dim_new[0])):
                for ih in range(dim_old[1], dim_new[1]):
                    self._mkwidget(iw, ih, size_cell=size_cell)
        for iw in range(dim_old[0], dim_new[0]):
            for ih in range(dim_old[1], dim_new[1]):
                self._mkwidget(iw, ih, size_cell=size_cell)

    @staticmethod
    def _reset(widget, index):
        raise NotImplementedError

    def apply(self, func):
        for iw in range(self.dim[0]):
            for ih in range(self.dim[1]):
                func(self.dummy.grid_slaves(column=iw, row=ih)[0].grid_slaves()[0], (iw, ih))

    def change_dim(self, dim, identical, conserve_size=None, size=None, size_type=None, *args, **kwargs):
        if self.dim != dim:
            if conserve_size is not None:
                if conserve_size:
                    size = self.size
                    size_type = self.size_type
            elif size is None or size_type is None:
                size = None
                size_type = None
            if size_type == Grid.GRID:
                size_cell = (size[0] // dim[0], size[1] // dim[1])
            elif size_type == Grid.CELL:
                size_cell = size
            if identical:
                if size_type == Grid.GRID:
                    for iw in range(min(self.dim[0], dim[0])):
                        for ih in range(min(self.dim[1], dim[1])):
                            self.dummy.grid_slaves(column=iw, row=ih)[0].configure(width=size_cell[0], height=size_cell[1])
                if dim[0] < self.dim[0]:
                    for iw in reversed(range(dim[0], self.dim[0])):
                        for ih in reversed(range(self.dim[1])):
                            self.dummy.grid_slaves(column=iw, row=ih)[0].destroy()
                if dim[1] < self.dim[1]:
                    for iw in reversed(range(min(self.dim[0], dim[0]))):
                        for ih in reversed(range(dim[1], self.dim[1])):
                            self.dummy.grid_slaves(column=iw, row=ih)[0].destroy()

                self._mkgrid(self.dim, dim, size=size, size_type=size_type)
            else:
                self.dummy.destroy()
                self.dummy = tk.Frame(self)
                self.dummy.grid()
                self.args = args
                self.kwargs = kwargs.copy()
                self._mkgrid((0, 0), dim, size=size, size_type=size_type)


class GameGrid(Grid):
    class COLORS():
        UNUSED = '#E0EEC6'
        GOAL = 'light green'
        NORMAL = '#243E36'
        TEXT = '#9CA68A'

    def __init__(self, dim, master=None):
        size = (25, 25)
        size_type = GameGrid.CELL
        super().__init__(dim, GameGrid._btn_init, master=master, size=size, size_type=size_type)

    @staticmethod
    def _btn_init(master=None, *args, **kwargs):
        btn = tk.Button(master=master, bg=GameGrid.COLORS.UNUSED, border=2, relief='groove')
        def _command():
            if btn.cget('bg') == GameGrid.COLORS.UNUSED:
                btn.configure(bg=GameGrid.COLORS.GOAL, text='GOAL', font=font.Font(size=btn.master.cget('width') // 4, weight='bold'))
            else:
                btn.destroy()
                entry = tk.Entry(master=master, bg=GameGrid.COLORS.NORMAL, fg=GameGrid.COLORS.TEXT, font=font.Font(size=12, weight='bold'), justify='center', border=2, relief='groove')
                entry.grid(sticky='news')
        btn.configure(command=_command)
        return btn

    @staticmethod
    def _reset(cell, index):
        master = cell.master
        cell.destroy()
        cell = GameGrid._btn_init(master=master)
        cell.grid(sticky='news')

    def reset(self):
        self.apply(GameGrid._reset)

    def change_dim(self, dim):
        super().change_dim(dim, True, conserve_size=True)

    # TODO REWRITE
    def get(self):
        cells = []
        for iw in range(self.dim[0]):
            cells_w = []
            cells.append(cells_w)
            for ih in range(self.dim[1]):
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


class SolGrid(Grid):
    class COLORS():
        UNUSED = '#E0EEC6'
        GOAL = 'light green'
        NORMAL = '#243E36'
        TEXT = '#9CA68A'

    def __init__(self, dim, master=None, *args, **kwargs):
        size = (25, 25)
        size_type = SolGrid.CELL
        super().__init__(dim, SolGrid._lbl_init, master=master, size=size, size_type=size_type, *args, **kwargs)

    @staticmethod
    def _lbl_init(master=None, *args, **kwargs):
        # normal cell font size = 12
        # goal cell font size = 6
        lbl = tk.Label(master=master, bg=SolGrid.COLORS.UNUSED, text='C', font=font.Font(size=12, weight='bold'), justify='center', border=2, relief='groove')
        return lbl

    @staticmethod
    def _reset(label, index):
        pass

    def change_dim(self, dim):
        super().change_dim(dim, True, conserve_size=True)


class App(tk.Frame):
    def __init__(self, title, master=None):
        super().__init__(master)
        self.master.title(title)
        self.master.minsize(width=150, height=0)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(sticky='news')

        self.upper = tk.Frame(self)
        for i in range(3):
            self.upper.grid_columnconfigure(i, weight=1)
            self.upper.grid_rowconfigure(i, weight=1)
        self.upper.grid_columnconfigure(1, weight=0)
        self.upper.grid(column=0, row=0, sticky='news')

        self.label_dims = tk.Label(self.upper, text='Grid dimensions')
        self.entry_dimw = tk.Entry(self.upper, width=1)
        self.label_dimxdim = tk.Label(self.upper, text=' X')
        self.entry_dimh = tk.Entry(self.upper, width=1)
        self.label_dims.grid(column=0, columnspan=3, row=0)
        self.entry_dimw.grid(column=0, row=1, sticky='ew')
        self.label_dimxdim.grid(column=1, row=1)
        self.entry_dimh.grid(column=2, row=1, sticky='ew')

        def command_solve():
            #res = self.gridgame.get()
            # TODO CHECK RESULT
            #zhed = Zhed(res)
            #zhed.solve()
            #print(zhed)
            self.gridsol.grid()
            self.gridgame.grid_configure(columnspan=3)
        def command_set():
            try:
                w = int(self.entry_dimw.get())
                h = int(self.entry_dimh.get())
                if w < 1 or h < 1:
                    raise ValueError
            except ValueError:
                showerror('Dimension Error', 'Please enter positive integer dimensions!')
                return
            self.gridgame.change_dim((w, h))
            self.gridsol.change_dim((w, h))
            self.gridsol.grid_remove()
            self.gridgame.grid_configure(columnspan=6)
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
            for i in range(6):
                self.lower.grid_columnconfigure(i, weight=1)
            for i in range(2):
                self.lower.grid_rowconfigure(i, weight=1)
            self.lower.grid(column=0, row=1, sticky='news')

            self.gridgame = GameGrid((w, h), master=self.lower)
            self.gridsol = SolGrid((w, h), master=self.lower)
            self.button_reset = tk.Button(self.lower, text='Reset', bg='red', command=self.gridgame.reset)
            self.button_solve = tk.Button(self.lower, text='Solve', bg=GameGrid.COLORS.GOAL, command=command_solve)

            self.gridgame.grid(column=0, columnspan=6, row=0, sticky='nws')
            self.gridsol.grid(column=3, columnspan=3, row=0, sticky='nes')
            self.gridsol.grid_remove()

            self.button_reset.grid(column=0, columnspan=2, row=1, sticky='new')
            self.button_solve.grid(column=2, columnspan=4, row=1, sticky='new')
            self.button_start.configure(text='Set dimensions', command=command_set)

        self.button_start = tk.Button(self.upper, text='Start', command=command_start)
        self.button_start.grid(column=0, columnspan=3, row=2, sticky='new')


if __name__ == '__main__':
    app = App('Zhed')
    app.mainloop()

