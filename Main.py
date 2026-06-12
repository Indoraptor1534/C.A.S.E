from SpeechRec import Listen
from txtai.embeddings import Embeddings
import numpy as np
import os
import pandas
import time
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
run=1
while run==1:
    try:
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

      