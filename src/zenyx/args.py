
from typing import Union

StringOrNone = Union[str, None]

class Arguments:
    def __init__(self, sys_args: list[str], include_script_name: bool = False) -> None:
        self.args = sys_args
        if not include_script_name:
            self.args.remove(self.args[0])

        self.normals: list[str] = []
        self.modifiers: dict[str, str] = {}
        self.tags: list[str] = []

        self.sort()

    def get(self, num: int) -> StringOrNone:
        assert isinstance(num, int), "Num has to be an integer"

        if len(self.args) > num:
            return self.normals[num]
        return None
    
    def tagged(self, tag: str) -> bool:
        assert isinstance(tag, str), "Tag has to be a string"

        if self.tags.__contains__(tag):
            return True
        return False
    
    def get_modifier_value(self, mod_name: str) -> StringOrNone:
        assert isinstance(mod_name, str), "mod_name has to be a string"

        return self.modifiers.get(mod_name)

    # xy main sub1 sub2 -m --m 
    # xy main -!-> sub1..
    # xy main -m sub1

    def sort(self):
        """

        ## Default order:
        `scriptname <main arg> <sub arg 1> <sub arg 2>...`

        ## Tagged order:
        `scriptname <main arg> --<tag> <sub arg 1> --<tag> --<tag> <sub arg 2>...` \n
        -(compiled to)-> \n
        - normals: `[<main arg>, <sub arg1>, <sub arg 2>]`
        - tags: `[--<tag>, --<tag>, --<tag>]`

        ## Modifier order:
        `scriptname <main arg> -<modifier> <mod arg> <sub arg 1> --<tag>...` \n
        -(compiled to)-> \n
        - normals: `[<main arg>, <sub arg1>]`
        - tags: `[--<tag>]`
        - modifiers: `{<modifier> : <mod arg>}`

        
        """

        skipnext: bool = False
        for index, arg in enumerate(self.args):
            if skipnext:
                skipnext = False
                continue

            if arg.startswith("--"):
                self.tags.append(arg[2:])
                continue

            if arg.startswith("-"):
                if len(self.args) == index + 1:
                    self.args.append(None)
                self.modifiers[arg[1:]] = self.args[index + 1]
                skipnext = True
                continue

            self.normals.append(arg)
                
