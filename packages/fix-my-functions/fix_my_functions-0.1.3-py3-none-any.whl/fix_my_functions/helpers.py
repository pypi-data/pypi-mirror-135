from .config import CONFIG
from functools import reduce
from colorama import Fore
from redbaron import nodes
from typing import Union, Iterable, Any
import json
import os
import sys

# baron helpers:

def is_self_arg(def_argument_node: nodes.DefArgumentNode) -> bool:
    return (def_argument_node.index_on_parent == 0
        and def_argument_node.type            == "def_argument"
        and def_argument_node.target.type     == "name"
        and def_argument_node.target.value    in {"self", "cls"}
        and not def_argument_node.annotation
    )

def make_comma() -> nodes.CommaNode:
    return nodes.CommaNode({
        "type"              : "comma",
        "first_formatting"  :  "",
        "second_formatting" :  "",
    })

def make_whitespace(value) -> Union[nodes.SpaceNode, nodes.EndlNode]:
    endl, indent = value.rstrip(" \t"), value.lstrip("\r\n")
    if endl:
        return nodes.EndlNode({
            "type"       : "endl",
            "value"      :  endl,
            "indent"     :  indent,
            "formatting" : [],
        })
    else:
        return nodes.SpaceNode({
            "type"  : "space",
            "value" :  indent,
        })

def make_multiline_comments(comment_nodes: list[nodes.CommentNode], whitespace_head: str, whitespace_sep: str, whitespace_tail: str) -> Iterable[nodes.Node]:
    yield make_whitespace(whitespace_head)
    for i, comment_node in enumerate(comment_nodes):
        if i != 0:
            yield make_whitespace(whitespace_sep)
        yield comment_node
    yield make_whitespace(whitespace_tail)

# pretty-print helpers

def color_diff(diff: list[str], force: bool = False) -> Iterable[str]:
    if not force and not os.isatty(1):
        yield from diff
    else:
        for line in diff:
            if line.startswith('+++'):
                yield f"{ Fore.CYAN   }{ line }{ Fore.RESET }"
            elif line.startswith('---'):
                yield f"{ Fore.BLUE   }{ line }{ Fore.RESET }"
            elif line.startswith('+'):
                yield f"{ Fore.GREEN }{ line }{ Fore.RESET }"
            elif line.startswith('-'):
                yield f"{ Fore.RED   }{ line }{ Fore.RESET }"
            elif line.startswith('^'):
                yield f"{ Fore.BLUE  }{ line }{ Fore.RESET }"
            elif line.startswith('@@') and line.rstrip().endswith("@@"):
                yield f"{ Fore.MAGENTA  }{ line }{ Fore.RESET }"
            else:
                yield line

def print_error(* a, ** kw):
    if os.isatty(2) or CONFIG.color:
        print(Fore.RED, end="", file=sys.stderr)
        print(*a, **kw, file=sys.stderr)
        print(Fore.RESET, end="", file=sys.stderr)
        sys.stderr.flush()
    else:
        print(*a, **kw, file=sys.stderr)


# itertools

def elementwise_max(iterable: Iterable):
    return reduce(lambda xs, ys: [*map(max, zip(xs, ys))], iterable)


# print debugging

def debug1(*a, **kw):
    return print(*map(repr, a), **kw)

def debug2(obj: Any):
    return debug1(dir(obj))

def debug3(obj: nodes.Node):
    return print(debug4(obj))

def debug4(obj: nodes.Node):
    return json.dumps(obj.fst(), indent=4)
