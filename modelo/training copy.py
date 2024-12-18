import random
import json
import pickle
import keras_tuner
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer,SnowballStemmer #Para pasar las palabras a su forma raíz
from keras.callbacks import EarlyStopping
#Para crear la red neuronal
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import schedules,SGD
import tensorflowjs as tfjs
import re

spanish_stemmer = SnowballStemmer('spanish')
english_stemmer = SnowballStemmer('english')

lemmatizer = WordNetLemmatizer()


with open('./intents.json', 'r') as f:
    intents = json.load(f)

with open('./constractions.json', 'r') as f:
    contractions = json.load(f)

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def expand_contractions(text, contractions_dict):
    pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in contractions_dict.keys()) + r')\b')
    return pattern.sub(lambda match: contractions_dict[match.group()], text)

def stem_word(word, lenguaje):
    if lenguaje == "es":
        return spanish_stemmer.stem(word)
    else:
        return english_stemmer.stem(word)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '¿', '.', ',']

#Clasifica los patrones y las categorías
for intent in intents['intents']:
    for pattern in intent['patterns']:
        #convertir a minúsculas y expandir contracciones
        pattern=expand_contractions(pattern.lower(), contractions)
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Detectar el idioma de las palabras y aplicar el stemmer correspondiente
words = [stem_word(word, "es") if re.search(r'[áéíóúñ]', word) else stem_word(word, "en") for word in words if word not in ignore_letters]
words = sorted(set(words))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

#Pasa la información a unos y ceros según las palabras presentes en cada categoría para hacer el entrenamiento
training = []
output_empty = [0]*len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [stem_word(word.lower(), "spanish") if re.search(r'[áéíóúñ]', word) else stem_word(word.lower(), "english") for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
random.shuffle(training)
print(len(training)) 
train_x=[]
train_y=[]
for i in training:
    train_x.append(i[0])
    train_y.append(i[1])

train_x = np.array(train_x) 
train_y = np.array(train_y)

#Creamos la red neuronal
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), name="inp_layer", activation='relu'))
model.add(Dropout(0.5, name="hidden_layer1"))
model.add(Dense(64, name="hidden_layer2", activation='relu'))
model.add(Dropout(0.5, name="hidden_layer3"))
model.add(Dense(len(train_y[0]), name="output_layer", activation='softmax'))

#Creamos el programa de aprendizaje
lr_schedule = schedules.ExponentialDecay(
    initial_learning_rate=0.001,
    decay_steps=30000,
    decay_rate=0.96,
    staircase=True,
)

#Creamos el optimizador y lo compilamos
sgd = SGD(learning_rate=lr_schedule , momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer = sgd, metrics = ['acc'])

# Definimos el callback de early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=100, restore_best_weights=True)


#Entrenamos el modelo y lo guardamos
model.fit(np.array(train_x), np.array(train_y), epochs=500, batch_size=5, verbose=1,validation_split=0.2, callbacks=[early_stopping])
model.save("chatbot_model.h5")
model.summary()

tfjs.converters.save_keras_model(model, 'model_js')
print("Modelo creado con exito")
