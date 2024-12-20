import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD, schedules
#from langdetect import detect
import tensorflow as tf
from keras.callbacks import EarlyStopping
import os
import re

# Inicializar lematizador
lemmatizer = WordNetLemmatizer()

# Cargar intents por idioma
def load_intents_by_language(files, dir_path):
    intents_by_language = {"es": {"intents": []}, "en": {"intents": []}}
    for file in files:
        language = "es" if "es" in file else "en"
        with open(dir_path + os.sep + file, 'r') as f:
            intents = json.load(f)
            intents_by_language[language]["intents"].extend(intents["intents"])
    return intents_by_language

# Expansión de contracciones
def expand_contractions(text, contractions_dict):
    pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in contractions_dict.keys()) + r')\b')
    return pattern.sub(lambda match: contractions_dict[match.group()], text)

# Procesamiento de datos
def preprocess_data(intents, contractions, ignore_letters):
    words, classes, documents = [], [], []
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            pattern = expand_contractions(pattern.lower(), contractions)
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            documents.append((word_list, intent["tag"]))
            if intent["tag"] not in classes:
                classes.append(intent["tag"])
    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
    return sorted(set(words)), sorted(set(classes)), documents

# Crear bolsas de palabras
def create_training_data(words, classes, documents):
    training = []
    output_empty = [0] * len(classes)
    for document in documents:
        bag = []
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in document[0]]
        bag = [1 if word in word_patterns else 0 for word in words]
        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])
    random.shuffle(training)
    train_x = np.array([item[0] for item in training])
    train_y = np.array([item[1] for item in training])
    return train_x, train_y

# Crear modelo
def create_model(input_size, output_size):
    model = Sequential()
    model.add(Dense(128, input_shape=(input_size,), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(output_size, activation='softmax'))
    lr_schedule = schedules.ExponentialDecay(
        initial_learning_rate=0.001,
        decay_steps=30000,
        decay_rate=0.96,
        staircase=True,
    )
    sgd = SGD(learning_rate=lr_schedule, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['acc'])
    return model

# Detectar idioma
def detect_language(input_text):
    try:
        lang = detect(input_text)
        return "es" if lang == "es" else "en"
    except:
        return "en"

# Generar respuesta
def chatbot_response(input_text, models, intents_by_language, words_by_language, classes_by_language):
    language = detect_language(input_text)
    model = models[language]
    words = words_by_language[language]
    classes = classes_by_language[language]
    
    # Crear bolsa de palabras
    bag_of_words = [1 if word in input_text else 0 for word in words]
    result = model.predict(np.array([bag_of_words]))[0]
    tag = classes[np.argmax(result)]
    
    # Buscar respuesta
    for intent in intents_by_language[language]["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

# Configuración
dir_path = './file_intents'
files_list = os.listdir(dir_path)
intents_by_language = load_intents_by_language(files_list, dir_path)

with open('./constractions.json', 'r') as f:
    contractions = json.load(f)

ignore_letters = ['?', '.', '!', ',', ':', ';', '...', '(', ')', '[', ']', '{', '}', '-', '_', '/', '|', '\\', '*', '=', '"', "'", '«', '»']

# Procesar datos por idioma
words_by_language, classes_by_language, documents_by_language = {}, {}, {}
for lang, intents in intents_by_language.items():
    words, classes, documents = preprocess_data(intents, contractions, ignore_letters)
    words_by_language[lang] = words
    classes_by_language[lang] = classes
    documents_by_language[lang] = documents

# Entrenar modelos por idioma
models = {}
for lang in intents_by_language.keys():
    train_x, train_y = create_training_data(words_by_language[lang], classes_by_language[lang], documents_by_language[lang])
    model = create_model(len(train_x[0]), len(train_y[0]))
    # Definimos el callback de early stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
    model.fit(train_x, train_y, epochs=500, batch_size=32, verbose=1, validation_split=0.2, callbacks=[early_stopping])
    model.save(f"chatbot_model_{lang}.h5")
    models[lang] = model

# Guardar datos procesados
for lang in intents_by_language.keys():
    pickle.dump(words_by_language[lang], open(f'words_{lang}.pkl', 'wb'))
    pickle.dump(classes_by_language[lang], open(f'classes_{lang}.pkl', 'wb'))

print("Modelos creados y listos para su uso.")