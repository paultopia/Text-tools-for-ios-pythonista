from buttonbox import make_view
from appex import get_text
from clipboard import set

incoming = get_text()

def to_lower(button):
    set(incoming.lower())
    button.superview.close()
    
def to_upper(button):
    set(incoming.upper())
    button.superview.close()

def titlemaker(word):
    if word.lower() in ["and", "but", "not"]:
        return word.lower()
    if len(word) > 2:
        return word[0].upper() + word[1:].lower()
    if word.lower().strip() == "i":
        return word.upper()
    return word.lower()

def to_title(button):
    words = incoming.split(" ")
    title = " ".join(map(titlemaker, words))
    final = title[0].upper() + title[1:]
    set(final)
    button.superview.close()

view = make_view([('lowercase', to_lower), ('Title Case', to_title), ("UPPERCASE", to_upper)])
view.present('sheet')
