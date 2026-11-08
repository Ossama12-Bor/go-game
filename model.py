import torch 
import numpy as np 
from Goban import Board  # Ajoute cette importation en haut si ce n'est pas déjà fait

model = torch.nn.Sequential(
    torch.nn.Conv2d(3,16,kernel_size=3,padding=1), 
    torch.nn.BatchNorm2d(16),
    torch.nn.ReLU(),
    torch.nn.Conv2d(16,32,kernel_size=3,padding=1),
    torch.nn.BatchNorm2d(32),
    torch.nn.ReLU(),
    torch.nn.Flatten(),
    torch.nn.Linear(32*8*8,64),
    torch.nn.ReLU(),
    torch.nn.Dropout(0.33),
    torch.nn.Linear(64, 32),
    torch.nn.ReLU(),
    torch.nn.Dropout(0.33),
    torch.nn.Linear(32, 1),
    torch.nn.Sigmoid()
)

model.load_state_dict(torch.load("mon_modele.pth", map_location=torch.device('cpu')))
model.eval()

def name_to_coord(s):
    if s == "PASS" :
        return -1, -1
    indexLetters = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}

    col = indexLetters[s[0]]
    lin = int(s[1:]) - 1
    return col, lin

def array_data(data):
    zeros = np.zeros((8, 8))
    ones = np.ones((8, 8))
    board = np.zeros((3,8,8))
    if len(data)%2 == 0 :
        board[0] = zeros
    else :
        board[0] = ones
    for sample in range(len(data)):
        move = data[sample]
        col, lin = name_to_coord(move)
        if sample%2 == 0 and col != -1:
            board[1, col, lin] = 1
        elif sample%2 == 1 and col != -1:
            board[2, col, lin] = 1
    return board

#b = Board()
#b._historyMoveNames = ["A1", "B2", "C3", "D4", "E5", "F6", "G7", "H8"]  # Exemple de données
#array = array_data(b._historyMoveNames)
#print(array)
#prediction = model(torch.tensor(array, dtype=torch.float32).unsqueeze(0))
#prediction = prediction.detach().numpy().reshape(-1)[0]
#print(prediction)

