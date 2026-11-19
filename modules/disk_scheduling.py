
def calculate_movement(sequence, initial_head):
    """Calculate total disk head movement."""
    movement = 0
    current = initial_head

    for request in sequence:
        movement += abs(request - current)
        current = request

    return movement


def fcfs(requests, initial_head):
    """Serve requests in the given order."""
    sequence = requests.copy()
    movement = calculate_movement(sequence, initial_head)
    return sequence, movement


def sstf(requests, initial_head):
    """Serve the nearest pending request first."""
    pending = requests.copy()
    sequence = []
    current = initial_head

    while pending:
        nearest = min(pending, key=lambda request: abs(request - current))
        sequence.append(nearest)
        pending.remove(nearest)
        current = nearest

    movement = calculate_movement(sequence, initial_head)
    return sequence, movement



def scan(requests, initial_head, disk_size, direction):
    """SCAN: move toward disk end, then reverse direction."""
    lower = sorted(
        (request for request in requests if request < initial_head),
        reverse=True
    )
    higher = sorted(
        request for request in requests if request >= initial_head
    )

    sequence = []

    if direction == "right":
        sequence.extend(higher)

        if initial_head != disk_size - 1:
            sequence.append(disk_size - 1)

        sequence.extend(reversed(lower))

    else:
        sequence.extend(lower)

        if initial_head != 0:
            sequence.append(0)

        sequence.extend(higher)

    movement = calculate_movement(sequence, initial_head)
    return sequence, movement



def display_result(name, sequence, movement):
    print(f"\n{name}")
    print("Service sequence:", " -> ".join(map(str, sequence)))
    print("Total head movement:", movement, "cylinders")


def run_disk_scheduling():
    print("\n===== DISK SCHEDULING =====")

    try:
        disk_size = int(input("Enter total number of cylinders: "))

        if disk_size < 2:
            print("Error: Disk must have at least 2 cylinders.")
            return

        initial_head = int(input("Enter initial head position: "))

        if not 0 <= initial_head < disk_size:
            print("Error: Head position must be within the disk range.")
            return

        requests = list(map(
            int,
            input("Enter disk requests separated by spaces: ").split()
        ))

        if not requests:
            print("Error: Enter at least one disk request.")
            return

        if any(request < 0 or request >= disk_size for request in requests):
            print(f"Error: Requests must be between 0 and {disk_size - 1}.")
            return

        print("\nChoose algorithm:")
        print("1. FCFS")
        print("2. SSTF")
        print("3. SCAN")
        print("4. Compare all")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            sequence, movement = fcfs(requests, initial_head)
            display_result("FCFS", sequence, movement)

        elif choice == "2":
            sequence, movement = sstf(requests, initial_head)
            display_result("SSTF", sequence, movement)

        elif choice == "3":
            direction = input("Enter direction (left/right): ").strip().lower()

            if direction not in ("left", "right"):
                print("Error: Direction must be left or right.")
                return

            sequence, movement = scan(
                requests, initial_head, disk_size, direction
            )
            display_result("SCAN", sequence, movement)

        elif choice == "4":
            sequence, movement = fcfs(requests, initial_head)
            display_result("FCFS", sequence, movement)

            sequence, movement = sstf(requests, initial_head)
            display_result("SSTF", sequence, movement)

            for direction in ("left", "right"):
                sequence, movement = scan(
                    requests, initial_head, disk_size, direction
                )
                display_result(f"SCAN ({direction})", sequence, movement)

        else:
            print("Invalid choice. Enter a number from 1 to 4.")

    except ValueError:
        print("Error: Please enter valid integers.")
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
