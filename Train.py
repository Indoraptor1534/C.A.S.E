import numpy as np 
import random
import pandas as pd
from txtai.embeddings import Embeddings
embeddings=Embeddings(path="sentence-transformers/all-MiniLM-L6-v2")
def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0,x)
def relu_derivative(x):
    return (x>0).astype(float)

df=pd.read_excel('Train_data.xlsx',header=None)
all_text=df[0].astype(str).tolist()
label=df[[1,2]].values
print(f"Loaded {len(all_text)} phrases and {len(label)} labels.")
print(f"First label check: {label[0]}") # Should look like [1 0]
string=" ".join(all_text).lower()
raw_words=string.split()
cleaned_words=[word.strip(".,!?()\"';:") for word in raw_words]
words=list(set(cleaned_words))
vocab=", ".join(words)



X_train = np.array(embeddings.batchtransform(all_text))
y_train = label
input_size=384
hidden1_size=12
hidden2_size=8
out_size = 2


weights1=np.random.randn(hidden1_size,input_size)*0.1
weights2=np.random.randn(hidden2_size,hidden1_size)*0.1
weights3=np.random.randn(out_size,hidden2_size)*0.1
biases1 = np.zeros(hidden1_size)
biases2 = np.zeros(hidden2_size)
biases3=np.zeros(out_size)
learning_rate=0.1
for epoch in range(1,400):
    combined=list(zip(X_train,y_train))
    random.shuffle(combined)
    for img,target in combined:


        z1=np.dot(weights1,img)+biases1
        a1=relu(z1)
        z2=np.dot(weights2,a1)+biases2
        a2=relu(z2)
        z3=np.dot(weights3,a2)+biases3
        a3=sigmoid(z3)


        error_out = target - a3
        d_out = error_out * (a3 * (1 - a3)) 
        error_hidden2 = np.dot(weights3.T, d_out)
        d_hidden2 = error_hidden2 * (z2 > 0) 
        error_hidden1 = np.dot(weights2.T, d_hidden2)
        d_hidden1 = error_hidden1 * (z1 > 0)


        weights1 += learning_rate * np.outer(d_hidden1, img)
        biases1  += learning_rate * d_hidden1
        weights2 += learning_rate * np.outer(d_hidden2, a1)
        biases2  += learning_rate * d_hidden2
        weights3 += learning_rate * np.outer(d_out, a2)
        biases3  += learning_rate * d_out
    if epoch % 100 == 0:
        print(f"Epoch {epoch} - Error: {np.mean(np.abs(error_out))}")

np.savez('model_weight.npz', w1=weights1, w2=weights2, w3=weights3, b1=biases1, b2=biases2, b3=biases3)

print("Weights saved to model_weights.npz")




    




