import re


def create_rule_map(rulelist):
    rules = {}
    for rule in rulelist:
        rules[rule[:5]] = rule[-1]
    return rules


def get_surroundings(pos, state):
    surroundings = ''
    for i in range(pos - 2, pos + 3):
        if 0 <= i < len(state):
            surroundings += state[i]
        else:
            surroundings += '.'
    return surroundings


def evolution_step(state, rules, leftmost):
    """Perform an evolution step."""
    new_state = []
    i = -1
    while i <= len(state):
        surroundings = get_surroundings(i, state)
        if surroundings not in rules:
            cell = '.'
        else:
            cell = rules[surroundings]
        if not ((i == -1 or i == len(state)) and cell == '.'):
            new_state.append(cell)
            if i == -1:
                leftmost -= 1
        i += 1
    return new_state, leftmost


def evolve(initial_state, rules, generations):
    """
    Performs all evolution steps and returns the final state and the
    number of the leftmost pot.
    """
    state = initial_state
    leftmost = 0
    for i in range(generations):
        state, leftmost = evolution_step(state, rules, leftmost)
    return state, leftmost


def pot_numbers(state, leftmost):
    """Return the sum of the indexs of the pots that have plants."""
    result = 0
    for i in range(len(state)):
        if state[i] == '#':
            result += leftmost + i
    return result


def main():
    with open("input") as f:
        match = re.match(r'^.*:\s(.*)$', f.readline().strip())
        state = match.group(1)
        # Blank line
        f.readline()
        rulelist = f.read().splitlines()
    
    # Part 1
    rules = create_rule_map(rulelist)
    final_state, leftmost = evolve(state, rules, 20)
    print(pot_numbers(final_state, leftmost))


if __name__ == "__main__":
    main()
