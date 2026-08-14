#!/usr/bin/env python3
# deobf.py
# Usage: python3 deobf.py captures/capture-01.txt > captures/capture-01.decoded.lua
import sys, re

def decode_escapes(s):
    # Replace hex \xhh and octal \ddd and unicode \u{hhhh}
    def repl_hex(m):
        try:
            return bytes([int(m.group(1),16)]).decode('utf-8', errors='replace')
        except:
            return m.group(0)
    s = re.sub(r'\\x([0-9A-Fa-f]{2})', repl_hex, s)
    def repl_oct(m):
        try:
            return bytes([int(m.group(1),8)]).decode('utf-8', errors='replace')
        except:
            return m.group(0)
    s = re.sub(r'\\([0-7]{1,3})', repl_oct, s)
    def repl_uni(m):
        try:
            return chr(int(m.group(1),16))
        except:
            return m.group(0)
    s = re.sub(r'\\u\{([0-9A-Fa-f]+)\}', repl_uni, s)
    return s

def main(fn):
    data = open(fn, "rb").read()
    try:
        text = data.decode("utf-8", errors="replace")
    except:
        text = data.decode("latin1", errors="replace")
    def repl_chr(m):
        nums = m.group(1).split(",")
        chars = []
        for n in nums:
            n = n.strip()
            if n.startswith("0x") or n.startswith("0X"):
                val = int(n,16)
            elif n.startswith("0b") or n.startswith("0B"):
                val = int(n,2)
            else:
                try:
                    val = int(n)
                except:
                    val = 0
            chars.append(chr(val % 256))
        return '"' + ''.join(chars).replace('"','\\"') + '"'
    text = re.sub(r'string\.char\s*\(\s*([0-9xXbB,_\s]+)\s*\)', repl_chr, text)
    text = decode_escapes(text)
    text = re.sub(r'0[xX]([0-9A-Fa-f_]+)', lambda m: hex(int(m.group(1).replace("_",""),16)), text)
    text = re.sub(r'0[bB]([01_]+)', lambda m: str(int(m.group(1).replace("_",""),2)), text)
    print(text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: deobf.py capture-file", file=sys.stderr); sys.exit(2)
    main(sys.argv[1])
