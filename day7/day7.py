import copy
import re


class WorkerManager:
    def __init__(self, status, worker_count=5):
        self.status = status
        self.worker_count = worker_count
        self.result = ""
        self.total_time = 0
        # The task each worker is currently working on
        self.doing = [None] * worker_count
        # Time left to finish the currently working task
        self.time_left = [0] * worker_count

    def assign_task(self, task):
        """Assign the task to the first available worker."""
        if not self.is_worker_available():
            raise Exception("No worker available.")
        cost = get_task_cost(task)
        next_available_worker = self.doing.index(None)
        self.doing[next_available_worker] = task
        self.time_left[next_available_worker] = cost
        # Remove the task from the status
        del self.status[task]

    def is_worker_available(self):
        """Check if there's a worker available."""
        return None in self.doing

    def all_workers_free(self):
        return all(i is None for i in self.doing)

    def finish_task(self, worker):
        task = self.doing[worker]
        assert task is not None and self.time_left[worker] == 0
        self.doing[worker] = None
        self.result += task

        # Remove from other task's requirements
        for reqs in self.status.values():
            if task in reqs:
                reqs.remove(task)

    def time_tick(self):
        """Advance one second of time.

        If any workers finish their tasks, assign the next available one,
        unless there are no more tasks.
        """
        self.total_time += 1
        for worker in range(self.worker_count):
            # Make workers work!
            if self.time_left[worker] > 0:
                assert self.doing[worker] is not None
                self.time_left[worker] -= 1

            # Check if the worker has finished its task
            if (self.time_left[worker] == 0
                    and self.doing[worker] is not None):
                    self.finish_task(worker)
        
        # Check if there are any free workers that can take a new job
        available = get_available(self.status)
        while available and self.is_worker_available():
            task = available.pop(0)
            self.assign_task(task)

    def process(self):
        """
        Process all the tasks until there are none left,
        and return the total time spent.
        """
        # Assign the first available tasks
        available = get_available(self.status)
        i = 0
        while i < len(available) and self.is_worker_available():
            self.assign_task(available[i])
            i += 1

        # Work until finished
        while self.status or not self.all_workers_free():
            self.time_tick()

        return self.total_time


def get_task_cost(task):
    """Get the cost associated to the task, including the base 60 seconds."""
    return 61 + ord(task) - ord('A')


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
        match = re.match(
            r'Step (.) must be finished before step (.) can begin', stm)
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
    status = copy.deepcopy(requirements)
    print(process(status))

    # Part 2
    status = copy.deepcopy(requirements)
    worker_manager = WorkerManager(status)
    print(worker_manager.process())


if __name__ == "__main__":
    main()
