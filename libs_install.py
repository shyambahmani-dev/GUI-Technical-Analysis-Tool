import subprocess

def install_dependencies():
    dependencies = ["numpy", "pandas", "scipy", "math", "sklearn", "time", "datetime", "dateutil", "csv", "os", "code", "traceback", "sys"]

    for dependency in dependencies:
        try:
            subprocess.check_call(['pip', 'install', dependency])
            print(f"Successfully installed {dependency}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {dependency}")

if __name__ == "__main__":
    print("Installing dependencies")
    install_dependencies()
    print("Dependencies installed.")
    input("Press any key to continue.")
    

