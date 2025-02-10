import os

# Desativar operações customizadas do oneDNN
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

#if using Theano with GPU
#os.environ["KERAS_BACKEND"] = "tensorflow"

import random
import numpy as np
import keras

import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Model
from keras.applications.inception_v3 import InceptionV3
from keras.layers import GlobalAveragePooling2D
from keras.optimizers import Adam

root = 'PetImages'
train_split, val_split = 0.7, 0.15

categories = [os.path.join(root, subfolder) for subfolder in os.listdir(root) if os.path.isdir(os.path.join(root, subfolder))]

print(categories)

# helper function to load image and return it and input vector
def get_image(path):
    try:
        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        return img, x
    except Exception as e:
        print(f"Erro ao carregar a imagem: {path} - {e}")
        return None, None

for category in categories:
    print(f"\nArquivos na categoria {category}:")
    files = os.listdir(category)
    for file in files[:10]:  # Mostra os primeiros 10 arquivos
        print(file)
        img, x = get_image(os.path.join(category, file))
        if img is not None and x is not None:
            print(img)
            print(x)

data = []
for c, category in enumerate(categories):
    images = [os.path.join(dp, f) for dp, dn, filenames 
              in os.walk(category) for f in filenames 
              if os.path.splitext(f)[1].lower() in ['.jpg','.png','.jpeg']]
for img_path in images:
    img, x = get_image(img_path)
    if img is not None and x is not None:  # Apenas adiciona imagens válidas
        data.append({'x': np.array(x[0]), 'y': c})
    else:
        print(f"Imagem inválida ignorada: {img_path}")


# count the number of classes
num_classes = len(categories)

random.shuffle(data)

idx_val = int(train_split * len(data))
idx_test = int((train_split + val_split) * len(data))
train = data[:idx_val]
val = data[idx_val:idx_test]
test = data[idx_test:]

x_train, y_train = np.array([t["x"] for t in train]), [t["y"] for t in train]
x_val, y_val = np.array([t["x"] for t in val]), [t["y"] for t in val]
x_test, y_test = np.array([t["x"] for t in test]), [t["y"] for t in test]
print(y_test)

# normalize data
x_train = x_train.astype('float32') / 255.
x_val = x_val.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

# convert labels to one-hot vectors
y_train = keras.utils.to_categorical(y_train, num_classes)
y_val = keras.utils.to_categorical(y_val, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
print(y_test.shape)

# summary
print("finished loading %d images from %d categories"%(len(data), num_classes))
print("train / validation / test split: %d, %d, %d"%(len(x_train), len(x_val), len(x_test)))
print("training data shape: ", x_train.shape)
print("training labels shape: ", y_train.shape)

# build the network
# model = Sequential()
# print("Input dimensions: ",x_train.shape[1:])

# model.add(Conv2D(32, (3, 3), input_shape=x_train.shape[1:]))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))

# model.add(Conv2D(32, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))

# model.add(Dropout(0.25))

# model.add(Conv2D(32, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))

# model.add(Conv2D(32, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))

# model.add(Dropout(0.25))

# model.add(Flatten())
# model.add(Dense(256))
# model.add(Activation('relu'))

# model.add(Dropout(0.5))

# model.add(Dense(num_classes))
# model.add(Activation('softmax'))


vgg = keras.applications.VGG16(weights='imagenet', include_top=True)
vgg.summary()

# make a reference to VGG's input layer
inp = vgg.input

# make a new softmax layer with num_classes neurons
new_classification_layer = Dense(num_classes, activation='softmax')

# connect our new layer to the second to last layer in VGG, and make a reference to it
out = new_classification_layer(vgg.layers[-2].output)

# create a new network between inp and out
model_new = Model(inp, out)

# make all layers untrainable by freezing weights (except for last layer)
for l, layer in enumerate(model_new.layers[:-1]):
    layer.trainable = False

# ensure the last layer is trainable/not frozen
for l, layer in enumerate(model_new.layers[-1:]):
    layer.trainable = True

model_new.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model_new.summary()

history2 = model_new.fit(x_train, y_train, 
                         batch_size=128, 
                         epochs=10, 
                         validation_data=(x_val, y_val))

fig = plt.figure(figsize=(16,4))
ax = fig.add_subplot(121)
# ax.plot(history.history["val_loss"])  # Remove old model's history plot
ax.plot(history2.history["val_loss"])
ax.set_title("validation loss")
ax.set_xlabel("epochs")

ax2 = fig.add_subplot(122)
# ax2.plot(history.history["val_acc"])  # Remove old model's history plot
ax2.plot(history2.history["val_acc"])
ax2.set_title("validation accuracy")
ax2.set_xlabel("epochs")
ax2.set_ylim(0, 1)

plt.show()

loss, accuracy = model_new.evaluate(x_test, y_test, verbose=0)

print('Test loss:', loss)
print('Test accuracy:', accuracy)

img, x = get_image('PetImages/Cat/6779.jpg')
probabilities = model_new.predict([x])