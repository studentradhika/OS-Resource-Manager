def allocate_memory(blocks, processes, method):
    remaining = blocks.copy()
    allocations = []

    for pid, size in enumerate(processes, start=1):
        suitable = [
            i for i, block in enumerate(remaining)
            if block >= size
        ]

        if not suitable:
            allocations.append({
                "pid": f"P{pid}",
                "size": size,
                "block": "Not Allocated",
                "remaining": "-"
            })
            continue

        if method == "First Fit":
            index = suitable[0]

        elif method == "Best Fit":
            index = min(suitable, key=lambda i: remaining[i])

        elif method == "Worst Fit":
            index = max(suitable, key=lambda i: remaining[i])

        else:
            raise ValueError("Unknown allocation method")

        remaining[index] -= size

        allocations.append({
            "pid": f"P{pid}",
            "size": size,
            "block": index + 1,
            "remaining": remaining[index]
        })

    return allocations, remaining


def display_results(method, allocations, remaining):
    print(f"\n--- {method} Results ---")
    print(f"{'Process':<12}{'Size KB':<12}{'Block':<18}{'Block Left KB'}")

    for item in allocations:
        print(
            f"{item['pid']:<12}"
            f"{item['size']:<12}"
            f"{str(item['block']):<18}"
            f"{item['remaining']}"
        )

    total_free = sum(remaining)
    print("\nTotal free memory:", total_free, "KB")


def run_memory_management():
    print("\n=== MEMORY MANAGEMENT ===")

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

        print("\n1. First Fit")
        print("2. Best Fit")
        print("3. Worst Fit")
        print("4. Compare all")

        choice = input("Choose method: ").strip()

        methods = {
            "1": ["First Fit"],
            "2": ["Best Fit"],
            "3": ["Worst Fit"],
            "4": ["First Fit", "Best Fit", "Worst Fit"]
        }

        if choice not in methods:
            print("Invalid method choice.")
            return

        for method in methods[choice]:
            allocations, remaining = allocate_memory(
                blocks, processes, method
            )
            display_results(method, allocations, remaining)

    except ValueError:
        print("Invalid input. Please enter whole numbers.")