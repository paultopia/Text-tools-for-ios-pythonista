import ui

# comments are usage examples

#def p1(sender):
#    print('hello 1')
#    sender.superview.close()
    
#def p2(sender):
#    print('bye 2')

#def yo(sender):
#    print('yo')

def make_view(mapping): 
    num_buttons = len(mapping)
    spacing = 1 / (num_buttons + 1)
    view = ui.View()
    view.frame=(0, 0, 500, 500)
    view.name = 'Buttonbox'
    view.background_color = 'white'
    view.flex = 'LRTB'
    for idx, item in enumerate(mapping):
        button = ui.Button(title=item[0])
        realindex = idx + 1
        height = realindex * spacing
        #button.border_width = 5
        bsize = 500 / (1 + num_buttons)
        button.bounds = (0, 0, 500, bsize)
        button.tint_color = "black"
        button.font=('<system-bold>', 20)
        if realindex % 2 == 0:
            button.background_color = "azure"
        else:
            button.background_color="lightgoldenrodyellow"
        button.center = (view.width * 0.5, view.height * height)
        button.flex = 'LRTB'
        button.action = item[1]
        view.add_subview(button)
        view.size_to_fit()
    return view

#view = make_view([('hello', p1), ('goodbye', p2), ('yo', yo)])
#view.present('sheet')    
