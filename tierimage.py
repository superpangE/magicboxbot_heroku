import os
def tier(level):
    if(level == "bronze5"):
        res=os.environ['bronze5']
    if(level == "bronze4"):
        res=os.environ['bronze4']
    if(level == "bronze3"):
        res=os.environ['bronze3']
    if(level == "bronze2"):
        res=os.environ['bronze2']
    if(level == "bronze1"):
        res=os.environ['bronze1']

    if(level == "silver5"):
        res=os.environ['silver5']
    if(level == "silver4"):
        res=os.environ['silver4']
    if(level == "silver3"):
        res=os.environ['silver3']
    if(level == "silver2"):
        res=os.environ['silver2']
    if(level == "silver1"):
        res=os.environ['silver1']

    if(level == "gold5"):
        res=os.environ['gold5']
    if(level == "gold4"):
        res=os.environ['gold4']
    if(level == "gold3"):
        res=os.environ['gold3']
    if(level == "gold2"):
        res=os.environ['gold2']
    if(level == "gold1"):
        res=os.environ['gold1']

    if(level == "platinum5"):
        res=os.environ['platinum5']
    if(level == "platinum4"):
        res=os.environ['platinum4']
    if(level == "platinum3"):
        res=os.environ['platinum3']
    if(level == "platinum2"):
        res=os.environ['platinum2']
    if(level == "platinum1"):
        res=os.environ['platinum1']
                                
    if(level == "diamond5"):
        res=os.environ['diamond5']
    if(level == "diamond4"):
        res=os.environ['diamond4']
    if(level == "diamond3"):
        res=os.environ['diamond3']
    if(level == "diamond2"):
        res=os.environ['diamond2']
    if(level == "diamond1"):
        res=os.environ['diamond1']

    if(level == "ruby5"):
        res=os.environ['ruby5']
    if(level == "ruby4"):
        res=os.environ['ruby4']
    if(level == "ruby3"):
        res=os.environ['ruby3']
    if(level == "ruby2"):
        res=os.environ['ruby2']
    if(level == "ruby1"):
        res=os.environ['ruby1']

    return res
