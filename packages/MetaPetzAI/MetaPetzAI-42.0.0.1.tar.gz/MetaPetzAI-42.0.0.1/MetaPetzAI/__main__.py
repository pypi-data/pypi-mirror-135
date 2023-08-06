# __main__.py
from keras.models import Sequential
from keras.layers import Dense
import keras
import pickle
import json

import pandas as pd
def ANN(_something):
    stored = []
    def AI():
        def remove_2_chars(a):
            for i in range(len(a)):
                j = list(a[i])
                k = []
                for p in j:
                    k.append(p)
                l = ""
                j.pop()
                for x in j:
                    l += x
                a[i] = l
            return a
        def generate():
                print("generating...")
                model = Sequential()
                model.add(Dense(units=5, input_dim=2, kernel_initializer='normal', activation='relu'))
                model.add(Dense(units=5, kernel_initializer='normal', activation='tanh'))

                model.add(Dense(1, kernel_initializer='normal'))
                model.compile(loss='mean_squared_error', optimizer='adam')
                return model
        def train(X, Y, model):
            print("generated")
            from sklearn.preprocessing import StandardScaler
            PredictorScaler=StandardScaler()
            TargetVarScaler=StandardScaler()
            PredictorScaler=StandardScaler()
            TargetVarScaler=StandardScaler()
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
            model.fit(X_train, y_train ,batch_size = 20, epochs = 50, verbose=1)
        def main(m, data):
            for da in data:
                f = open("words.txt", "r")
                a = f.read()
                b = []
                k1 = ""
                for i in a:
                    if i == "&":
                        b.append(k1)
                        k1 = ""
                    else:
                        k1 += i
                a = b
                encounterred_words = a
                f.close()
                def train(X, Y, model):
                    print("generated")
                    from sklearn.preprocessing import StandardScaler
                    PredictorScaler=StandardScaler()
                    TargetVarScaler=StandardScaler()
                    PredictorScaler=StandardScaler()
                    TargetVarScaler=StandardScaler()
                    from sklearn.model_selection import train_test_split
                    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
                    model.fit(X_train, y_train ,batch_size = 20, epochs = 1000, verbose=1)
                    return model
                def parseDictArr(da, speakers):
                    x = []
                    y = []
                    z = []
                    for i in da['utterances']:
                        if i["speaker"] == speakers[0]:
                            x.append(i['text'])
                        elif i["speaker"] == speakers[1]:
                            y.append(i['text'])
                        z.append(i["text"])
                    for i in z:
                        a = ""
                        for k in i:
                            for j in k:
                                print(j)
                                if j[0] == " ":
                                    encounterred_words.append(a)
                                    a = ""
                                else:
                                    a += str(j[0])
                        encounterred_words.append(a)
                    return x, y
                x, y = parseDictArr(da, ["JORDAN", "YOU"])
                def parse_sentence(sentence):
                    j = ""
                    words = []
                    for i in sentence:
                        if i == " ":
                            words.append(j)
                            j = ""
                        else:
                            j += i
                    words.append(j)
                    return words
                def convert_to_int(word):
                    for i in range(len(encounterred_words)):
                        if word == encounterred_words[i]:
                            return i
                X = []

                for i in x:
                    a = []
                    for j in parse_sentence(i):
                        a.append(convert_to_int(j))
                    X.append(a)
                Y = []
                for i in y:
                    a = []
                    for j in parse_sentence(i):
                        a.append(convert_to_int(j))
                    Y.append(a)
                for i in range(len(X)):
                    counter = 0
                    _X_ = []
                    k = []
                    for j in X[i]:
                        if counter >= 2:
                            _X_.append(k)
                            counter = 0
                            k = []
                        else:
                            counter += 1
                            k.append(j)
                    counter = 0
                    _Y_ = []
                    k = []
                    for j in Y[i]:
                        if counter >= 2:
                            _Y_.append(k)
                            counter = 0
                            k = []
                        else:
                            counter += 1
                            k.append(j)
                    m = train(_X_, _Y_, m)
            return m
        import requests
        import os
        import numpy as np
        something = _something
        f = open("words.txt", "r")
        a = f.read()
        b = []
        k1 = ""
        for i in a:
            if i == "&":
                b.append(k1)
                k1 = ""
            else:
                k1 += i
        a = b
        encounterred_words = a
        def parse_sentence(sentence):
            j = ""
            words = []
            for i in sentence:
                if i == " ":
                    words.append(j)
                    j = ""
                else:
                    j += i
            words.append(j)
            return words
        for i in parse_sentence(something):
            encounterred_words.append(i)
        f = open("words.txt", "w")
        print(encounterred_words)
        for i in encounterred_words:
            print(i)
            f.write(i + "&")
        f.close()
        def convert_to_int(word):
            for i in range(len(encounterred_words)):
                if word == encounterred_words[i]:
                    return i
        def convert_S(s):
            o = []
            for i in s:
                o.append(convert_to_int(i))
                o.append(convert_to_int(i))
            return o
        def decode(inp):
            o = []
            for i in inp:
                for j in i:
                    o.append(encounterred_words[round(j)])
            return o
        a = parse_sentence(something)
        print(a)
        t1 = convert_S(a)
        counter = 0
        _Y_ = []
        k = []
        print(t1)
        for j in t1:
            if counter >= 2:
                _Y_.append(k)
                counter = 0
                k = []
            else:
                counter += 1
                k.append(j)
        t1 = _Y_
        print(t1)
        m = keras.models.load_model('saved_model')

        t3 = m.predict(t1)
        t2 = t3
        print(t2)
        input("")
        data = [{'utterances': [{
            "speaker": "JORDAN",
            'text': something,

        },
        {
            "speaker": "YOU",
            "text": decode(t2)
        }]}]
        print(t2[0][0])
        something = parse_sentence(something)
        m.save('saved_model')
        stored.append([t2[0][0], something])
        return t2[0][0], something
    class aiCoder:
        def __init__(self):
            f = open("words.txt", "r")
            a = f.read()
            b = []
            k1 = ""
            for i in a:
                if i == "&":
                    b.append(k1)
                    k1 = ""
                else:
                    k1 += i
            a = b
            self.encounterred_words = a
        def decode(self, inp):
            o = []
            for i in inp:
                for j in i:
                    o.append(self.encounterred_words[round(j)])
            return o
    
        def encode(self, word):
            for i in range(len(self.encounterred_words)):
                if word == self.encounterred_words[i]:
                    return i
    
    def train(X, Y, model):
        print("generated")
        from sklearn.preprocessing import StandardScaler
        PredictorScaler=StandardScaler()
        TargetVarScaler=StandardScaler()
        PredictorScaler=StandardScaler()
        TargetVarScaler=StandardScaler()
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
        model.fit(X_train, y_train ,batch_size = 20, epochs = 1000, verbose=1)
        return model
    m2 = keras.models.load_model('extrapolator_store')
    dat = AI()
    Encoder = aiCoder()
    a = []
    for i in stored:
        for j in i[1]:
            print([[i[0]]],[[Encoder.encode(j)]])
            
    
            for k in dat[1]:
                a.append(Encoder.decode(m2.predict([[float(dat[0]), float(Encoder.encode(k))]])))
            m2 = train([[float(i[0]), float(Encoder.encode(j))], [float(i[0]), float(Encoder.encode(j))]],[[float(i[0]), float(Encoder.encode(j))], [float(i[0]), float(Encoder.encode(j))]], m2)
    print(a)
    m2.save('extrapolator_store')
    text = ""
    b = []
    for i in range(0, len(a), 5):
        b.append(a[i][0])
    buf = ""
    for i in b:
        if i != buf:
            text += i + " "
            buf = i
    def main(m, data):
        def do_something(m, data):
            for da in data:
                f = open("words.txt", "r")
                a = f.read()
                b = []
                k1 = ""
                for i in a:
                    if i == "&":
                        b.append(k1)
                        k1 = ""
                    else:
                        k1 += i
                a = b
                encounterred_words = a
                f.close()
                def train(X, Y, model):
                    print("generated")
                    from sklearn.preprocessing import StandardScaler
                    PredictorScaler=StandardScaler()
                    TargetVarScaler=StandardScaler()
                    PredictorScaler=StandardScaler()
                    TargetVarScaler=StandardScaler()
                    from sklearn.model_selection import train_test_split
                    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
                    model.fit(X_train, y_train ,batch_size = 20, epochs = 1000, verbose=1)
                    return model
                def parseDictArr(da, speakers):
                    x = []
                    y = []
                    z = []
                    for i in da['utterances']:
                        if i["speaker"] == speakers[0]:
                            x.append(i['text'])
                        elif i["speaker"] == speakers[1]:
                            y.append(i['text'])
                        z.append(i["text"])
                    for i in z:
                        a = ""
                        for k in i:
                            for j in k:
                                print(j)
                                if j[0] == " ":
                                    encounterred_words.append(a)
                                    a = ""
                                else:
                                    a += str(j[0])
                        encounterred_words.append(a)
                    return x, y
                x, y = parseDictArr(da, ["JORDAN", "YOU"])
                def parse_sentence(sentence):
                    j = ""
                    words = []
                    for i in sentence:
                        if i == " ":
                            words.append(j)
                            j = ""
                        else:
                            j += i
                    words.append(j)
                    return words
                def convert_to_int(word):
                    for i in range(len(encounterred_words)):
                        if word == encounterred_words[i]:
                            return i
                X = []

                for i in x:
                    a = []
                    for j in parse_sentence(i):
                        a.append(convert_to_int(j))
                    X.append(a)
                Y = []
                for i in y:
                    a = []
                    for j in parse_sentence(i):
                        a.append(convert_to_int(j))
                    Y.append(a)
                for i in range(len(X)):
                    while len(X[i]) < len(Y[i]):
                        X[i].append(0)

                    while len(Y[i]) < len(X[i]):
                        Y[i].append(0)
                    counter = 0
                    _X_ = []
                    k = []
                    for j in X[i]:
                        if counter >= 2:
                            _X_.append(k)
                            counter = 0
                            k = []
                        else:
                            counter += 1
                            k.append(j)
                    counter = 0
                    _Y_ = []
                    k = []
                    for j in Y[i]:
                        if counter >= 2:
                            _Y_.append(k)
                            counter = 0
                            k = []
                        else:
                            counter += 1
                            k.append(j)
                            
                    
                    m = train(_X_, _Y_, m)
            return m
        return do_something(m, data)
    data = [{'utterances': [{
        "speaker": "JORDAN",
         'text': dat[1],

    },
    {
        "speaker": "YOU",
        "text": text
    }]}]
    m = keras.models.load_model('saved_model')
    m = main(m, data)
    
    m.save('saved_model')
    return text

