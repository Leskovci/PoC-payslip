from azure_blob_io import (
    list_input_files,
    list_output_files,
    delete_blob
)

CONTAINER_INPUT = "inputfiles"
CONTAINER_OUTPUT = "outputfiles"


def print_table(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def show_files(files_list):
    if not files_list:
        print("(empty)\n")
        return

    for f in files_list:
        print(f"- {f}")
    print("\n")


def delete_all(files_list):
    for f in files_list:
        print(f"Deleting: {f}")
        delete_blob(f)
    print("Done.\n")


def main():
    print_table("AZURE BLOB MAINTENANCE TOOL")

    # Fetch current blob contents
    inputs = list_input_files()
    outputs = list_output_files()

    print_table("INPUT FILES")
    show_files(inputs)

    print_table("OUTPUT FILES")
    show_files(outputs)

    print("Actions:")
    print("1. Delete ALL inputfiles")
    print("2. Delete ALL outputfiles")
    print("3. Delete a single file")
    print("0. Exit")

    choice = input("\nSelect an option: ")

    # Delete ALL inputfiles
    if choice == "1":
        delete_all(inputs)

    # Delete ALL outputfiles
    elif choice == "2":
        delete_all(outputs)

    # Delete a single file
    elif choice == "3":
        filename = input("Enter exact blob filename to delete: ").strip()

        # Try matching full blob path or filename-only
        matched_input = next((f for f in inputs if f == filename or f.endswith(filename)), None)
        matched_output = next((f for f in outputs if f == filename or f.endswith(filename)), None)

        if matched_input:
            print(f"Deleting: {matched_input}")
            delete_blob(matched_input)

        elif matched_output:
            print(f"Deleting: {matched_output}")
            delete_blob(matched_output)

        else:
            print("File not found in either container.")

    else:
        print("Exiting.")


if __name__ == "__main__":
    main()
