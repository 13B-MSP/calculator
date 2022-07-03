import argparse
from functools import partial
import operator
from typing import Callable, NoReturn, Sequence, Union

_OPERANDS = {
    "+": operator.add,
    "-": operator.sub,
    "/": operator.truediv,
    "*": operator.mul
}

_NUMBERS = "0123456789"
_VALID_CHARS = f"{_OPERANDS}{_NUMBERS}. "

CalcSequence = Sequence[Union[str, float]]

def _create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('calc_expr', type=str, nargs='+',
        help="the calculator expression to evaluate, ie. 5+5")
    return parser

def _output_printer(expr: str, output: float) -> None:
    """Prints formatted ouput of expression"""
    print(f"{expr} = {output}")

def _raise_not_valid_error(expr: str) -> NoReturn:
    """Raises a formatted ValueError for invalid expression"""
    raise ValueError(f"'{expr}' not a valid calculator expression")

def _parse_expr(expr: str) -> CalcSequence:
    """Parse calculator expression"""
    number = ""
    multiplier = 1
    sequence: CalcSequence = []
    for c in expr:
        if c in _NUMBERS:
            number += c
        elif c in _OPERANDS:
            if c == '-' and not number:
                multiplier *= -1
            elif number:
                sequence.extend([multiplier * float(number), c])
                number = ""
            else:
                _raise_not_valid_error(expr)
        elif c in ',.':
            if '.' in number:
                _raise_not_valid_error(expr)
            number += '.'
    if number:
        sequence.append(multiplier * float(number))
    return sequence

def _resolve_calc_sequence(seq: CalcSequence) -> float:
    """Resolve the calc sequence to float"""
    total = 0.0
    fu: Callable[[float], float] = lambda n: n
    for ent in seq:
        if ent in _OPERANDS:
            fu = partial(_OPERANDS[ent], fu(total))
        else:
            total = fu(ent)
            fu = lambda n: n
    return fu(total)

def _calculate(expr: str) -> float:
    """
    Calculate the sequence
    
    Raise ValueError if expr not valid"""
    if not all(c in _VALID_CHARS for c in expr):
        _raise_not_valid_error(expr)
    calc_sequence = _parse_expr(expr)
    return _resolve_calc_sequence(calc_sequence)

def main(*args: str) -> int:
    """Main entry point"""
    parser = _create_arg_parser()
    parsed_args = parser.parse_args(args)
    expr = "".join(parsed_args.calc_expr).replace(',', '.')
    if not expr:
        return -1
    _output_printer(expr, _calculate(expr))
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(*sys.argv[1:]))
