## **Overview**

These scripts form a simple **chatbot** using **Natural Language Processing (NLP)** and **Machine Learning (ML)** with TensorFlow.

- **`training.py`**: Prepares the training data, builds a neural network model, and trains it.
- **`chatbot.py`**: Loads the trained model and predicts user inputs to generate chatbot responses.

# 1. `training.py`

### **Purpose**

- Reads a JSON file (`intents.json`) containing predefined chatbot responses.
- Prepares data for training by **tokenizing, lemmatizing**, and vectorizing words.
- Trains a **neural network model** using TensorFlow and **saves** the model for later use.

---

### **Key Components**

### **Imports**

```jsx
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers.legacy import SGD

```

- **NLTK**: Used for tokenization and lemmatization (reduces words to their root form).
- **TensorFlow Keras**: Builds a neural network for classifying chatbot responses.
- **Pickle**: Stores preprocessed words and class labels.

1. Data Preprocessing

```jsx
intents = json.loads(open('intents.json').read())
words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

```

- **Reads** the chatbot's intents from `intents.json`.
- Stores:
    - **Words** from chatbot patterns.
    - **Classes** (response categories).
    - **Documents** (word-class pairs).

2. Tokenization and Lemmatization

```jsx
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

```

- **Splits sentences** into words (`nltk.word_tokenize()`).
- **Lemmatizes** words (e.g., "running" → "run").
- **Removes punctuation**.

3. Save Processed Data

```jsx
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

```

Saves `words.pkl` and `classes.pkl` for chatbot usage.

4. Convert Words to Vectors

```jsx
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

```

- Converts words into **binary vectors** for ML training.
- Each **document** is labeled with a class (one-hot encoding).

5. Neural Network Model

```jsx
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

```

- **3-layer neural network**:
    - **Input Layer**: 128 neurons.
    - **Hidden Layer**: 64 neurons.
    - **Output Layer**: `len(train_y[0])` neurons (one for each class).
- Uses **ReLU activation** and **SGD optimizer**.

6. Train and Save the Model

```jsx
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbotmodel.h5', hist)

```

- Trains for **200 epochs**.
- Saves the trained model as **"chatbotmodel.h5"**.

# 2. `chatbot.py`

### **Purpose**

- Loads the trained chatbot model.
- Converts user input into **vectorized format**.
- Predicts a chatbot response using **neural network inference**.

### **Key Components**

### **Imports**

```jsx
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

```

Loads **NLTK**, **Pickle**, and **TensorFlow** to process inputs and predict responses.

## 1. Load Pretrained Data

```jsx
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

```

Loads **preprocessed words**, **classes**, and **trained model**.

## 2. Preprocess User Input

```jsx
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

```

Tokenizes and lemmatizes user input.

3. Convert Input to Bag of Words

```jsx
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

```

Converts the cleaned sentence into a **binary vector**.

4. Predict User Intent

```jsx
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]
    return return_list

```

- Uses the **trained neural network** to predict the user's intent.
- Filters results based on a confidence threshold (`ERROR_THRESHOLD = 0.25`).

### 5. Generate Response

```jsx
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

```

Selects a random **response** from `intents.json` based on the predicted intent.

### 6. Run Chatbot

```jsx
while True:
    message = input("")
    ints = predict_class(message)
    res = get_response(ints, intents)
    print(res)

```

- **Waits for user input**.
- **Predicts the intent** and selects a response.
- **Prints the response**.

## **How It Works**

1. **Train the chatbot (`training.py`)**:
    - Run `python training.py` to train and save the model.
2. **Run the chatbot (`chatbot.py`)**:
    - Run `python chatbot.py` and start typing messages.

---

## **Future Improvements**

✅ **Deploy as an API** (e.g., Flask, FastAPI).

✅ **Use Transformer Models** (like GPT) instead of simple ML.

✅ **Store Conversations** in a database for analytics.

✅ **Add UI** (React, Vue, or a chatbot widget).