from .config import CONFIG
from .helpers import is_self_arg, make_comma, make_whitespace, make_multiline_comments
from .helpers import elementwise_max
from .helpers import debug1, debug2, debug3, debug4
from redbaron import RedBaron
from typing import Callable, Optional
import json


FormattingPass      = Callable[[RedBaron, ...], RedBaron]
InteractiveCallable = Optional[Callable[[RedBaron], bool]]

FORMATTING_PASSES: list[FormattingPass] = []
def _formatting_pass(func):
    FORMATTING_PASSES.append(func)
    return func

# === formatting passes

@_formatting_pass
def tabulate_function_definitions(red: RedBaron, *, interactive: InteractiveCallable) -> RedBaron:
    for i, node in enumerate(red.find_all("def")):
        backup_node = node.copy()

        #debug1(node)

        # read/derive indent levels
        indent_def = str(node.get_indentation_node() or "\n")
        indent_body = str(node.value[0].get_indentation_node() or "\n")
        indent_diff = indent_body.removeprefix(indent_def)
        if indent_diff:
            #debug1(indent_def)
            #debug1(indent_body)
            assert node.value.node_list[0].type == "endl"
        else:
            assert node.value.node_list[0].type != "endl"
            indent_diff = " " * CONFIG.tab_width # TODO: support tabs
            indent_body += indent_diff
            if node.value.node_list[0].type == "space":
                node.value.node_list[0].replace(make_whitespace(indent_body))
            else:
                node.value.node_list.insert(0, make_whitespace(indent_body))
        indent_args = indent_body + indent_diff

        # store some user comments before we wipe them below
        def_comment_nodes_head = [
            *(i.copy() for i in node.async_formatting .find_all("comment")),
            *(i.copy() for i in node.first_formatting .find_all("comment")),
            *(i.copy() for i in node.second_formatting.find_all("comment")),
            *(i.copy() for i in node.third_formatting .find_all("comment")),
        ]
        def_comment_nodes_tail = [
            *(i.copy() for i in node.fourth_formatting.find_all("comment")),
            *(i.copy() for i in node.return_annotation_first_formatting .find_all("comment")),
            *(i.copy() for i in node.return_annotation_second_formatting.find_all("comment")),
            *(i.copy() for i in node.fifth_formatting .find_all("comment")),
            *(i.copy() for i in node.sixth_formatting .find_all("comment")),
        ]
        try:
            has_def_argument_comments = bool(node.arguments[is_self_arg(node.arguments[0]):].find("comment"))
        except IndexError:
            has_def_argument_comments = False

        # set fixed whitespace
        node.async_formatting  = " "
        node.first_formatting  = " "                   # between def and name
        node.second_formatting = ""                    # between name and (
        node.third_formatting  = ""                    # between ( and first token
        node.fourth_formatting = ""                    # between last token and )
        node.return_annotation_first_formatting  = " " # before ->
        node.return_annotation_second_formatting = " " # after ->
        node.fifth_formatting  = ""                    # before :
        node.sixth_formatting  = ""                    # after :

        #debug2(node)
        #debug1(node.arguments)
        #debug2(node.arguments)

        supported_arg_node_types = {
            "def_argument",        # foo   : bar = baz
            "list_argument",       # *foo  : bar
            "dict_argument",       # **foo : bar
            "kwargs_only_marker",  # *
            #"args_only_marker,    # /, not implemented in baron
        }
        assert all(arg_node.type in supported_arg_node_types for arg_node in node.arguments), debug4(node.arguments)
        n_items = bool(node.return_annotation) + sum(
            1 + bool(arg_node.annotation) + bool(arg_node.value)
            if arg_node.type != "kwargs_only_marker" else
            1
            for arg_node in node.arguments
            if not is_self_arg(arg_node)
        )
        if n_items >= 5 or "\n" in node.arguments.dumps():
            node.third_formatting = indent_args

            l1m, l2m, l3m = elementwise_max(
                (
                    len(str(arg_node.target     or "")),
                    len(str(arg_node.annotation or "")),
                    len(str(arg_node.value      or "")),
                )
                if arg_node.type == "def_argument" else
                (
                    len(str(arg_node.value      or "")) + 1 + (arg_node.type == "dict_argument"),
                    len(str(arg_node.annotation or "")),
                    0,
                )
                for arg_node in node.arguments
                if not is_self_arg(arg_node)
                    and not arg_node.type == "kwargs_only_marker"
            )

            #if node.arguments.node_list.find("comment") and node..find("comment"):

            # ensure trailing comma
            if not node.arguments.has_trailing:
                node.arguments.node_list.append(make_comma())

            for arg_node in node.arguments:
                assert arg_node.type in supported_arg_node_types, arg_node.type

                if arg_node.type in {
                        "list_argument",
                        "dict_argument",
                        "kwargs_only_marker",
                        }:
                    arg_node.formatting = ""

                comma_node = arg_node.next
                assert comma_node
                assert comma_node.type == "comma", comma_node.type

                if is_self_arg(arg_node): # special case for "self" and "cls"
                    node.third_formatting                 = ""
                    arg_node.first_formatting             = ""
                    arg_node.second_formatting            = ""
                    arg_node.annotation_first_formatting  = ""
                    arg_node.annotation_second_formatting = ""

                    comment_nodes = [*def_comment_nodes_head, *comma_node.find_all("comment")]
                elif arg_node.type != "kwargs_only_marker":
                    l1, l2, l3 = (
                        (
                            len(str(arg_node.target     or "")),
                            len(str(arg_node.annotation or "")),
                            len(str(arg_node.value      or "")),
                        )
                        if arg_node.type == "def_argument" else
                        (
                            len(str(arg_node.value      or "")) + 1 + (arg_node.type == "dict_argument"),
                            len(str(arg_node.annotation or "")),
                            0,
                        )
                    )

                    # annotations
                    arg_node.annotation_first_formatting  = " " * (1 + l1m - l1)
                    arg_node.annotation_second_formatting = " "

                    # default values
                    if arg_node.type == "def_argument":
                        arg_node.first_formatting         = " " * (1 + l2m - l2 + (l1m - l1 + 3)*(not l2))
                        arg_node.second_formatting        = " "

                    comment_nodes = comma_node.find_all("comment")

                # comments and endl
                comma_node.first_formatting  = ""
                if comment_nodes:
                    sep  = indent_args + " " * (l1m + 3 + l2m + 3 + l3m + 1 + 2)
                    comma_column = comma_node.absolute_bounding_box.top_left.column

                    do_dedent_top_comment = is_self_arg(arg_node) \
                        and (len(comment_nodes) > 1 or not has_def_argument_comments)

                    if do_dedent_top_comment:
                        sep = indent_args + " " * (comma_column + 2 - len(indent_args.lstrip("\r\n")))

                    lead = " " * (len(sep.lstrip("\r\n")) - comma_column)
                    #lead = " " * (2 + l3m - l3)

                    # eww
                    if do_dedent_top_comment:
                        comma_column -= indent_diff.count("\t") * (CONFIG.tab_width-1) * 2
                        sep = indent_args + " " * (comma_column + 2 - len(indent_args.lstrip("\r\n")))

                    comma_node.second_formatting.clear()
                    comma_node.second_formatting.extend(
                        make_multiline_comments(comment_nodes, lead, sep, indent_args)
                    )
                else:
                    comma_node.second_formatting = indent_args

            # final comments
            if def_comment_nodes_tail:
                assert node.value.node_list[0].type == "endl", json.dumps(node.value.node_list[0].fst(), indent=4)
                column = node.value.node_list[0].absolute_bounding_box.top_left.column
                sep    = indent_args + " " * (l1m + 3 + l2m + 3 + l3m + 1 + 2)
                lead   = " " * (len(sep.lstrip("\r\n")) - column)

                if not has_def_argument_comments:
                    sep = sep[:-(len(lead) - 2)]
                    lead = " " * 2

                #node.sixth_formatting.clear()
                node.sixth_formatting.extend(
                    make_multiline_comments(def_comment_nodes_tail, lead, sep, indent_args)
                )
        else:
            node.replace(backup_node)
            continue

        if interactive:
            if node.dumps() != backup_node.dumps():
                if not interactive(red):
                    # rollback
                    node.replace(backup_node)

    return red


# TODO: def tabulate_function_calls

# TODO: def tabulate_dictionaries

# TODO: def tabulate_assignment_blocks
