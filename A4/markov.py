import numpy as np
import random
from hmmlearn import hmm



def generate_random_health_injured_sequence(total_states=100):
	sequence=[]
	state = 1
	healthy_matrix = [1,1,1,1,1,1,1,0,0,0]
	unhealthy_matrix = [1,1,1,1,1,0,0,0,0,0]
	random.shuffle(healthy_matrix)
	random.shuffle(unhealthy_matrix)
	#Always start healthy
	sequence.append(state)
	for i in range(total_states-1):
		if state == 1:
			state = np.random.choice(healthy_matrix)
		elif state ==0:
			state = np.random.choice(unhealthy_matrix)
		sequence.append(state)
	return sequence

def generate_random_move_sequence(total_states=100):
	hidden = generate_random_health_injured_sequence(total_states)
	sequence = []
	state=1
	healthy_matrix = [2,2,3,4,4,4,4,4,4,4]
	unhealthy_matrix = [2,2,2,3,3,3,3,3,3,4]
	random.shuffle(healthy_matrix)
	random.shuffle(unhealthy_matrix)
	move = np.random.choice(healthy_matrix)
	sequence.append(move)
	for i in range(total_states-1):
		#skip first one as it has been already appended
		state = hidden[i+1]
		if state == 1:
			move = np.random.choice(healthy_matrix)
		elif state == 0:
			move = np.random.choice(unhealthy_matrix)
		sequence.append(move)
	return hidden,sequence

seq_1 = generate_random_health_injured_sequence(300)
print(seq_1)

hidden, seq_2 = generate_random_move_sequence(300)
print(hidden)
print(seq_2)

#--------------- HMM --------------

model = hmm.MultinomialHMM(n_components=2,n_iter=100)

#The Initial state, as it is assumed that the patient starts healthy
model.startprob_ = np.array([1.0,0.0])

#Represents the change from Healthy to Injured
model.transmat_ = np.array([[0.3,0.7],
							[0.5,0.5]])

#Represents how likely each possible move of
#dribble, pass, or shot is given its condition
#of either healthy or injured
model.emissionprob_ = np.array([[0.2,0.1,0.7],
				  				[0.3,0.6,0.1]])

#model.startprob_ = np.array([0.3,0.7])

X=np.append(seq_1,seq_2)
#print(X.reshape(-1,1))
lengths=[len(seq_1),len(seq_2)]

#model.transmat_ = np.array([[0.5,0.5],[0.5,0.5]])

model.fit(([seq_1]))

print(model.sample(300)[1])

prediction = model.predict(np.array(seq_1).reshape(-1,1))
print(prediction)

print(np.sum(np.array(hidden) == prediction))

#print(model.predict(X.reshape(-1,1),lengths))