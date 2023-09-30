from keras import Sequential
from keras.src.layers import Dense
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense

from .models import Venta

class VentaPredictionView(APIView):

    def get(self, request):
        # Obtener los datos de la solicitud
        products = Venta.objects.values('producto', 'cantidad')
        data = [{'producto': product['producto'], 'cantidad': product['cantidad']} for product in products]

        # Crear un DataFrame a partir de los datos
        df = pd.DataFrame(data)

        # Codificar las etiquetas de producto
        label_encoder = LabelEncoder()
        df['producto_encoded'] = label_encoder.fit_transform(df['producto'])

        # Preparar los datos
        X = df['producto_encoded'].values.reshape(-1, 1)
        y = df['cantidad'].values

        # Normalizar los datos
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)

        # Dividir en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        # Crear el modelo de red neuronal
        model = Sequential([
            Dense(10, activation='relu', input_shape=(1,)),
            Dense(1)  # Capa de salida
        ])

        # Compilar el modelo
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Entrenar el modelo
        model.fit(X_train, y_train, epochs=25, batch_size=32)

        # Predecir con el modelo entrenado
        predictions = model.predict(X_test)

        # Devolver las predicciones
        response_data = {
            'predicciones': predictions.tolist()
        }

        return Response(response_data, status=status.HTTP_200_OK)