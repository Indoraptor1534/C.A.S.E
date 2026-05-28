
from WindowSizer import GetWindowLoc,UpdateWindowLoc,SaveConfigToFile
while True:
    project=input(">")
    window=input(">")
    result=GetWindowLoc(window)
    print(result)
    if result:
        x=result[0]
        y=result[1]
        w=result[2]
        h=result[3]
        UpdateWindowLoc(project,window,x,y,w,h)
        SaveConfigToFile()