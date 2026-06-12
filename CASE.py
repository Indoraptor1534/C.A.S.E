import os
import numpy as np
from op import launch_apps,close_apps
from Config import projects

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0,x)
def relu_derivative(x):
    return (x>0).astype(float)

def ContinueWith(text,embeddings,weights1,weights2,weights3,biases1,biases2,biases3):
        text1=text.replace(",","")

        test = np.array(embeddings.transform(text1)).flatten()




        z1= np.dot(weights1, test) + biases1
        a1=relu(z1)
        z2=np.dot(weights2,a1)+biases2
        a2=relu(z2)
        z3=np.dot(weights3,a2)+biases3
        prob=sigmoid(z3)
        print(prob)
        task=["Open","Close"]
        print(f"Result for '{text1}': {task[np.argmax(prob)]}")



        found_projects=[
                name for entry in projects
                for name in entry.keys()
                if name in text1.lower()
            ]
        if(found_projects):
                if task[np.argmax(prob)]=="Open":
                    launch_apps(found_projects[0])
            
        if task[np.argmax(prob)]=="Close":
                    print("close")
                    close_apps(found_projects[0] if found_projects else 0)

