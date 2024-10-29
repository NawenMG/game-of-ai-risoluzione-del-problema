import numpy as np
import tensorflow as tf
from game_of_life import next_generation

def generate_training_data(num_samples=1000, input_shape=(5, 5)): #Numero di campioni da generare
    X = [] #Stato corrente 
    y = [] #Stato successivo
    for _ in range(num_samples):
        current_state = np.random.randint(2, size=input_shape)
        next_state = next_generation(current_state)
        X.append(current_state)
        y.append(next_state)
    return np.array(X), np.array(y)

def train_model():
    X, y = generate_training_data() #Ottiene gli stati correnti e successivi

    model = tf.keras.Sequential([ #Modello sequenziale
        tf.keras.layers.Flatten(input_shape=(5, 5)), #Appiattisce la matrice in un vettore di 25 elementi
        tf.keras.layers.Dense(128, activation='relu'), #128 neuroni e uno stato di attivazione relu
        tf.keras.layers.Dense(25, activation='sigmoid') #25 neuroni e uno stato di attivazione sigmoid
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']) #Compilazione con il modello ottimizzazione adam
    model.fit(X, y, epochs=10, batch_size=32) #Abbiamo utilizzato 10 epoche di caddestramento e un batch di 32 campio
    model.save('game_of_life_model.h5') #salvataggio del modello in un file HDF5 per un uso futuro

    return model


