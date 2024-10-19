import subprocess
import os
import sys

def install_dependencies():
    """Installs Node.js dependencies and apk-mitm."""
    try:
        # Check if Node.js is installed
        node_check = subprocess.run(["node", "-v"], capture_output=True, text=True)
        if node_check.returncode != 0:
            print("Node.js not found. Please install it from https://nodejs.org/")
            sys.exit(1)
        
        # Install apk-mitm globally using npm
        print("Installing apk-mitm...")
        subprocess.run(["npm", "install", "-g", "apk-mitm"], check=True)
        print("All dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during installation: {e}")
        sys.exit(1)

def patch_apk(input_apk_path, output_dir):
    """Patches the APK to bypass SSL pinning."""
    try:
        os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

        # Run apk-mitm command
        command = ["apk-mitm", input_apk_path, "-o", output_dir]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Successfully patched APK. Output saved to: {output_dir}")
        else:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

def main():
    # Check if OpenJDK is installed
    java_check = subprocess.run(["java", "-version"], capture_output=True, text=True)
    if java_check.returncode != 0:
        print("OpenJDK not found. Please install it from https://jdk.java.net/ and try again.")
        sys.exit(1)

    # Install necessary dependencies
    install_dependencies()

    # Get APK path and output directory from user
    input_apk = input("Enter the path to the APK file: ").strip()
    output_directory = input("Enter the output directory path: ").strip()

    # Check if the provided APK file exists
    if not os.path.isfile(input_apk):
        print("The specified APK file does not exist. Please check the path and try again.")
        sys.exit(1)

    # Patch the APK
    patch_apk(input_apk, output_directory)

if __name__ == "__main__":
    main()
