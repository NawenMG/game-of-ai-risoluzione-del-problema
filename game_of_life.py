import numpy as np

def next_generation(current_state):
    rows, cols = current_state.shape
    # Inizializza la nuova generazione come matrice di zeri
    new_state = np.zeros((rows, cols), dtype=int) #Matrice bidimensionale di int

    for row in range(rows): #Ciclo delle righe
        for col in range(cols): #Ciclo delle colonne
            # Calcola il numero di vicini vivi
            alive_neighbors = np.sum(current_state[max(0, row-1):min(row+2, rows), max(0, col-1):min(col+2, cols)]) - current_state[row, col]
            
            # Regole per la cella viva
            if current_state[row, col] == 1:
                if alive_neighbors < 2:
                    new_state[row, col] = 0  # Muore per solitudine
                elif 2 <= alive_neighbors <= 3:
                    new_state[row, col] = 1  # Sopravvive
                elif alive_neighbors > 3:
                    new_state[row, col] = 0  # Muore per sovrappopolazione
            # Regola per la cella morta
            else:
                if alive_neighbors == 3:
                    new_state[row, col] = 1  # Diventa viva per riproduzione

    return new_state
