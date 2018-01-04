import re
from appex import get_text
from clipboard import set

def tab_paras_to_double_lines(s):
    return re.sub("\n\t", "\n\n", s)

def de_leading_trailing(s):
    s1 = re.sub(" \n", "\n", s)
    return re.sub("\n ", "\n", s1)

def fix_unspaced(mobj):
    m = mobj.group(0)
    return m[0] + " " + m[2]

def de_break(s):
    return re.sub("[^\s]\n[^\s]", fix_unspaced, s)

def clean_lines(s):
    return de_break(de_leading_trailing(tab_paras_to_double_lines(s)))

set(clean_lines(get_text()))
print("done!")
