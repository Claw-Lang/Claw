"""Claw programming language

usage:
    claw compile [-ldo FILE] <file>
    claw run [-td] <file>
    claw [-hv]

options:
    -h, --help                  Shows this help menu
    -v, --version               Shows the version
    -l, --llvm                  Emit llvm code
    -o FILE, --output FILE      Output file
    -t, --timer                 Time the execution
    -d, --debug                 Debug mode
"""

import os
from typing import Dict, Any

from docopt import docopt
from claw.compiler.code_generator import CodeGenerator
from claw.lexer import Lexer
from claw.parser import Parser
from claw.type_checker import Preprocessor
from claw.utils import error


def process_file(claw_file: str) -> CodeGenerator:
    if not os.path.isfile(claw_file):
        error(claw_file + " is not a valid file")

    code = open(claw_file, encoding="utf8").read()
    lexer = Lexer(code, claw_file)
    parser = Parser(lexer)
    prog = parser.parse()
    symtab_builder = Preprocessor(claw_file)
    symtab_builder.check(prog)

    generator = CodeGenerator(claw_file)
    generator.generate_code(prog)

    return generator


def _run(arg_list: Dict[str, Any]) -> None:
    claw_file: str = arg_list['<file>']
    timer: bool = arg_list['--timer']
    debug: bool = arg_list['--debug']

    generator = process_file(claw_file)
    generator.evaluate(not debug, debug, timer)


def _compile(arg_list: Dict[str, Any]) -> None:
    claw_file: str = arg_list['<file>']
    output: str = arg_list['--output']
    emit_llvm: bool = arg_list['--llvm']
    debug: bool = arg_list['--debug']

    generator = process_file(claw_file)
    generator.compile(claw_file, not debug, output, emit_llvm)


if __name__ == "__main__":
    args: Dict[str, Any] = docopt(__doc__, version='v0.4.1')

    if args['compile']:
        _compile(args)
    elif args['run']:
        _run(args)
    else:
        exit(__doc__)
