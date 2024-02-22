import keras 
from keras import layers 

# Conduct a model 
class Model(keras.Model):
    def __init__(self):
        super(Model, self).__init__()
        self.dense1 = layers.Dense(20, activation = 'elu', input_shape = (11, ))
        self.dense2 = layers.Dense(20, activation = 'elu')
        self.dense3 = layers.Dense(20, activation = 'elu')
        self.out = layers.Dense(3, activation = 'softmax')  

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        x = self.dense3(x)
        x = self.out(x)
        return x

# model = Model()
# model.compile(loss='mse', optimizer='adam', metrics=['mae'])

# input_data = np.ones((1, 11))  # You need to specify the input as a 2D array
# q_value = model.predict(input_data)
# q_value[0, 1] = 3
# print(q_value)