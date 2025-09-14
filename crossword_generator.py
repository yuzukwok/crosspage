import random
from typing import List, Tuple, Dict

class CrosswordCell:
    def __init__(self):
        self.char = ''
        self.is_black = False

class Crossword:
    def __init__(self, words: List[str], size: int = 12):
        self.words = [w.upper() for w in words]
        self.size = size
        self.grid = [[CrosswordCell() for _ in range(size)] for _ in range(size)]
        self.placed_words = []  # (word, row, col, direction)

    def can_place(self, word, row, col, direction):
        if direction == 'across':
            if col + len(word) > self.size:
                return False
            for i, c in enumerate(word):
                cell = self.grid[row][col + i]
                if cell.char not in ('', c):
                    return False
        else:
            if row + len(word) > self.size:
                return False
            for i, c in enumerate(word):
                cell = self.grid[row + i][col]
                if cell.char not in ('', c):
                    return False
        return True

    def place_word(self, word, row, col, direction):
        if direction == 'across':
            for i, c in enumerate(word):
                self.grid[row][col + i].char = c
        else:
            for i, c in enumerate(word):
                self.grid[row + i][col].char = c
        self.placed_words.append((word, row, col, direction))

    def generate(self):
        # 简单策略：第一个单词横向放在中间，后续尽量交叉
        self.place_word(self.words[0], self.size // 2, (self.size - len(self.words[0])) // 2, 'across')
        for word in self.words[1:]:
            placed = False
            for pw, prow, pcol, pd in self.placed_words:
                for i, pc in enumerate(pw):
                    for j, wc in enumerate(word):
                        if pc == wc:
                            if pd == 'across':
                                row = prow - j
                                col = pcol + i
                                if 0 <= row < self.size and 0 <= col < self.size:
                                    if self.can_place(word, row, col, 'down'):
                                        self.place_word(word, row, col, 'down')
                                        placed = True
                                        break
                            else:
                                row = prow + i
                                col = pcol - j
                                if 0 <= row < self.size and 0 <= col < self.size:
                                    if self.can_place(word, row, col, 'across'):
                                        self.place_word(word, row, col, 'across')
                                        placed = True
                                        break
                    if placed:
                        break
                if placed:
                    break
            if not placed:
                # 随机找个能放的位置
                for _ in range(100):
                    direction = random.choice(['across', 'down'])
                    row = random.randint(0, self.size - 1)
                    col = random.randint(0, self.size - 1)
                    if self.can_place(word, row, col, direction):
                        self.place_word(word, row, col, direction)
                        break

    def to_grid(self) -> List[List[str]]:
        return [[cell.char if cell.char else '' for cell in row] for row in self.grid]

    def get_layout(self) -> List[Dict]:
        # 返回每个单词的布局信息
        return [
            {'word': w, 'row': r, 'col': c, 'direction': d}
            for w, r, c, d in self.placed_words
        ]

def generate_crossword(words: List[str], size: int = 12):
    cw = Crossword(words, size)
    cw.generate()
    return cw.to_grid(), cw.get_layout()

if __name__ == '__main__':
    # 示例
    words = ['apple', 'banana', 'orange', 'grape', 'pear', 'peach']
    grid, layout = generate_crossword(words)
    for row in grid:
        print(' '.join(c if c else '.' for c in row))
    print(layout)
