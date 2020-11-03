import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

print(sigmoid(5/10))