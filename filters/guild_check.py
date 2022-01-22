from emoji import emojize
def check_g(guild):
    if guild:
        return f'[{emojize(guild)}]'
    else:
        return ''