from flask import Flask, request, jsonify, render_template
import pandas as pd
import json
from google.cloud import pubsub_v1
import os
import sys
from data_cleaning import clean_data
from game_of_life import next_generation
from model import load_trained_model, predict_future_state
from image_video import save_states_as_images, create_video_from_images
import grpc
from concurrent import futures

# Aggiungi il percorso della directory protos al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'protos'))
import game_of_life_pb2
import game_of_life_pb2_grpc

app = Flask(__name__)

# Carica il modello addestrato una sola volta
model = load_trained_model()

# Inizializza il Pub/Sub Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('YOUR_PROJECT_ID', 'YOUR_TOPIC_NAME')  # Modifica con il tuo ID progetto e nome topic

# Funzione per elaborare i dati tramite gRPC
def process_game_of_life_with_grpc(file_content):
    # Crea un canale gRPC
    channel = grpc.insecure_channel('localhost:50051')
    stub = game_of_life_pb2.GameOfLifeServiceStub(channel)

    # Crea una richiesta
    request = game_of_life_pb2.GameOfLifeRequest(file_content=file_content)

    # Invia la richiesta e ottieni la risposta
    response = stub.ProcessGameOfLife(request)
    return response

@app.route('/game_of_AI', methods=['POST'])
def game_of_AI():
    file = request.files['file']
    data = pd.read_csv(file, header=None)  # Supponendo un file CSV; modifica se necessario per un file TXT

    # Pulizia dei dati
    cleaned_data = clean_data(data)

    # Converte in matrice NumPy per la simulazione
    current_state = cleaned_data.values

    # Lista per salvare gli stati delle generazioni
    states = [current_state.copy()]

    # Esegui la simulazione di più generazioni
    generations = 5
    for _ in range(generations):
        current_state = next_generation(current_state)
        states.append(current_state.copy())

    # Salva gli stati come immagini
    save_states_as_images(states)

    # Crea il video dalle immagini salvate
    create_video_from_images()

    # Predizione dello stato futuro utilizzando gRPC
    # Converti il DataFrame pulito in una stringa CSV
    file_content = cleaned_data.to_csv(header=False, index=False)

    # Utilizza gRPC per elaborare il gioco della vita
    grpc_response = process_game_of_life_with_grpc(file_content)

    # Preparazione dei risultati per il JSON di output
    results = {
        'final_state': grpc_response.final_state,
        'predicted_state': grpc_response.predicted_state,
        'video_path': 'game_of_life_simulation.mp4'  # Percorso del video creato
    }

    # Pubblica le tempistiche e altre informazioni su Pub/Sub
    publish_performance_data(current_state, grpc_response)

    return jsonify(results)

def publish_performance_data(final_state, grpc_response):
    # Crea il messaggio da pubblicare
    performance_data = {
        'final_state': final_state.tolist(),
        'predicted_state': grpc_response.predicted_state,
        'message': 'Game of Life execution completed successfully.'
    }
    message_json = json.dumps(performance_data).encode("utf-8")

    # Pubblica il messaggio
    future = publisher.publish(topic_path, message_json)
    print(f'Published message ID: {future.result()}')  # Stampa l'ID del messaggio pubblicato

def serve():
    # Avvia il server gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_of_life_pb2_grpc.add_GameOfLifeServiceServicer_to_server(GameOfLifeService(), server)
    server.add_insecure_port('[::]:50051')  # Porta su cui ascoltare
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    # Avvio del server Flask
    app.run(debug=True)

    # Avvio del server gRPC (se desiderato, può essere eseguito in un thread separato)
    # serve()
