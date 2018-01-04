import re
import clipboard
from appex import get_text
from buttonbox import make_view

text = get_text()

# clean up paragraphs
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
    
# clean up unicode "smart" punctuation that breaks stuff

drek = {'“': '"', '”': '"', "’": "'", "‘": "'", '—': '-', '−': '-', '…': '...', '•': '-', '–':'-'}
def clean_punctuation(t):
  for key in drek.keys():
    t = t.replace(key, drek[key])
  return t

# views

def fix_paragraphs(button):
    clean_paragraphs = clean_lines(text)
    clipboard.set(clean_paragraphs)
    button.superview.close()

def fix_punctuation(button):
    clean_text = clean_punctuation(text)
    clipboard.set(clean_text)
    button.superview.close()

view = make_view([('clean up paragraph breaks', fix_paragraphs), ('dumbify punctuation', fix_punctuation)])
view.present('sheet')
