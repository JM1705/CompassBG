# Script used by compassbg.py and compassBGQT.py to convert key names in the json dictionary to variable names
def translateDict(dict, to):
    # Change the names of keys so the code doesn't break
    keyChanges = [
        ["username", "unm"],
        ["password", "pwd"],
        ["background_path", "bgpath"],
        ["font_size", "fontsize"],
        ["font_file", "fontfile"],
        ["line_spacing", "linespace"],
        ["start_position", "startpos"],
        ["text_colour", "textcolour"],
        ["run_on_startup", "autorun"],
        ["high_contrast", "highcontrast"],
        ["title_size_modifier", "titlemod"],
        ["title_spacing", "titlespace"],
        ["max_tries", "maxTries"]
    ]

    to = to.lower()

    if to == "file":
        for i in keyChanges:
            dict[i[0]] = dict.pop(i[1])

    if to == "code":
        for i in keyChanges:
            dict[i[1]] = dict.pop(i[0])
    
    return dict