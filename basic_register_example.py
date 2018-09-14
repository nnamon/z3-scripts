#!/usr/bin/env python

# Solving constraints where all values are 8 bit registers.
# (x << 2) + (3 * y) == 0x41
# (x >> 4) - (y << 2) > 0x10
# (x * 5) + (y * 2) == 0x42
# x != 0
# y != 0

import z3

def main():
    x = z3.BitVec('x', 8)
    y = z3.BitVec('y', 8)

    s = z3.Solver()
    s.add(((x << 2) + (3 * y)) == z3.BitVecVal(0x41, 8))
    s.add(((x >> 4) - (y << 2)) > z3.BitVecVal(0x10, 8))
    s.add(((x * 5) - (y * 2)) > z3.BitVecVal(0x42, 8))
    s.add(x != z3.BitVecVal(0, 8))
    s.add(y != z3.BitVecVal(0, 8))

    while s.check() == z3.sat:
        # Get a model satisfying the rules.
        model = s.model()

        # Do something with the model
        print model

        # Prevent the same model from showing up again.
        block = []
        for instance in model:
            if instance.arity() > 0:
                raise z3.Z3Exception("uninterpreted functions are not supported")
            constant = instance()
            if z3.is_array(constant) or constant.sort().kind() == z3.Z3_UNINTERPRETED_SORT:
                raise Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(constant == model[instance])
        inverted_block = z3.Not(z3.And(block))
        s.add(inverted_block)


if __name__ == '__main__':
    main()
