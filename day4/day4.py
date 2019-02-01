import re
from datetime import datetime
import numpy as np


class GuardManager:
    def __init__(self):
        self._guard_dict = {}

    def update_guard_timetable(self, guard_id, sleep_time, wake_time):
        """Adds the sleeping period to the guard's timetable."""
        # If the guard is not in the dictionary, add it
        if guard_id not in self._guard_dict:
            # Minutes of the day, starting from 00:00 and ending in 23:59
            self._guard_dict[guard_id] = self._sleeptimes = np.zeros(60*24 - 1,
                                                                     dtype=int)
        
        # Update minutes slept on the guard's timetable
        timetable = self._guard_dict[guard_id]
        start_time = time_to_minutes(sleep_time)
        end_time = time_to_minutes(wake_time)
        if end_time > start_time:
            timetable[start_time:end_time] += 1
        else:
            # Time wraps around
            timetable[end_time:] += 1
            timetable[:start_time] += 1
    
    def find_laziest_guard(self):
        """Returns the id of the guard that has slept the most."""
        return max(self._guard_dict.keys(),
                   key=lambda k: self._guard_dict[k].sum())

    def find_most_slept_minute(self, guard_id):
        """Return the minute in which the given guard has slept the most."""
        if guard_id not in self._guard_dict:
            raise KeyError("Guard not found.")
        return np.argmax(self._guard_dict[guard_id])

    def find_most_slept_minute_all_guards(self):
        """Find the most slept minute among all guards.

        Return the guard's id and the minute.
        """
        current_id = current_minute = current_max = 0

        for guard_id, timetable in self._guard_dict.items():
            max_minute = self.find_most_slept_minute(guard_id)
            # Get the actual number of minutes
            max_minute_count = self._guard_dict[guard_id][max_minute]
            # Update current if necessary
            if max_minute_count > current_max:
                current_minute = max_minute
                current_max = max_minute_count
                current_id = guard_id
        
        return current_id, current_minute


def time_to_minutes(time):
    """Translate a datetime time to the minute of the day."""
    return time.hour * 60 + time.minute


def get_sorted_statements(statements):
    statements_sorted = []

    # For each statement, make a tuple of the datetime and the string after
    for stm in statements:
        match = re.match(r'\[([^]]*)\] (.*)', stm)
        timestamp = match.group(1)  # The datetime in string format
        stm_string = match.group(2)  # The statement string
        statements_sorted.append((datetime.strptime(timestamp, '%Y-%m-%d %H:%M'),
                                  stm_string))

    # Sort by datetime
    return sorted(statements_sorted, key=lambda x: x[0])


def parse_all_statements(statements_sorted):
    """Return a guard manager with all the timetables updated."""
    guard_manager = GuardManager()
    current_id = -1
    sleeping = False
    sleep_time = wake_time = None

    for stm in statements_sorted:
        match = re.match(r'Guard #(\d+) begins shift', stm[1])
        # If it's a new guard, update the current id
        if match:
            current_id = int(match.group(1))
        else:
            # Not a new guard, update sleep status, and update timetable if a
            # cycle was completed
            if not sleeping:
                sleep_time = stm[0]
                sleeping = True
            else:
                wake_time = stm[0]
                sleeping = False
                # Cycle completed: update guard's timetable
                guard_manager.update_guard_timetable(current_id,
                                                     sleep_time,
                                                     wake_time)
    
    return guard_manager


def main():
    with open("input") as f:
        statements = f.read().splitlines()

    statements_sorted = get_sorted_statements(statements)
    guard_manager = parse_all_statements(statements_sorted)

    # Part 1
    laziest_guard = guard_manager.find_laziest_guard()
    mins_by_laziest_guard = guard_manager.find_most_slept_minute(laziest_guard)
    print(laziest_guard * mins_by_laziest_guard)

    # Part 2
    guard_id, max_minute = guard_manager.find_most_slept_minute_all_guards()
    print(guard_id * max_minute)


if __name__ == "__main__":
    main()
