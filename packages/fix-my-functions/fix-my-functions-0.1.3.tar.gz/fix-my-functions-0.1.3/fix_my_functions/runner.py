from .config import CONFIG
from .formatters import FORMATTING_PASSES
from .helpers import color_diff, print_error
from .helpers import debug1, debug2, debug3, debug4
from pathlib import Path
from redbaron import RedBaron
import difflib


def process_file(fname: Path, *, interactive: bool = False, accept: bool = False, dry: bool = False, no_diff: bool = False):
    assert sum(map(bool, [interactive, accept, dry])) == 1
    if no_diff: assert dry

    with fname.open() as f:
        orig_src = f.read()
        try:
            red = RedBaron(orig_src)
        #except baron.parser.ParsingError as e:
        except Exception as e:
            print_error(f"== {e.__class__.__name__}: ==\n{e}\n")
            return
        assert red.dumps() == orig_src

    def ask_and_write(red: RedBaron) -> bool:
        new_src = red.dumps()
        if dry:
            if no_diff:
                print(new_src)
            else:
                view_diff(fname, new_src)
            return True
        elif accept or view_diff_ask_accept(fname, new_src):
            with open(fname, "w") as f:
                f.write(new_src)
            return True
        return False

    for formatting_pass in FORMATTING_PASSES:
        #name = formatting_pass.__name__.capitalize().replace("__", " - ").replace("_", " ")
        #print("    -", name)

        #print("    -", name, end="\r")
        #print()
        #sys.stdout.write("\033[K") # clear to end of line

        #debug3(red)
        red = formatting_pass(red, interactive=ask_and_write if interactive else None)
        ask_and_write(red)
        #debug3(red)

def view_diff(fname: Path, new_src: str):
    #if shutil.which("diff"):
    #    subprocess.run([
    #            "diff",
    #            "-Bwu",
    #            "--color",
    #            fname,
    #            "-",
    #        ], input=new_src, text=True)
    #    #TODO: check if diff returned success due to no difference
    #elif shutil.which("git"):
    #    subprocess.run([
    #            "git",
    #            "diff",
    #            "-U0",
    #            #"--word-diff",
    #            #"--word-diff-regex=[<]|[>]|[^[:space:]]",
    #            "--no-index",
    #            "--", fname, "-"
    #        ], input=new_src, text=True)
    #    #TODO: check if diff returned success due to no difference
    #else:

    with fname.open() as f:
        original_file = f.read()

    diff = list(difflib.unified_diff(
        original_file.splitlines(keepends=True),
        new_src      .splitlines(keepends=True),
        fromfile = str(fname),
        tofile   = str(fname),
    ))
    if diff:
        print(
            *color_diff(diff, force=CONFIG.color),
            sep="",
        )
        return True
    else:
        return False

def view_diff_ask_accept(fname: Path, new_src: str) -> bool:
    if view_diff(fname, new_src):
        return input("Apply changes? [y/N] ").lower().startswith("y")
    else:
        return False
