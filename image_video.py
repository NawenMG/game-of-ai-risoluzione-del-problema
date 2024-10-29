import numpy as np
import matplotlib.pyplot as plt
import os #Per interagire con il sistema operativo, per esempio per salvare dei file
import cv2 #Per la creazione della clip

def save_states_as_images(states, output_folder='frames'):
    """
    Salva ogni stato della simulazione come immagine.
    
    Args:
        states (list): Una lista di matrici 2D che rappresentano gli stati.
        output_folder (str): Cartella in cui salvare le immagini.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, state in enumerate(states):
        plt.figure(figsize=(6, 6))
        plt.imshow(state, cmap='binary', interpolation='nearest')
        plt.title(f'Game of Life - Generation {i}')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.colorbar(ticks=[0, 1], label='Cell State')
        plt.clim(-0.5, 1.5)
        plt.savefig(f'{output_folder}/generation_{i}.png')
        plt.close()

def create_video_from_images(output_folder='frames', video_name='game_of_life_simulation.mp4'):
    """
    Crea un video dalle immagini salvate nella cartella specificata.
    
    Args:
        output_folder (str): Cartella da cui leggere le immagini.
        video_name (str): Nome del video da creare.
    """
    images = [img for img in os.listdir(output_folder) if img.endswith(".png")]
    images.sort()  # Assicurati che le immagini siano nell'ordine corretto

    # Ottieni dimensioni dell'immagine
    first_image = cv2.imread(os.path.join(output_folder, images[0]))
    height, width, layers = first_image.shape

    # Crea un oggetto video writer
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

    for image in images:
        img_path = os.path.join(output_folder, image)
        video.write(cv2.imread(img_path))

    cv2.destroyAllWindows()
    video.release()
