import os
import tensorflow_datasets as tfds
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

IMG_SIZE = 160
BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = 1000

def formatExample(pair):
    image, label = pair['image'], pair['label']
    image = tf.cast(image, tf.float32)
    image = (image/127.5) - 1
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    return image, label

builder = tfds.folder_dataset.ImageFolder('images/')
#print(builder.info)
rawTrain = builder.as_dataset(split='train', shuffle_files=True)
rawValid = builder.as_dataset(split='valid', shuffle_files=True)
rawTest = builder.as_dataset(split='test', shuffle_files=True)

#tfds.show_examples(rawTrain, builder.info)

train = rawTrain.map(formatExample)
validation = rawValid.map(formatExample)
test = rawTest.map(formatExample)

trainBatches = train.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
validationBatches = validation.batch(BATCH_SIZE)
testBatches = test.batch(BATCH_SIZE)

for imageBatch, labelBatch in trainBatches.take(1):
    pass

#print(imageBatch.shape)

IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)

baseModel = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE, include_top=False, weights='imagenet')

featureBatch = baseModel(imageBatch)
#print(featureBatch.shape)

baseModel.trainable = False

#baseModel.summary()

globalAverageLayer = tf.keras.layers.GlobalAveragePooling2D()
featureBatchAverage = globalAverageLayer(featureBatch)
#print(featureBatchAverage.shape)

predictionLayer = tf.keras.layers.Dense(1)
predictionBatch = predictionLayer(featureBatchAverage)
#print(predictionBatch.shape)

model = tf.keras.Sequential([
    baseModel,
    globalAverageLayer,
    predictionLayer
])

baseLearningRate = 0.0001
model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=baseLearningRate),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

#model.summary()

initialEpochs = 20
validationSteps = 20
loss0, accuracy0 = model.evaluate(validationBatches, steps = validationSteps)

print(f'initial loss: {loss0}')
print(f'initial accuracy: {accuracy0}')

history = model.fit(trainBatches,
                    epochs=initialEpochs,
                    validation_data=validationBatches)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()

print("Number of layers in the base model: ", len(baseModel.layers))

fineTuneAt = 100

for layer in baseModel.layers[:fineTuneAt]:
  layer.trainable =  False

model.compile(optimizer = tf.keras.optimizers.RMSprop(learning_rate=baseLearningRate/10),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

#model.summary()

fineTuneEpochs = 10
totalEpochs = initialEpochs + fineTuneEpochs

historyFine = model.fit(trainBatches,
                        epochs=totalEpochs,
                        initial_epoch=history.epoch[-1],
                        validation_data=validationBatches)

acc += historyFine.history['accuracy']
val_acc += historyFine.history['val_accuracy']

loss += historyFine.history['loss']
val_loss += historyFine.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.ylim([0.8, 1])
plt.plot([initialEpochs-1,initialEpochs-1],
          plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.ylim([0, 1.0])
plt.plot([initialEpochs-1,initialEpochs-1],
         plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()

for i in range(0):
  test_batches = test.batch(1)
  for image, label in test_batches.take(1):
    pass
  plt.imshow(np.squeeze(image))
  plt.title("No Foot" if model.predict(image) > 0 else "Foot")