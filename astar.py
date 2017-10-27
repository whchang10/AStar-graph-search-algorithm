import state


class Search:
    def __init__(self, first_state, env):
        self.env = env
        self.frontier = []
        self.visited = []
        first_state.energy = env.energy_budget
        self.frontier.append(first_state)

    def is_goal(self, cur_state):
        return (cur_state.pos_x == self.env.end_x) and (cur_state.pos_y == self.env.end_y)

    def elev(self, pos_x, pos_y):
        return self.env.elevations[pos_y][pos_x]

    @staticmethod
    def is_in_range(var, var_range):
        return (var < var_range) and (var >= 0)

    def est_cost(self, cur_x, cur_y, next_x, next_y):
        cur_elev = self.elev(cur_x, cur_y)
        next_elev = self.elev(next_x, next_y)
        if next_elev > cur_elev:
            return 1 + (next_elev - cur_elev) ** 2
        elif next_elev < cur_elev:
            return 1 + (cur_elev - next_elev)
        else:
            return 1

    def calc_heuristic(self, x, y):
        return abs(self.env.end_x - x) + abs(self.env.end_y - y) + \
               abs(self.elev(self.env.end_x, self.env.end_y) - self.elev(x, y))

    def has_enough_energy(self, cur_state, next_x, next_y):
        cost = self.est_cost(cur_state.pos_x, cur_state.pos_y, next_x, next_y)
        return cost <= cur_state.energy

    def is_visited(self, x, y):
        matches = [state for visited_state in self.visited
                   if (x == visited_state.pos_x) and (y == visited_state.pos_y)]
        return len(matches) != 0

    def append_frontier(self, cur_state):
        for exist_state in self.frontier:
            if (cur_state.pos_x == exist_state.pos_x) and\
               (cur_state.pos_y == exist_state.pos_y):
                if cur_state.a_star < exist_state.a_star:
                    self.frontier.remove(exist_state)
                    break
                else:
                    return

        if len(self.frontier) == 0:
            self.frontier.append(cur_state)
            return

        if cur_state.a_star < self.frontier[len(self.frontier) - 1].a_star:
            self.frontier.append(cur_state)
            return

        for index, exist_state in enumerate(self.frontier):
            if cur_state.a_star >= exist_state.a_star:
                self.frontier.insert(index, cur_state)
                break

    def search(self):
        solution = None
        directions = [('N', 0, 1), ('E', 1, 0), ('S', 0, -1), ('W', -1, 0)]

        while len(self.frontier):
            cur_state = self.frontier.pop()
            self.visited.append(cur_state)

            if self.is_goal(cur_state):
                solution = cur_state
                break

            for direction, plac_x, plac_y in directions:
                next_x = cur_state.pos_x + plac_x
                next_y = cur_state.pos_y + plac_y
                if self.is_in_range(next_x, self.env.width) and \
                   self.is_in_range(next_y, self.env.height) and \
                   self.has_enough_energy(cur_state, next_x, next_y) and\
                   not self.is_visited(next_x, next_y):
                    cur_cost = self.est_cost(cur_state.pos_x, cur_state.pos_y, next_x, next_y)
                    next_state = state.State(next_x, next_y)
                    next_state.moves_so_far = cur_state.moves_so_far + [direction]
                    next_state.direction = direction
                    next_state.cost_so_far = cur_state.cost_so_far + cur_cost
                    next_state.heuristic = self.calc_heuristic(next_x, next_y)
                    next_state.a_star = next_state.cost_so_far + next_state.heuristic
                    next_state.energy = cur_state.energy - cur_cost
                    self.append_frontier(next_state)

        return solution, self.frontier, self.visited
