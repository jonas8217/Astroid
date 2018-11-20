import pickle

score = {'name':'','score':0,'stage':0}
scores = []
for i in range(10):
    scores.append(score)
with open('highscore.txt', 'wb') as f:
    pickle.dump(scores, f)

with open('highscore.txt', 'rb') as f:
    scores = pickle.load(f)
    print(scores[0]['name'])