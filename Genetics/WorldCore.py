import random


class World:
    def __init__(self, width, height, colors, count):
        self.food_map = []
        self.item_map = []
        self.width = width
        self.height = height
        self.cell_width = width // count
        self.cell_height = height // count
        self.count = count

        for i in range(0, count):
            t = []
            u = []
            for j in range(0, count):
                t.append(colors.copy())
                u.append(0)
            self.food_map.append(t)
            self.item_map.append(u)

    def get_chunk_x(self, x):
        return int((x // self.cell_width) % self.count)

    def item_at(self, x, y):
        cx = self.get_chunk_x(x)
        cy = self.get_chunk_y(y)
        return self.item_map[cx][cy] != 0

    def get_item_at(self, x, y):
        cx = self.get_chunk_x(x)
        cy = self.get_chunk_y(y)
        return self.item_map[cx][cy]

    def set_item_at(self, x, y, item=0):
        cx = self.get_chunk_x(x)
        cy = self.get_chunk_y(y)
        self.item_map[cx][cy] = item

    def get_chunk_y(self, y):
        return int((y // self.cell_height) % self.count)

    def get_food_at_chunk(self, x, y):
        # print(self.food_map[x % self.count][y % self.count])
        return self.food_map[x % self.count][y % self.count]

    def __set_food_at_chunk(self, x, y, value):
        self.food_map[x % self.count][y % self.count] = value

    def get_food_by_hue(self, x, y, hue):
        cx = self.get_chunk_x(x)
        cy = self.get_chunk_y(y)
        return self.get_food_at_chunk(cx, cy)[hue]

    def get_food_at_chunk_by_hue(self, cx, cy, hue):
        return self.food_map[cx % self.count][cy % self.count][hue]

    def set_food_at_chunk_by_hue(self, cx, cy, value, hue):
        self.food_map[cx % self.count][cy % self.count][hue] = value

    def __get_food(self, x, y):
        cx = self.get_chunk_x(x)
        cy = self.get_chunk_y(y)
        return self.get_food_at_chunk(cx, cy)

    def __set_food(self, x, y, value):
        cx = self.get_chunk_x(x)
        cy = self.get_chunk_y(y)
        self.__set_food_at_chunk(cx, cy, value)

    def set_food_by_hue(self, x, y, value, hue):
        cx = self.get_chunk_x(x)
        cy = self.get_chunk_y(y)
        self.food_map[cx][cy][hue] = value

    def refill(self, cx, cy, param, hue):
        food = self.get_food_at_chunk_by_hue(cx, cy, hue)
        # print(food, param, hue)
        if food < 255:
            self.set_food_at_chunk_by_hue(cx, cy, food + param, hue)

    def can_be_refilled(self, cx, cy, hue):
        return self.get_food_by_hue(cx, cy, hue) < 255 and self.get_food_by_hue(cx, cy, hue) != -1

    def refill_chunk(self, cx, cy, param, hue):
        food = self.get_food_at_chunk_by_hue(cx, cy, hue)
        # print(food, param, hue)
        if food < 255:
            self.set_food_at_chunk_by_hue(cx, cy, food + param, hue)

    def can_chunk_be_refilled(self, cx, cy, hue):
        return self.get_food_at_chunk_by_hue(cx, cy, hue) < 255 and self.get_food_at_chunk_by_hue(cx, cy, hue) != -1

    def update(self):
        if random.randint(0, 625) < 80:
            for i in range(0, self.count):
                for j in range(0, self.count):
                    # if game_map[i][j][0] < 250 and game_map[i][j][0] != -1:
                    #     # print('restored')
                    #     game_map[i][j][0] = game_map[i][j][0] + 1

                    if self.can_chunk_be_refilled(i, j, 1):
                        self.refill_chunk(i, j, 1, 1)
                    if self.can_chunk_be_refilled(i, j, 2):
                        self.refill_chunk(i, j, 1, 0)

                    # if game_map[i][j][2] < 250 and game_map[i][j][2] != -1:
                    #     # print('restored')
                    #     game_map[i][j][2] = game_map[i][j][2] + 1
                    # pass
