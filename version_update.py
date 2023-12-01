
import os
import re

root_folder = "\\".join(__file__.split("\\")[0:-1])

def __get_current_version() -> str:
    with open(os.path.join(root_folder, "zenyx", "__init__.py")) as read_file:
        pattern = r'\b\d+\.\d+\.\d+\b'
        version_numbers = re.findall(pattern, read_file.read())
        return version_numbers[0]
    
def __replace_first_version(input_text, custom_version):
    # Define a pattern to match version numbers in the format x.x.x
    version_pattern = re.compile(r'\b\d+\.\d+\.\d+\b')

    # Find all version numbers in the text
    version_numbers = version_pattern.findall(input_text)

    # Replace the first version number with the custom input
    if version_numbers:
        first_version = version_numbers[0]
        result_text = version_pattern.sub(custom_version, input_text, count=1)
        return result_text
    else:
        # No version numbers found
        return input_text

print(__get_current_version())

def __update_version(update_type: 0 or 1 or 2):
    current = __get_current_version().split(".")
    __new_version = [int(current[0]), int(current[1]), int(current[2])]
    
    __new_version[abs(-2 + update_type)] += 1
    new_version = []
    
    for x in __new_version:
        new_version.append(str(x))
    
    
    with open(os.path.join(root_folder, "zenyx", "__init__.py"), "r+") as file:
        version_replaced: str = __replace_first_version(file.read(), ".".join(new_version))
        file.seek(0)
        file.write(version_replaced)
    

def main():
    try:
        update_type: int = int(input("0 - Patch | 1 - Minor | 2 - Major\nPatch type: "))
        __update_version(update_type)
        commit_title: str = input("Commit title: ")
        commit_description: str = input("Commit description: ")
        
        os.system("git add .")
        os.system(f"git commit -m \"{__get_current_version()} | {commit_title}\" -m \"{commit_description}\"")
        
        try:
            os.system("git push")
        except: 
            print("failed to push to current branch")
    except ValueError:
        print("Incorrect input :(")

if __name__ == "__main__":
    main()