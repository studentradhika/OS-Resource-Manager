
from modules.cpu_scheduling import fcfs, sjf, round_robin
from modules.memory_management import allocate_memory, display_results
from modules.deadlock import calculate_need, is_safe_state


def show_cpu_report():
    print("\n========== CPU PERFORMANCE REPORT ==========")

    try:
        count = int(input("Enter number of processes: "))

        if not 1 <= count <= 100:
            print("Enter process count between 1 and 100.")
            return

        processes = []

        for i in range(count):
            print(f"\nProcess P{i + 1}")

            arrival = int(input("Arrival Time: "))
            burst = int(input("Burst Time: "))

            if arrival < 0 or burst <= 0:
                print("Invalid input.")
                return

            processes.append({
                "pid": f"P{i + 1}",
                "arrival": arrival,
                "burst": burst
            })

        quantum = int(input("\nEnter Round Robin Time Quantum: "))

        if quantum <= 0:
            print("Time quantum must be positive.")
            return

        algorithms = {
            "FCFS": fcfs(processes),
            "SJF": sjf(processes),
            "Round Robin": round_robin(processes, quantum)
        }

        print("\n========== COMPARISON TABLE ==========")
        print(f"{'Algorithm':<18}{'Avg Waiting':<18}{'Avg Turnaround'}")

        report = []

        for name, results in algorithms.items():
            avg_wait = sum(p["waiting"] for p in results) / len(results)
            avg_tat = sum(p["turnaround"] for p in results) / len(results)

            report.append((name, avg_wait, avg_tat))

            print(f"{name:<18}{avg_wait:<18.2f}{avg_tat:.2f}")

        best = min(report, key=lambda x: x[1])

        print("\nBest Algorithm:", best[0])
        print("Average Waiting Time:", round(best[1], 2))
        print("Average Turnaround Time:", round(best[2], 2))

    except ValueError:
        print("Please enter valid integer values.")

    except (EOFError, KeyboardInterrupt):
        print("\nReport cancelled.")


def show_memory_report():
    print("\n========== MEMORY PERFORMANCE REPORT ==========")

    try:
        block_count = int(input("Number of memory blocks: "))

        if not 1 <= block_count <= 100:
            print("Enter between 1 and 100 blocks.")
            return

        blocks = []

        for i in range(block_count):
            size = int(input(f"Size of block {i + 1} (KB): "))

            if size <= 0:
                print("Block size must be positive.")
                return

            blocks.append(size)

        process_count = int(input("\nNumber of processes: "))

        if not 1 <= process_count <= 100:
            print("Enter between 1 and 100 processes.")
            return

        processes = []

        for i in range(process_count):
            size = int(input(f"Memory required by P{i + 1} (KB): "))

            if size <= 0:
                print("Process size must be positive.")
                return

            processes.append(size)

        methods = ["First Fit", "Best Fit", "Worst Fit"]
        report = []

        print("\n========== MEMORY COMPARISON ==========")
        print(f"{'Algorithm':<15}{'Allocated':<15}{'Not Allocated':<18}{'Free Memory'}")

        for method in methods:
            allocations, remaining = allocate_memory(
                blocks, processes, method
            )

            allocated = sum(
                1 for item in allocations
                if item["block"] != "Not Allocated"
            )

            not_allocated = len(processes) - allocated
            total_free = sum(remaining)

            report.append((method, allocated, not_allocated, total_free))

            print(
                f"{method:<15}{allocated:<15}"
                f"{not_allocated:<18}{total_free} KB"
            )

            display_results(method, allocations, remaining)

        best = max(report, key=lambda x: (x[1], -x[2]))

        print("\n========== MEMORY ANALYSIS ==========")
        print("Best Allocation Method:", best[0])
        print("Processes Allocated:", best[1])
        print("Processes Not Allocated:", best[2])
        print("Remaining Memory:", best[3], "KB")

    except ValueError:
        print("Please enter valid whole numbers.")

    except (EOFError, KeyboardInterrupt):
        print("\nReport cancelled.")

def show_deadlock_report():
    print("\n========== DEADLOCK PERFORMANCE REPORT ==========")

    try:
        process_count = int(input("Number of processes: "))
        resource_count = int(input("Number of resource types: "))

        if not 1 <= process_count <= 20:
            print("Processes must be between 1 and 20.")
            return

        if not 1 <= resource_count <= 10:
            print("Resource types must be between 1 and 10.")
            return

        allocation = []
        maximum = []

        print("\nEnter Allocation Matrix:")

        for i in range(process_count):
            row = list(map(int, input(f"P{i}: ").split()))

            if len(row) != resource_count or any(x < 0 for x in row):
                print("Invalid allocation values.")
                return

            allocation.append(row)

        print("\nEnter Maximum Matrix:")

        for i in range(process_count):
            row = list(map(int, input(f"P{i}: ").split()))

            if len(row) != resource_count or any(x < 0 for x in row):
                print("Invalid maximum values.")
                return

            if any(row[j] < allocation[i][j] for j in range(resource_count)):
                print("Maximum cannot be less than allocation.")
                return

            maximum.append(row)

        available = list(map(
            int,
            input("Enter available resources: ").split()
        ))

        if len(available) != resource_count or any(x < 0 for x in available):
            print("Invalid available resources.")
            return

        need = calculate_need(allocation, maximum)

        safe, sequence, need = is_safe_state(
            allocation, maximum, available
        )

        print("\n========== DEADLOCK ANALYSIS ==========")
        print("Need Matrix:", need)
        print("Available Resources:", available)

        if safe:
            print("\nSystem Status: SAFE")
            print(
                "Safe Sequence:",
                " -> ".join(f"P{p}" for p in sequence)
            )
            print("All processes can complete successfully.")
        else:
            print("\nSystem Status: UNSAFE")
            print("No complete safe sequence exists.")

        print("\n========== REPORT COMPLETED ==========")

    except ValueError:
        print("Enter valid integer values.")

    except (EOFError, KeyboardInterrupt):
        print("\nReport cancelled.")



def show_performance_reports():

    while True:
        print("\n========== PERFORMANCE REPORTS ==========")
        print("1. CPU Scheduling Comparison")
        print("2. Memory Management Comparison")
        print("0. Back to Main Menu")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            show_cpu_report()

        elif choice == "2":
            show_memory_report()

        elif choice == "0":
            break

        else:
            print("Invalid choice. Try again.")
