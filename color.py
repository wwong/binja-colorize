from binaryninja import *

HL_ANTI_DEBUG  = highlight.HighlightColor(red=0xff, green=0xff, blue=0x00)
HL_ANTI_VM     = highlight.HighlightColor(red=0x00, green=0x00, blue=0xff)
HL_CALL        = highlight.HighlightColor(red=0xc7, green=0xfd, blue=0xff)
HL_PUSH_RET    = highlight.HighlightColor(red=0xff, green=0x00, blue=0xff)
HL_XOR         = highlight.HighlightColor(red=0x00, green=0xa5, blue=0xff)

ANTI_VM_INSTRUCTIONS = set(['sidt', 'sgdt', 'sldt', 'smsw', 'str', 'in',
                            'cpuid', 'rdtsc', 'icebp'])

def run_plugin_globally(bv):
    call_hits = []
    xor_hits = []
    antidebug_hits = []
    antivm_hits = []
    pushret_hits = []
    for function in bv.functions:
        call_hits += colorize_calls(bv, function)
        xor_hits += colorize_xor(bv, function)
        antidebug_hits += colorize_antidebug(bv, function)
        antivm_hits += colorize_antivm(bv, function)
        pushret_hits += colorize_push_ret(bv, function)
    print_results(call_hits, xor_hits, antidebug_hits, antivm_hits,pushret_hits)

def run_plugin_on_function(bv, function):
    call_hits = colorize_calls(bv, function)
    xor_hits = colorize_xor(bv, function)
    antidebug_hits = colorize_antidebug(bv, function)
    antivm_hits = colorize_antivm(bv, function)
    pushret_hits = colorize_push_ret(bv, function)
    print_results(call_hits, xor_hits, antidebug_hits, antivm_hits,pushret_hits)

def print_results(call_hits, xor_hits, antidebug_hits, antivm_hits, pushret_hits):
    print("Number of calls: %d" % len(call_hits))
    print("Number of xor: %d" % len(xor_hits))
    print("Number of push-ret: %d" % len(pushret_hits))

    print("Number of potential Anti-VM instructions: %d" % len(antivm_hits))
    for addr in antivm_hits:
        print("Anti-VM potential at 0x%x" % addr)

    print("Number of potential Anti-Debug instructions: %d" % len(antidebug_hits))
    for addr in antidebug_hits:
        print("Anti-Debug potential at 0x%x" % addr)

def colorize_calls(bv, function):
    hits = []
    for block in function.llil:
        for op in block:
            if op.operation.name == 'LLIL_CALL':
                hits.append(op.address)
                function.set_auto_instr_highlight(op.address, HL_CALL)
    return hits

def colorize_xor(bv, function):
    hits = []
    for block in function.llil:
        for op in block:
            if op.operation.name == 'LLIL_SET_REG' \
            and isinstance(op.operands[1], lowlevelil.LowLevelILInstruction) \
            and op.operands[1].operation.name == 'LLIL_XOR':
                hits.append(op.address)
                function.set_auto_instr_highlight(op.address, HL_XOR)
    return hits

def colorize_push_ret(bv, function):
    hits = []
    prev_op = None
    for block in function.llil:
        for op in block:
            if op.operation.name == 'LLIL_RET' and prev_op == 'LLIL_PUSH':
                hits.append(op.address)
                function.set_auto_instr_highlight(op.address, HL_PUSH_RET)
            prev_op = op.operation.name
    return hits

def colorize_antivm(bv, function):
    hits = []
    for instr, addr in function.instructions:
        if  instr[0].text in ANTI_VM_INSTRUCTIONS:
            hits.append(addr)
            function.set_auto_instr_highlight(addr, HL_ANTI_VM)
    return hits

def colorize_antidebug(bv, function):
    hits = []
    for instr, addr in function.instructions:
        if  instr[0].text == 'int3' or instr[0].text == 'int' and instr[2].text == '0x2d':
            hits.append(addr)
            function.set_auto_instr_highlight(addr, HL_ANTI_DEBUG)
    return hits