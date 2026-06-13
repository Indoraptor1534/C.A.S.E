from AppOpener import open,close
from Config import projects
import pyautogui
import time
import pywinctl as pwc
import psutil

from WindowSizer import runNameCheck

opened_apps=[]
commands=["type","loc"]



def launch_apps(target_project):
    for project_dict in projects:
        if target_project in project_dict:
            apps_to_open=project_dict[target_project]
            sorted_apps = [a for a in apps_to_open if isinstance(a, dict)] + \
                          [a for a in apps_to_open if isinstance(a, str)]
            for appname in sorted_apps:
                if type(appname)==str:
                    appname=runNameCheck(appname)
                    open(appname,match_closest=False)
                    opened_apps.append(appname)
                elif type(appname)==dict:
                    actual_app_name=list(appname.keys())[0]
                    acactual_app_name=runNameCheck(actual_app_name)
                    print(acactual_app_name)
                    open(acactual_app_name,match_closest=False)
                    opened_apps.append(actual_app_name)
                    request=appname[actual_app_name]
                    if ";" not in request:
                        parts=request.split('|')
                        command=parts[0]
                        print("print"+actual_app_name,command)
                        action=parts[1]
                        if(command in commands):
                            if command=="type":
                                time.sleep(0.5)
                                type_in_window(action,acactual_app_name)
                            elif command=="loc":
                                coords=action.split(",")
                                x=int(coords[0])
                                y=int(coords[1])
                                w=int(coords[2])
                                h=int(coords[3])
                                time.sleep(0.5)
                                from WindowSizer import ChangeLoc
                                ChangeLoc(acactual_app_name,x,y,w,h)
                    else:
                        actions=request.split(";")
                        for req in actions:
                            parts=req.split('|')
                            command=parts[0]
                            action=parts[1]
                            print(command)
                            if(command in commands):
                                print(command)
                                if command=="type":
                                    time.sleep(0.5)
                                    type_in_window(action,acactual_app_name)
                                elif command=="loc":
                                    coords=action.split(",")
                                    print("coords ",coords)
                                    x=int(coords[0])
                                    y=int(coords[1])
                                    w=int(coords[2])
                                    h=int(coords[3])
                                    time.sleep(0.5)
                                    from WindowSizer import ChangeLoc
                                    ChangeLoc(acactual_app_name,x,y,w,h)
            time.sleep(2)
    print(opened_apps)
                
                    

def close_apps(target_project):
    if target_project!=0:
        for project_dict in projects:
            if target_project in project_dict:
                apps_to_open=project_dict[target_project]
                for appname in apps_to_open:
                    if type(appname)==str:
                        kill_by_name(appname)
                    elif type(appname)==dict:
                        actual_app_name=list(appname.keys())[0]
                        kill_by_name(actual_app_name)

    else:
        for appname in opened_apps:
            if type(appname)==str:
                kill_by_name(appname)
            elif type(appname)==dict:
                actual_app_name=list(appname.keys())[0]
                kill_by_name(actual_app_name)

        opened_apps.clear()





def kill_by_name(target_name):
    from Config import AppNames
    target_lower=target_name.lower()

    possible_names = {target_lower}
    
    for mapping in AppNames:
        for key, val in mapping.items():
            if key.lower() == target_lower:
                possible_names.add(val.lower())
            elif val.lower() == target_lower:
                possible_names.add(key.lower())
    for proc in psutil.process_iter(['name']):
        try:
            proc_name_lower = proc.info['name'].lower()
            exe_clean = proc_name_lower.replace('.exe', '')
            
            if not exe_clean:
                continue
                
            # Check if ANY of our aliases match the executable, or vice-versa
            match_found = False
            for name in possible_names:
                if name in proc_name_lower or exe_clean in name:
                    match_found = True
                    break
            
            if match_found:
                proc.kill()
                print(f" Force Killed: {proc.info['name']}")
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue






def type_in_window(text, window_name):

    windows = pwc.getWindowsWithTitle(window_name, condition=pwc.Re.CONTAINS, flags=pwc.Re.IGNORECASE)
    
    if not windows:
        print(f"Error: Could not find window containing '{window_name}'")
        return

    win = windows[0]
    

    if win.isMinimized:
        win.restore()
    win.activate()
    
    time.sleep(0.8) 


    active_win = pwc.getActiveWindow()
    if active_win and (win.title in active_win.title or active_win.title in win.title):
        pyautogui.write(text, interval=0.05)
        pyautogui.press('enter')
        print(f"Successfully typed '{text}' into: {active_win.title}")
    else:
        print(f"Safety Abort: Active window is '{active_win.title if active_win else 'None'}', not CMD.")

