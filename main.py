
from modules.cpu_scheduling import run_cpu_scheduling
from modules.memory_management import run_memory_management
from modules.deadlock import run_deadlock_management
from modules.disk_scheduling import run_disk_scheduling
from modules.performance_reports import show_performance_reports


def show_menu():
    print("\n=============================================")
    print("       OS RESOURCE MANAGEMENT SYSTEM")
    print("=============================================")
    print("1. CPU Scheduling")
    print("2. Memory Management")
    print("3. Deadlock Management")
    print("4. Disk Scheduling")
    print("5. Performance Reports")
    print("0. Exit")
    print("=============================================")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (0-5): ").strip()

        if choice == "1":
            run_cpu_scheduling()

        elif choice == "2":
            run_memory_management()

        elif choice == "3":
            run_deadlock_management()

        elif choice == "4":
            run_disk_scheduling()

        elif choice == "5":
            show_performance_reports()

        elif choice == "0":
            print("\nThank you for using OS Resource Manager!")
            print("Exiting program...")
            break

        else:
            print("\nInvalid choice. Please enter a number from 0 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram terminated safely.")
