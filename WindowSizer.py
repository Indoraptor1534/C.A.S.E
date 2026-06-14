import pywinctl as pwc 
import time
from Config import AppNames
def ChangeLoc(window,x,y,w,h):
    acwindow=window
    for alias_dict in AppNames:
        firstname = list(alias_dict.keys())[0] 
        
        if firstname == window:
            acwindow = alias_dict[firstname]  
            print(f"Match Found! Alias Map: '{window}' -> '{acwindow}'")
            break

    acwindows = []
    for _ in range(10):  
        raw_windows = pwc.getWindowsWithTitle(acwindow, condition=pwc.Re.CONTAINS, flags=pwc.Re.IGNORECASE)
        acwindows = [w for w in raw_windows if "opening -" not in w.title.lower()]
        if acwindows:
            break
        time.sleep(0.2)
    if acwindows:
        target = None
        for win in acwindows:
            if win.visible and not win.isMinimized:
                target = win
                break
        if not target:
            target=acwindows[0]
        if target.isMinimized:
            target.restore()
        if target.isMaximized:
            target.restore()
            time.sleep(0.1)

        print("window:",target)
        try:
            if target.isMinimized or target.isMaximized:
                target.restore()
            
        # Standard, rapid execution. No middle-of-the-screen jumping.
            target.resizeTo(w, h)
            target.moveTo(x, y)
        
        except Exception as e:
        # If Word or CMD changes handles mid-air, catch it silently without crashing Jarvis
            print(f"⚠️ Handled window state transition: {e}")
    else:
        print("Nope thats the problem")

def GetWindowLoc(window):
    target_title = runNameCheck(window)
    windows = pwc.getWindowsWithTitle(target_title, condition=pwc.Re.CONTAINS, flags=pwc.Re.IGNORECASE)
    if windows:
        target=windows[0]
        x=target.left
        y=target.top
        w=target.width
        h=target.height
        return x,y,w,h


from Config import projects

def UpdateWindowLoc(project,window,x,y,w,h):
 for project_dict in projects:
    if project in project_dict:
        acproject = project_dict[project]
        for i,item in enumerate(acproject):
            if isinstance(item,dict) and window in item:
                current_request=item[window]
                new_loc=f"loc|{x},{y},{w},{h}"
                if "loc|" in current_request:
                    subrequests=current_request.split(';')
                    updated_subrequests=[]
                    for req in subrequests:
                        if req.startswith("loc|"):
                            updated_subrequests.append(new_loc)
                        else:
                            updated_subrequests.append(req)
                    item[window]= ";".join(updated_subrequests)
                else:
                    if current_request:
                        item[window]=f"{current_request};{new_loc}"
                    else:
                        item[window]=new_loc



def UpdateWindowType(Project,Window,Text):
         for project_dict in projects:
            if Project in project_dict:
                acproject = project_dict[Project]
                for i,item in enumerate(acproject):
                    if isinstance(item,dict) and Window in item:
                        current_request=item[Window]
                        new_text=f"type|{Text}"
                        if "type|" in current_request:
                            subrequests=current_request.split(";")
                            updated_subrequests=[]
                            for req in subrequests:
                                if req.startswith("type|"):
                                    updated_subrequests.append(new_text)
                                else:
                                    updated_subrequests.append(req)
                            item[Window]=";".join(updated_subrequests)
                        else:
                            if current_request:
                                item[Window]=f"{current_request};{new_text}"
                            else:
                                item[Window]=new_text



def SaveConfigToFile():
    with open("Config.py", "w", encoding="utf-8") as file:
        file.write(f"AppNames = {repr(AppNames)}\n\n")
        file.write(f"projects = {repr(projects)}\n")
    print("💾 Workspace settings file configuration saved to Config.py successfully.")

def runNameCheck(name):
    if not isinstance(name, str):
        return name
        
    for alias_dict in AppNames:
        if not isinstance(alias_dict, dict):
            continue
        firstname = list(alias_dict.keys())[0] 
        
        if firstname == name:
            print(f"Match Found! Alias Map: '{name}' -> '{alias_dict[firstname]}'")
            return alias_dict[firstname]  
            
    return name 
    




def Collect(project,window):
    command=input("Do you want to Modify Location or Typing thing?(L for Location and T for the type thing): ").lower()
    if command=="l":
        wait=input(f"Open {window} in desired postition and click 'enter'")
        result=GetWindowLoc(window)
        print(result)
        if result:
            x=result[0]
            y=result[1]
            w=result[2]
            h=result[3]
            UpdateWindowLoc(project,window,x,y,w,h)
            SaveConfigToFile()
        else:
            print("Not Found")
    elif command=="t":
        Text=input("Enter what you want it to type:")
        if Text:
            UpdateWindowType(project,window,Text)
            SaveConfigToFile()
        else:
            print("no text found")




def AddAppsorProjects(project,app):

    #Checking if project exists in dict
    for project_dict in projects:
        if project in project_dict:
            acproject=project_dict[project]

            alreadexists=False
            for item in acproject:
                if isinstance(item,dict) and app in item:
                    alreadexists=True
                    print("Exists")
                    break
                if isinstance(item,str) and item==app:
                    alreadexists=True
                    print("Exists")
                    break

            if not alreadexists:
                new_app_dict={app:""}
                acproject.append(new_app_dict)

                SaveConfigToFile()
                print(f"Added App {app} to {project}")
                Collect(project,app)
            else:
                print("Already exists mate")
        else:
            print("SomeBugMateReport")
            return
        



def removeAppsOrProjects(Project,App=None):
    Project=Project.lower()
    if App:
        App=App.lower()
    for project_dict in projects:
        if Project in project_dict:
            if App:
                original_list=project_dict[Project]

                updated_list=[]
                app_found=False

                for item in original_list:
                    if isinstance(item,dict) and App in item:
                        app_found=True
                        continue
                    elif isinstance(item,str) and item==App:
                        app_found=True
                        continue
                    updated_list.append(item)
                if app_found:
                    project_dict[Project]=updated_list
                    SaveConfigToFile()
                    print(f"Successfully deleted {App} from {Project}")
                else:
                    print(f"Failed to find {App} in {Project}")
                return
            else:
                del project_dict[Project]
                SaveConfigToFile()
                print(f"Successfully deleted {Project}")
                return
    print("Could not find")

