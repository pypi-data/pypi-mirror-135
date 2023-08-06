def wasm_sprintf(p_fmt: int, mem, offset : int) :
    fmt : str = read_str(mem, p_fmt)
    pp_fmt = []
    args = []
    i = 0
    c_offset = offset
    while i < len(fmt) :
        pp_fmt.append(fmt[i])
        if fmt[i] == '%' :
            if fmt[i + 1] == '%' :
                pp_fmt.append(fmt[i])
                i += 2
                continue
            j = i + 1
            while j < len(fmt) and not ('a' <= fmt[j].lower() <= 'z') :
                j += 1
            assert j < len(fmt), "Invalid format"
            f_spec = fmt[i + 1:j]
            if fmt[j].lower() == 'l' :
                j += 1
            assert j < len(fmt), "Invalid format"
            f_type = fmt[j].lower()

            if f_type in "cdxu" :
                args.append(read_i64(mem, c_offset))
            elif f_type in "fe" :
                args.append(read_f64(mem, c_offset))
            elif f_type == "s" :
                address = read_i64(mem, c_offset)
                args.append(read_str(mem, address))
            else :
                raise RuntimeError("Invalid format = " + (f_spec + f_type))
            c_offset += 8

            pp_fmt.append(f_spec)
            pp_fmt.append(f_type)

            i = j + 1
        else :
            i += 1

    # print(f"\nprintf({''.join(pp_fmt)!r}, {repr(args)[1:-1]})")
    return ''.join(pp_fmt) % tuple(args)


def read_str(mem, offset : int) -> str :
    res = bytearray()
    i = 0
    while i < 1024 :
        c = mem[offset + i]
        i += 1
        if c == 0 :
            return bytes(res).decode('utf-8')
        res.append(c)
    raise RuntimeError("Unbound string")


def read_i64(mem, offset : int) -> int :
    val : int = 0
    if mem[offset + 7] >= 128 :
        for i in range(7,-1,-1) :
            val = 256 * val + 255 ^ mem[offset + i]
        val = -val - 1
    else :
        for i in range(7,-1,-1) :
            val = 256 * val + mem[offset + i]
    return val


def read_f64(mem, offset : int) -> float :
    import struct
    buf = bytearray()
    for i in range(8) :
        buf.append(mem[offset + i])

    return struct.unpack('d', bytes(buf))[0]

def read_i32(mem, offset : int) -> int :
    import struct
    buf = bytearray()
    for i in range(4) :
        buf.append(mem[offset + i])
    return struct.unpack('i', bytes(buf))[0]
