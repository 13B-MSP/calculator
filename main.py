import argparse
from functools import partial
import operator
from typing import Any, Callable, Sequence, Union

_OPERANDS = {
    "+": operator.add,
    "-": operator.sub
    # "/": operator.truediv,
    # "*": operator.mul
}

_NUMBERS = "0123456789"
_VALID_CHARS = f"{_OPERANDS}{_NUMBERS} "

CalcSequence = Sequence[Union[str, int]]

def _create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('calc_expr', type=str, nargs='+',
        help="the calculator expression to evaluate, ie. 5+5")
    return parser

def _output_printer(expr: str, output: Any) -> None:
    """Prints formatted ouput of expression"""
    print(f"{expr} = {output}")

def _parse_expr(expr: str) -> CalcSequence:
    """Parse calculator expression"""
    num = ""
    seq: CalcSequence = []
    for c in expr:
        if c in _NUMBERS:
            num += c
        elif c == ' ':
            if num:
                seq.append(int(num))
                num = ""
        elif c in _OPERANDS:
            if num:
                seq.append(int(num))
                num = ""
            if (not seq and not num) or (seq and seq[-1] in _OPERANDS):
                raise ValueError("Not allowed: ", seq, expr, c)
            seq.append(c)
    if num:
        seq.append(int(num))
    return seq

def _resolve_calc_sequence(seq: CalcSequence) -> int:
    """Resolved the calc sequence to an int"""
    total = 0
    fu: Callable[[int], int] = lambda n: n
    for ent in seq:
        if ent in _OPERANDS:
            fu = partial(_OPERANDS[ent], fu(total))
        else:
            total = fu(ent)
            fu = lambda n: n
    return fu(total)

def _calculate(expr: str) -> int:
    """
    Calculate the sequence
    
    Raise ValueError if expr not valid"""
    if not all(c in _VALID_CHARS for c in expr):
        raise ValueError(f"'{expr}' not a valid calculator expression")
    calc_sequence = _parse_expr(expr)
    return _resolve_calc_sequence(calc_sequence)

def main(*args: str) -> int:
    """Main entry point"""
    parser = _create_arg_parser()
    parsed_args = parser.parse_args(args)
    expr = "".join(parsed_args.calc_expr)
    if not expr:
        return -1
    _output_printer(expr, _calculate(expr))
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(*sys.argv[1:]))
