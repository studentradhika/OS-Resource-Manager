
def calculate_need(allocation, maximum):
    """Need = Maximum - Allocation."""
    need = []

    for i in range(len(allocation)):
        row = []
        for j in range(len(allocation[i])):
            row.append(maximum[i][j] - allocation[i][j])
        need.append(row)

    return need


def is_safe_state(allocation, maximum, available):
    """Check whether all processes can finish safely."""
    process_count = len(allocation)
    resource_count = len(available)

    need = calculate_need(allocation, maximum)
    work = available.copy()
    finished = [False] * process_count
    safe_sequence = []

    while len(safe_sequence) < process_count:
        found_process = False

        for i in range(process_count):
            if finished[i]:
                continue

            # Check whether this process's remaining need can be met.
            can_finish = True

            for j in range(resource_count):
                if need[i][j] > work[j]:
                    can_finish = False
                    break

            if can_finish:
                # Process finishes and releases its allocated resources.
                for j in range(resource_count):
                    work[j] += allocation[i][j]

                finished[i] = True
                safe_sequence.append(i)
                found_process = True

        # If no process can finish, the state is unsafe.
        if not found_process:
            return False, safe_sequence, need

    return True, safe_sequence, need


def print_matrix(title, matrix):
    print(f"\n{title}")
    for i, row in enumerate(matrix):
        print(f"P{i}: {row}")


def run_deadlock_management():
    print("\n===== DEADLOCK MANAGEMENT =====")
    print("Banker's Algorithm - Safety Check")

    try:
        process_count = int(input("Enter number of processes (1-20): "))
        resource_count = int(input("Enter number of resource types (1-10): "))

        if not 1 <= process_count <= 20:
            print("Error: Processes must be between 1 and 20.")
            return

        if not 1 <= resource_count <= 10:
            print("Error: Resource types must be between 1 and 10.")
            return

        resource_names = [
            chr(ord("A") + i) for i in range(resource_count)
        ]

        allocation = []
        maximum = []

        print("\nEnter Allocation matrix.")
        print("For each process, enter resource values separated by spaces.")

        for i in range(process_count):
            values = list(map(
                int,
                input(f"Allocation for P{i}: ").split()
            ))

            if len(values) != resource_count or any(v < 0 for v in values):
                print("Error: Enter the correct number of non-negative values.")
                return

            allocation.append(values)

        print("\nEnter Maximum matrix.")

        for i in range(process_count):
            values = list(map(
                int,
                input(f"Maximum for P{i}: ").split()
            ))

            if len(values) != resource_count or any(v < 0 for v in values):
                print("Error: Enter the correct number of non-negative values.")
                return

            for j in range(resource_count):
                if values[j] < allocation[i][j]:
                    print(
                        f"Error: Maximum cannot be less than Allocation "
                        f"for P{i}, resource {resource_names[j]}."
                    )
                    return

            maximum.append(values)

        available = list(map(
            int,
            input(
                "\nEnter Available resources "
                f"({resource_count} values): "
            ).split()
        ))

        if len(available) != resource_count or any(v < 0 for v in available):
            print("Error: Enter the correct number of non-negative values.")
            return

        need = calculate_need(allocation, maximum)

        print_matrix("ALLOCATION MATRIX", allocation)
        print_matrix("MAXIMUM MATRIX", maximum)
        print_matrix("NEED MATRIX", need)
        print("\nAvailable:", available)

        safe, sequence, need = is_safe_state(
            allocation, maximum, available
        )

        print("\n===== RESULT =====")

        if safe:
            sequence_text = " -> ".join(f"P{p}" for p in sequence)
            print("System is in a SAFE STATE.")
            print("Safe sequence:", sequence_text)
            print("All processes can finish in this order.")
        else:
            sequence_text = " -> ".join(f"P{p}" for p in sequence)
            print("System is in an UNSAFE STATE.")
            if sequence_text:
                print("Processes that could finish:", sequence_text)
            print("No complete safe sequence exists.")

    except ValueError:
        print("Error: Please enter integers only.")
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
