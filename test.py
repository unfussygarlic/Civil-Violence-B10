import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

print(sigmoid(a))
print(sigmoid(40))