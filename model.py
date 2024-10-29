import tensorflow as tf
import numpy as np
from train_model import train_model

def load_trained_model():
    # Carica il modello pre-addestrato da file
    return tf.keras.models.load_model('game_of_life_model.h5')

def predict_future_state(model, current_state):
    # Esegui la previsione dello stato futuro
    prediction = model.predict(current_state.reshape(1, 5, 5))  #Forma dell'input
    return prediction.reshape(5, 5)  # Riformatta l'output in una matrice 5x5
