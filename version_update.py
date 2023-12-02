
import os
import re
import time


root_folder = "\\".join(__file__.split("\\")[0:-1])

def __get_current_version() -> str:
    with open(os.path.join(root_folder, "src", "zenyx", "__init__.py")) as read_file:
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


def __update_version(update_type: 0 or 1 or 2):
    current = __get_current_version().split(".")
    __new_version = [int(current[0]), int(current[1]), int(current[2])]
    
    __new_version[abs(-2 + update_type)] += 1
    new_version = []
    
    if update_type == 0:
        pass
    
    elif update_type == 1:
        __new_version[2] = 0
        
    elif update_type == 2:
        __new_version[2] = 0
        __new_version[1] = 0
    
    for x in __new_version:
        new_version.append(str(x))

    
    with open(os.path.join(root_folder, "src", "zenyx", "__init__.py"), "r+") as file:
        version_replaced: str = __replace_first_version(file.read(), ".".join(new_version))
        file.seek(0)
        file.write(version_replaced)
        
    with open(os.path.join(root_folder, "pyproject.toml"), "r+") as file:
        version_replaced: str = __replace_first_version(file.read(), ".".join(new_version))
        file.seek(0)
        file.write(version_replaced)
        
    return ".".join(new_version)


def __delete_files_in_folder(folder_path):
    try:
        # Get the list of files in the folder
        files = os.listdir(folder_path)

        # Iterate through the files and delete each one
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        print(f"All files in {folder_path} have been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    try:
        new_v: str = ""
        
        update_type: int = int(input("0 - Patch | 1 - Minor | 2 - Major | 3 - Amend | 4 - Chore\nPatch type: "))
        
        option_dict = {
            3: "Amend",
            4: "Chore"
        }
        
        version_number = __get_current_version()
        
        if update_type <= 2 and update_type >= 0:
            new_v = __update_version(update_type)
            version_number = new_v
        elif update_type <= 4 and update_type >= 3:
            new_v = option_dict[update_type]
        else:
            raise ValueError
            
        commit_title: str = input("Commit title: ")
        commit_description: str = input("Commit description: ")
        
        amend_text = ""
        if update_type == 3:
            amend_text = " --amend"
        
        os.system("git add .")
        os.system(f"git commit{amend_text} -m \"{new_v} | {commit_title}\" -m \"{commit_description}\"")
        
        def push_next():
            os.system("git push")
            
            __delete_files_in_folder(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist"))
            os.system("python -m build")
            try:
                os.system("python -m twine upload --verbose --repository  testpypi dist/*")
            except:
                print("Version already uploaded")
                
            __range = 10
            print(f"Waiting for package upload... ({__range}s)", end="")
            for i in range(__range):
                time.sleep(1)
                print(f"Waiting for package upload... ({__range - i}s)", end="\r")
                
            os.system("python -m pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade zenyx")
            
        
        try:
            push_next()
        except: 
            print("failed to push to current branch")
    except ValueError:
        print("Incorrect input :(")

if __name__ == "__main__":
    main()