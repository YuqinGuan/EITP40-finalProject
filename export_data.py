from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn import metrics
import numpy as np
import pandas as pd
import scipy.io
from tensorflow import keras as K, nn
import seaborn as sns
from keras.regularizers import l2
import os

first_layer_input_cnt = 145

def append_photo_data(data, data_cnt, type, lines):
    lines.append("const float cnn_" + type + "_data[" + str(data_cnt) + "][" + str(first_layer_input_cnt) + "] = {")
    frames_str = []
    for frame in data:
        frame_values = [str(i) for i in frame]
        frames_str.append("  {" + ", ".join(frame_values) + "}")
    lines.append(",\n".join(frames_str))
    lines.append("};")
    lines.append("")

def append_label_data(data, data_cnt, type, lines):
    lines.append("const int " + type + "_labels[" + str(data_cnt) + "] = {")
    labels_str = [str(i) for i in data]
    lines.append("  " + ", ".join(labels_str))
    lines.append("};")
    lines.append("")

def append_class_data(data, data_cnt, lines):
    lines.append("const char* classes[" + str(data_cnt) + "] = {")
    classes_str = ['"' + str(i) + '"' for i in data]
    lines.append("  " + ", ".join(classes_str))
    lines.append("};")
    lines.append("")

def encode_char(chars,x):
    
    try:
        i=chars.index(x)
        return i
    except ValueError:
        return 99

def main():
    model = K.models.load_model('model')
    x = model.layers[-2].output #remove the output softmax layer shape is 145 in our case
    model = K.Model(inputs = model.input, outputs = x)
    model.summary()
    training_data=np.load("data/training/device/X_train.npy")#104x28x28
    validation_data=np.load("data/training/device/X_val.npy")#26x28x28
    #test_data=[]
    model_training_output=model.predict(training_data)
    model_val_output=model.predict(validation_data)
    
    chars="abcdefghijklmnopqrstuvwxyz"

    training_labels=np.load("data/training/device/y_train.npy") #numbers
    validation_labels=np.load("data/training/device/y_val.npy")
    lines=[]
    classes=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','-']# todo: convert to numberse
    encoded_classes=[encode_char(chars,x) for x in classes]


    
    append_class_data(encoded_classes,len(encoded_classes),lines)# classes
    append_label_data(training_labels,len(training_labels),"train",lines)# training labels   

    append_label_data(validation_labels,len(validation_labels),"validation",lines)# validation labels

    append_photo_data(model_training_output,len(model_training_output),"train",lines)# training features

    append_photo_data(model_val_output,len(model_val_output),"validation",lines)# validation features

    f = open("data"  + ".h", "w")
    f.write("\n".join(lines))
    f.close()

if __name__ == "__main__":
    main()