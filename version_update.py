
import os
import re

root_folder = "\\".join(__file__.split("\\")[0:-1])

def __get_current_version() -> str:
    with open(os.path.join(root_folder, "zenyx", "__init__.py")) as read_file:
        pattern = r'\b\d+\.\d+\.\d+\b'
        version_numbers = re.findall(pattern, read_file.read())
        return version_numbers[0]

print(__get_current_version())

def main():
    commit_title: str = input("Commit title: ")
    commit_description: str = input("Commit description: ")
    
    os.system("git add .")
    os.system(f"git commit -m \"{__get_current_version()} | {commit_title}\" -m \"{commit_description}\"")
    
    try:
        os.system("git push")
    except: 
        print("failed to push to current branch")

if __name__ == "__main__":
    main()