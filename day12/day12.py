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


def seen(state, state_record):
    state = ''.join(state).strip('.')
    i = 0
    for record in state_record:
        cur_state = record[0]
        cur_state = ''.join(cur_state).strip('.')
        if state == cur_state:
            return True
        i += 1
    return False


def find_first_repeat(initial_state, rules):
    """
    Evolves until the pattern repeats, not necessarily at the same
    positions, and returns the list of all patterns found until then
    with their leftmost index.
    """
    leftmost = 0
    state = initial_state
    state_record = [(state, leftmost)]
    while True:
        state, leftmost = evolution_step(state, rules, leftmost)
        if seen(state, state_record):
            return state_record
        state_record.append((state, leftmost))


def pot_numbers(state, leftmost, shift=0):
    """Return the sum of the indexs of the pots that have plants."""
    result = 0
    for i in range(len(state)):
        if state[i] == '#':
            result += leftmost + i + shift
    return result


def main():
    with open("input") as f:
        match = re.match(r'^.*:\s(.*)$', f.readline().strip())
        state = list(match.group(1))
        # Blank line
        f.readline()
        rulelist = f.read().splitlines()

    # Part 1
    rules = create_rule_map(rulelist)
    final_state, leftmost = evolve(state, rules, 20)
    print(pot_numbers(final_state, leftmost))

    # Part 2
    record = find_first_repeat(state, rules)
    state, leftmost = record[-1]
    next_state, next_leftmost = evolution_step(state, rules, leftmost)
    print(f"Leftmost: {leftmost}")  # -2
    print(f"Leftmost difference: {next_leftmost - leftmost}")  # 0
    are_equal = ''.join(next_state).strip('.') == ''.join(state).strip('.')
    print(f"States are equal: {are_equal}")
    # After step 125 it repeats the same pattern over and over and the leftmost
    # keeps being -2, but everything is shifted 1 to the right
    print(pot_numbers(state, leftmost, shift=50000000000-124))


if __name__ == "__main__":
    main()
