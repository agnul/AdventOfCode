class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.n_rows = len(lines)
        self.n_cols = len(lines[0])

    def rows(self):
        return iter(self.lines)

    def cols(self, row):
        return iter(self.lines[row])

    def at(self, r, c):
        if not (0 <= r < self.n_rows
                and 0 <= c < self.n_cols):
            return None
        return self.lines[r][c]

    def up(self, r, c, dist=1):
        return self.at(r - dist, c)

    def down(self, r, c, dist=1):
        return self.at(r + dist, c)

    def right(self, r, c, dist=1):
        return self.at(r, c + dist)

    def left(self, r, c, dist=1):
        return self.at(r, c - dist)
