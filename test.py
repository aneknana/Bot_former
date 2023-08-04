import bot_former as tlg

def create_actions():
    act1 = tlg.action.Action(name = 'task',
                             task = lambda : 'task')
    act2 = tlg.action.Action(name = 'sum',
                             task = lambda a,  b, c: a + b + c)
    return {'test' : [act1, act2], 'prod' : [act2]}

acts = create_actions()
tlg.infinite_loop(acts, [999999999], False)
