import json
import os

os.environ["KERAS_BACKEND"] = "torch"

import keras
from keras.src.optimizers import Adam
import numpy as np
from keras import Sequential, Input
from keras.src.layers import Dense, BatchNormalization

def _build_model():
    model = Sequential([
        Input(shape=(10,)),
        Dense(256, activation='relu'),
        BatchNormalization(),

        Dense(128, activation='tanh'),
        BatchNormalization(),

        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model

class Solver:
    def __init__(self):
        self.model = _build_model()
        self.is_trained = False

    def train(self, x, y, batch_size=32, epochs=100):
        try:
            x_train = np.array(x)
            y_train = np.array(y)

            # Обучение модели
            self.model.fit(
                x_train,
                y_train,
                epochs=epochs,
                batch_size=batch_size,
                shuffle=True,
                verbose=1,
            )

        except Exception as e:
            raise Exception(f"Ошибка обучения модели: {e}")

    def test(self, x, y) -> float:
        x_test = np.array(x)
        y_test = np.array(y)

        loss, metrics = self.model.evaluate(x_test, y_test)
        return loss

    def predict(self, features):
        try:
            features = np.array(features).reshape(1, -1)
            return self.model.predict(features, verbose=0)[0][0]
        except Exception as e:
            raise Exception(f"Ошибка предсказания: {e}")

    def save_model(self, path):
        self.model.save(path)

    def load_model(self, path):
        self.model = keras.models.load_model(path)

    def parse_params(self, data: str) -> list:
        d: dict = json.loads(data)

        return [d[k] for k in sorted(list(d.keys()))]