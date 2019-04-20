import recognize

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits

def cross(A,B):
    return [a + b for a in A for b in B]

squares = cross(rows, cols)

unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in squares)

class Sudoku:
  def __init__(self, blocks, image):
    self._initBlock(blocks, image)

  def _initBlock(self, blocks, image):
    index = 0
    self.blocks = {}
    recognizer = recognize.Recognize()
    for c in cols:
      for r in rows:
        self.blocks[r+c] = {}
        self.blocks[r+c]['block'] = blocks[index]
        x,y,w,h = blocks[index]
        block_num = image[y+5:y + h-5, x+5:x + w-5]
        num = recognizer.recognizing(block_num)
        self.blocks[r+c]['value'] = num
        self.blocks[r+c]['is_show'] = True
        if num != 0:
            self.blocks[r+c]['is_show'] = False
        index += 1

  def toString(self):
    test_str = ''
    for r in rows:
      for c in cols:
        num = self.blocks[r+c]['value']
        test_str += str(num)
    return test_str

  def parse_grid(self, grid):
    # Convert grid to a dict of possible values,{square: digits}, or
    # return False if a contridiction is detected.
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    # print grid_values(grid).items()
    for s, d in self.grid_values(grid).items():
        if d in digits and not self.assign(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
    return values

  def grid_values(self, grid):
    # "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

  def assign(self, values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(self.eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False
  def eliminate(self, values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(self.eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
    if len(dplaces) == 0:
        return False ## Contradiction: no place for this value
    elif len(dplaces) == 1:
        # d can only be in one place in unit; assign it there
        if not self.assign(values, dplaces[0], d):
            return False
    return values

  def search(self, values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return self.some(self.search(self.assign(values.copy(), s, d))
        for d in values[s])

  def some(self, seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

  def result(self):
    # "Display these values as a 2-D grid."
    values = self.parse_grid(self.toString())
    values = self.search(values)
    if not values:
        print('Cannot solve')
        return False
    for block in values.items():
      key, value = block
      self.blocks[key]['value'] = value
      # print (self.blocks[key])
    return True
