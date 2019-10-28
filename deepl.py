from load_dataset import ImageDataset
import tensorflow as tf

imd = ImageDataset('icons/')
images = imd.get_image_arrays()
labels = imd.get_image_lables()

layers = [
    tf.keras.layers.Conv2D(filters=16, kernel_size=(3,3), padding="same", activation=tf.nn.relu,
                                                                  input_shape=images.shape[1:]),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
    tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), padding="same", activation=tf.nn.relu),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
    tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), padding="same", activation=tf.nn.relu),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
    tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), padding="same", activation=tf.nn.relu),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
    tf.keras.layers.Conv2D(filters=256, kernel_size=(3,3), padding="same", activation=tf.nn.relu),
    tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=512, activation=tf.nn.relu),
    tf.keras.layers.Dense(units=256, activation=tf.nn.relu),
    tf.keras.layers.Dense(1)
]
model = tf.keras.Sequential(layers)
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mse',metrics=['mae', 'mse'])
model.fit(images, labels, epochs=20, batch_size=20)
model.save_weights('model.tf')

eval_model = tf.keras.Sequential(layers)
eval_model.load_weights('model.tf')

print(eval_model.predict(images[:10]))
print(labels[:10])

