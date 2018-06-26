import numpy as np
from hmmlearn import hmm

model = hmm.GaussianHMM(n_components=2)

model.startprob_ = np.array([0.3,0.7])

model.transmat_ = np.array([0.5,0.5])

model.fit([100][2])

model.sample(100)