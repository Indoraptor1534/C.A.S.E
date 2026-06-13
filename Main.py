
from txtai.embeddings import Embeddings
import numpy as np
import os
import pandas
import time
import difflib
from Config import projects
from WindowSizer import AddAppsorProjects
from appchecker import CheckApps
os.environ["FOR_DISABLE_CONSOLE_CTRL_HANDLER"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
embeddings = Embeddings(path="local_miniLM_model")

if os.path.exists('model_weight.npz'):
    data=np.load('model_weight.npz',allow_pickle=True)
    weights1,weights2,weights3=data['w1'],data['w2'],data['w3']
    biases1,biases2,biases3=data['b1'],data['b2'],data['b3']
    print("loaded weights and biases")

acProjectForAdd=None
while True:
    ProjectName=input("Enter project name: ").lower()
    if ProjectName=="exit":
        print("Exiting")
        break
    for project_dict in projects:
        if ProjectName in project_dict:
            acProjectForAdd=ProjectName
            break
    if not acProjectForAdd:
        create_new=input(f"Do you want to add a new project named{ProjectName}?(Y/N)").lower()
        if create_new=="y":
            if projects:
                projects[0][ProjectName]= []
            else:
                projects.append({ProjectName: []})
            from WindowSizer import SaveConfigToFile
            SaveConfigToFile()
            print(f"Added a new project {ProjectName}")
            acProjectForAdd=ProjectName
            break
        elif create_new=="n":
            print("Lets try again...")
            continue
        else:
            print("Not a valid command")
            continue
    else:
        break



if acProjectForAdd:
    while True:
        AppName=input("Enter new app's name: ").lower()
        if AppName=="exit":
            print("Exiting")
            break
        AllAppsInComp=CheckApps()
        if AppName in AllAppsInComp:
            AddAppsorProjects(acProjectForAdd,AppName)
            break
        else:
            Matches=difflib.get_close_matches(AppName,AllAppsInComp,n=1,cutoff=0.7)
            if Matches:
                print (f"Perhaps You Meant {Matches[0]}?")
                continue
                    
            else:
                print("No Luck Finding Your Specified App")
                continue


                    

            



run=1 
while run==1:
    try:
        from SpeechRec import Listen
        print("\nReady. Hold [INSERT] to give a command...")
        command_text=Listen()
        print("text receieved")
        print(command_text)
        if command_text:
            if isinstance(command_text,str):
                from CASE import ContinueWith
                ContinueWith(command_text,embeddings,weights1,weights2,weights3,biases1,biases2,biases3)
        if command_text==False:
            run=0
            import sys
            print("\nExiting ")
            sys.exit(0)

        time.sleep(0.05)

    except KeyboardInterrupt:
        print("Yipee")

      