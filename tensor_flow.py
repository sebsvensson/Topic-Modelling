import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Tvingar TensorFlow att inte se någon GPU

import tensorflow as tf

# Testa om TensorFlow nu bara använder CPU
print("Antal tillgängliga GPU:er: ", len(tf.config.experimental.list_physical_devices('GPU')))
