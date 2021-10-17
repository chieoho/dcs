# -*- coding: utf-8 -*-

def half2full(ustring):
    """把字符串半角转全角"""
    r_string = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符则返回原来的字符
            r_string += uchar
        if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        r_string += unichr(inside_code)
    return r_string
