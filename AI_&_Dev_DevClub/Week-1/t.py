import subprocess
import os
import re

# --- Configuration ---
DISK_IMAGE_PATH = "/home/sumit/Downloads/disk_image.dd"
RECOVERY_DIR = "/home/sumit/Downloads/recovered_files_from_dd"  # Where recovered files will be saved


# --- Main Script ---

def run_command(command, check_errors=True, capture_output=True):
    """Helper to run a shell command."""
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,  # Decode stdout/stderr as text
            check=check_errors,  # Raise CalledProcessError if command returns non-zero exit status
            shell=False  # Prefer direct execution, arguments are already a list
        )
        return result
    except FileNotFoundError:
        print(f"Error: Command not found. Make sure '{command[0]}' is installed and in your PATH.")
        exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}")
        print(f"Stderr: {e.stderr}")
        if check_errors:
            exit(1)  # Exit if critical command like fls fails


def recover_files():
    """Recovers files from the disk image to the specified recovery directory."""
    print(f"Starting recovery from: {DISK_IMAGE_PATH}")
    print(f"Target recovery directory: {RECOVERY_DIR}")

    if os.path.exists(RECOVERY_DIR):
        print(f"Warning: Recovery directory '{RECOVERY_DIR}' already exists.")
        print("Existing files might be overwritten if their names collide.")
    else:
        os.makedirs(RECOVERY_DIR)
        print(f"Created recovery directory: {RECOVERY_DIR}")

    # Step 1: Run fls to list files
    print("\nRunning fls to enumerate files...")
    fls_command = ["fls", "-r", "-l", DISK_IMAGE_PATH]
    fls_result = run_command(fls_command)

    lines = fls_result.stdout.strip().split('\n')

    file_count = 0
    recovered_count = 0
    failed_count = 0

    print("Parsing fls output and preparing for extraction...")

    # Regex to parse fls output lines:
    # Captures: 1. file_type (e.g., d/d, r/r, -/r, V/V)
    #           2. inode number
    #           3. full path
    # It accounts for leading spaces (for nested directories) and the optional '*' for deleted files.
    fls_line_pattern = re.compile(r'^\s*([drV-]+/[drV-]+)\s+(?:\*\s+)?(\d+):\s+(.*)$')

    for line in lines:
        match = fls_line_pattern.match(line)
        if not match:
            # print(f"Skipping unparsable line: {line}") # Uncomment for debugging if lines are missed
            continue

        file_type_raw, inode, path = match.groups()

        # We are interested in "regular files" (r/r) and potentially "deleted regular files" (-/r).
        # We want to explicitly exclude directories (d/d) and special volume entries (V/V).
        if 'r' not in file_type_raw:  # Check if 'r' (regular file) is in the type string
            # This filters out 'd/d' and 'V/V' but keeps 'r/r' and '-/r'
            # print(f"Skipping non-regular file/directory type: {file_type_raw} {path}") # Uncomment for debugging
            continue

        file_count += 1

        # Construct the full destination path
        # lstrip('/') handles cases where 'path' might start with '/', avoiding '//' in the join
        dest_path = os.path.join(RECOVERY_DIR, path.lstrip('/'))

        # Create parent directories if they don't exist
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except OSError as e:
                print(f"Error creating directory {dest_dir}: {e}")
                failed_count += 1
                continue

        # Step 2: Use icat to extract the file content
        icat_command = ["icat", DISK_IMAGE_PATH, inode]

        print(f"Recovering file {recovered_count + 1}/{file_count} (inode {inode}): {path}")

        try:
            # Open the destination file in binary write mode
            with open(dest_path, 'wb') as f:
                # Run icat and redirect its stdout directly to the file
                subprocess.run(
                    icat_command,
                    stdout=f,
                    stderr=subprocess.PIPE,  # Capture stderr for error messages from icat itself
                    check=True  # Raise an error if icat fails for this specific file
                )
            recovered_count += 1
        except subprocess.CalledProcessError as e:
            print(f"Error extracting {path} (inode {inode}): {e.stderr.strip()}")
            failed_count += 1
        except IOError as e:
            print(f"Error writing to file {dest_path}: {e}")
            failed_count += 1

    print("\n--- Recovery Summary ---")
    print(f"Total potential files identified (regular files only): {file_count}")
    print(f"Successfully recovered files: {recovered_count}")
    print(f"Failed to recover files: {failed_count}")
    print(f"Recovery completed. Check '{RECOVERY_DIR}' for extracted files.")


if __name__ == "__main__":
    recover_files()