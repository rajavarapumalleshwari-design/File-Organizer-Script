import os
import shutil
import logging
import argparse


# Configure logging
logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_unique_path(destination):
    """
    If a file already exists, create a unique filename.
    Example:
    report.pdf
    report_1.pdf
    report_2.pdf
    """
    if not os.path.exists(destination):
        return destination

    folder = os.path.dirname(destination)
    filename = os.path.basename(destination)

    name, extension = os.path.splitext(filename)
    counter = 1

    while True:
        new_filename = f"{name}_{counter}{extension}"
        new_path = os.path.join(folder, new_filename)

        if not os.path.exists(new_path):
            return new_path

        counter += 1


def organize_folder(folder, dry_run=False):
    """
    Organize files in the given folder according to their extensions.
    """

    if not os.path.isdir(folder):
        print(f"Error: Folder does not exist: {folder}")
        return

    for filename in os.listdir(folder):

        source = os.path.join(folder, filename)

        # Ignore folders
        if not os.path.isfile(source):
            continue

        # Get file extension
        extension = os.path.splitext(filename)[1].lower()

        # Files without an extension go into 'Others'
        if extension:
            extension = extension[1:]  # Remove '.'
            destination_folder = os.path.join(folder, extension)
        else:
            destination_folder = os.path.join(folder, "Others")

        destination = os.path.join(destination_folder, filename)

        # Handle duplicate filenames
        destination = get_unique_path(destination)

        if dry_run:
            print(f"[DRY RUN] {filename} -> {destination_folder}")
            logging.info(
                f"[DRY RUN] Would move {source} -> {destination}"
            )
        else:
            # Create destination folder
            os.makedirs(destination_folder, exist_ok=True)

            # Move file
            shutil.move(source, destination)

            print(f"Moved: {filename} -> {destination_folder}")
            logging.info(f"Moved {source} -> {destination}")


def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a folder by their extensions."
    )

    parser.add_argument(
        "folder",
        help="Path of the folder to organize"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without moving files"
    )

    args = parser.parse_args()

    organize_folder(args.folder, args.dry_run)


if __name__ == "__main__":
    main()