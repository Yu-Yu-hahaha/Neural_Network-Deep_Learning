# -*- coding: utf-8 -*-
"""ModifiedLanguage.ipynb
Automatically generated by Colaboratory.
"""

import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder

from google.colab import drive
drive.mount('/content/drive')

train_df = pd.read_csv('/content/drive/MyDrive/training.csv')
train_df.head()

type(train_df)

len(train_df)

"""Encode the target variable ('language') from text to number

"""

Y = train_df['language']
#convert Y to number 
#there are 4 languages
le = LabelEncoder()
Y = le.fit_transform(Y)
Y = tf.keras.utils.to_categorical(Y, 4)

Y

"""It is be expected to convert the **train_df["sentence"]**

*  get rid of pucntuations, 
*  convert to lower case
* get rid of the null values

let's call it :   **train_df['sentence_no_punctuation']**

"""

import string
train_df['sentence_no_punctuation'] = train_df["sentence"].str.replace('[^\w\s]', ' ')
train_df['sentence_no_punctuation'] = train_df['sentence_no_punctuation'].str.lower()
train_df['sentence_no_punctuation'] = train_df['sentence_no_punctuation'].dropna()
train_df['sentence_no_punctuation'] = train_df['sentence_no_punctuation'].astype("str")

max_features=5000 #set maximum number of words to 5000
maxlen=400 #set maximum sequence length to 400

tok = tf.keras.preprocessing.text.Tokenizer(num_words=max_features) #again tokenizer step

tok.fit_on_texts(list(train_df['sentence_no_punctuation'])) #fit to cleaned text

print(len(tok.word_index))
vocab_size = len(tok.word_index) + 1 
#this represents the number of words that we tokenize different from max_features but necessary for
#the definition of the dimension of the embedding space

train_df = tok.texts_to_sequences(list(train_df['sentence_no_punctuation'])) #create sequences
train_df = tf.keras.preprocessing.sequence.pad_sequences(train_df, maxlen=maxlen) #let's execute pad step

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_df, Y, test_size=0.2)

embedding_dim = 50 #this is the final dimension of the embedding space.

"""Let's write down the model using embedding layer

Note: you may need Embedding, flatten and Dense layers
"""

from tensorflow import keras
from tensorflow.keras import models, Sequential, layers
from keras.layers import Embedding, Flatten, Dense

model = tf.keras.models.Sequential([
  layers.Embedding(vocab_size, embedding_dim, input_length=maxlen, name = 'embedding'),
  layers.Flatten(),
  layers.Dense(16, 'relu'),
  layers.Dense(4, 'softmax'),
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary() #here to show the architecture

model.fit(np.array(X_train), np.array(y_train), epochs=3) #let's fit the model

"""Remember the train_test_split? now we use the test to evaluate our model"""

model.evaluate(np.array(X_test), np.array(y_test))

"""
Let's evaluate the model"""

from sklearn.metrics import confusion_matrix #import this package from sklearn and output it
predictions = model.predict(X_test) #make predictions
cm = confusion_matrix(predictions.argmax(axis=1), y_test.argmax(axis=1))#generate the confusion matrix

cm

"""Let's try brand new text"""

#these are the codes for each language in order to evaluate properly
print('english', le.transform(['english']))
print('french', le.transform(['french']))
print('italian', le.transform(['italian']))
print('spanish', le.transform(['spanish']))

"""In this experiment we will predict the language of the same sentence in the different languages"""

#new_text = ["tensorflow is a great tool you can find a lot of tutorials from packt"]
#new_text = ["tensorflow est un excellent outil vous pouvez trouver beaucoup de tutoriels de packt"]
#new_text = ["tensorflow è un ottimo strumento puoi trovare molti tutorial di packt"]
new_text = ["tensorflow es una gran herramienta puedes encontrar muchos tutoriales de packt"]

test_text = tok.texts_to_sequences(new_text) #this is how we create sequences
test_text = tf.keras.preprocessing.sequence.pad_sequences(test_text, maxlen=maxlen) #let's execute pad step

np.set_printoptions(suppress=True)
predictions = model.predict(test_text)
print(predictions.argmax())
print(predictions) #spanish you can get confused with italian which makes sense since they are more similar languages

!pip install wikipedia
import wikipedia

"""Let's build a brand new data set with only spanish and let's see if we recognize it ..."""

#language codes
#english: en
#italian: it
#french: fr
#spanish: es
new_wiki_text = []
wikipedia.set_lang('es')
for i in range(0, 5):
    print(i)
    random = wikipedia.random(1)
       
    try:
        new_wiki_text.append([wikipedia.page(random).summary])
    except wikipedia.exceptions.DisambiguationError as e:
        random = wikipedia.random(1)

new_wiki_text = pd.DataFrame(new_wiki_text)
new_wiki_text.columns = ['sentence']
new_wiki_text

new_wiki_text['sentence_lower'] = new_wiki_text["sentence"].str.lower()
new_wiki_text['sentence_no_punctuation'] = new_wiki_text['sentence_lower'].str.replace('[^\w\s]','')
new_wiki_text['sentence_no_punctuation'] = new_wiki_text["sentence_no_punctuation"].fillna("fillna")

np.set_printoptions(suppress=True)
test_wiki_text = tok.texts_to_sequences(list(new_wiki_text['sentence_no_punctuation'] )) #this is how we create sequences
test_wiki_text = tf.keras.preprocessing.sequence.pad_sequences(test_wiki_text, maxlen=maxlen) #let's execute pad step

predictions = model.predict(test_wiki_text)
print(predictions)