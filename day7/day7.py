import re


def get_available(status):
    """Get the available tasks at the current status, sorted."""
    return sorted([task for task in status.keys() if not status[task]])


def make_task(task, status):
    """
    Do the task, removing it from the status and the requirements
    from other tasks.
    """
    if status[task]:
        raise ValueError("Task has unmet requirements.")
    # Remove the task
    del status[task]
    # Remove from other task's requirements
    for reqs in status.values():
        if task in reqs:
            reqs.remove(task)


def read_instructions(instructions):
    """Reads the list of instructions and returns a map of requirements."""
    requirements = {}
    for stm in instructions:
        match = re.match(r'Step (.) must be finished before step (.) can begin', stm)
        required = match.group(1)
        step = match.group(2)
        if step not in requirements:
            requirements[step] = [required]
        else:
            requirements[step].append(required)
        # Also add the requirement if it is not in the map
        if required not in requirements:
            requirements[required] = []
    return requirements


def process(status):
    """
    Perform all the tasks in the required order until no tasks remain,
    and return the resulting string.
    """
    result = ""
    available = get_available(status)
    while available:
        task = available[0]
        make_task(task, status)
        result += task
        available = get_available(status)
    return result


def main():
    with open("input") as f:
        inp = f.read().splitlines()
    
    # Part 1
    requirements = read_instructions(inp)
    print(process(requirements))
    

if __name__ == "__main__":
    main()
