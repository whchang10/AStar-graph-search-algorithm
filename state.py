class State:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.moves_so_far = []

        self.direction = ''
        self.cost_so_far = 0
        self.heuristic = 0
        self.a_star = 0
        self.energy = 0

    def __str__(self):
        state_out = "Pos=(%d, %d) " % (self.pos_x, self.pos_y)
        state_out = state_out + "Moves=%s " % self.moves_so_far
        state_out = state_out + "Cost=%d" % self.cost_so_far
        # state_out = state_out + "AStar=%d " % self.a_star
        # state_out = state_out + "Heu=%d " % self.heuristic
        # state_out = state_out + "Energy=%d " % self.energy
        return state_out
