import numpy as np
from IPython.display import clear_output, display_html
import time

def evolve(cells, rule, steps, display='always', colors = ['white', 'black']):
    """
    Evolves a grid of cells a number of steps according to a rule function.
    
    Parameters
    ----------
    cells: an MxN array of ints
        A starting grid of cells.
    rule: function
        A function handle which 
        The function must be callable as rule(self, neighbors[])
        and return the new value for the self.
    steps: int
        Number of steps to take
    display : string
        Determines how often the grid is shown.
        'always' - after each step
        'never' - does not display
        'end' - displays after the last step.
    colors : array of strings
        See how colors is defined for the show_cells function.
        The default here is the same.
    """
    
    nx, ny = cells.shape # Size of the grid
    buffer = np.empty_like(cells) # Make a buffer
    neighbors = np.zeros(8, dtype='int') # Each cell has 8 neighbors
    
    # Loop over each step
    for step in range(steps):

        # Loop over all cells
        for x in np.arange(nx):
            for y in np.arange(ny):
                
                neighbors[0] = 0 if (x == 0    or y == 0   ) else cells[x-1, y-1]
                neighbors[1] = 0 if (             y == 0   ) else cells[x  , y-1]
                neighbors[2] = 0 if (x == nx-1 or y == 0   ) else cells[x+1, y-1]
                neighbors[3] = 0 if (x == 0                ) else cells[x-1, y  ]
                neighbors[4] = 0 if (x == nx-1             ) else cells[x+1, y  ]
                neighbors[5] = 0 if (x == 0    or y == ny-1) else cells[x-1, y+1]
                neighbors[6] = 0 if (             y == ny-1) else cells[x  , y+1]
                neighbors[7] = 0 if (x == nx-1 or y == ny-1) else cells[x+1, y+1]
                #print(x, y, sum(neighbors), neighbors)               
        
                buffer[x, y] = rule(cells[x, y], neighbors)
        
        # Swap the two
        cells, buffer = buffer, cells
        
        # Show the cells when requested
        if (display == "always" or (step == steps-1 and display == "end")):
            show_grid(cells, colors)
    
    return cells
    

def show_grid(cells, colors = ['white', 'black'], pause=0.2):
    """
    Makes an html table of the current state of the board and displays it.
    
    Parameters
    ----------
    cells : MxN array of ints
        The grid of cells to be displayed.
    colors : array of strings
        Each entry is the html name of a color associated with its index.
        The default will display all 0s in the board as white, and all 1s as black.
    pause : float
        Adds a small delay after displaying the board, to make animation easier.
    """
    nx, ny = cells.shape
    table = '<table style="border-color: black; border-width: 5px;">\n'
    for y in np.arange(ny-1, -1, -1):
        table += '<tr>'
        for x in np.arange(0, nx):
            table += '<td style="background: '+colors[cells[x, y]]+'; border-color: white;"></td>'
        table += '</tr>\n'
    table += '</table>'
    clear_output(wait=True)
    display_html(table, raw=True)
    time.sleep(pause)
