from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import Input, Dense, Flatten, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras import optimizers

# ResNet50モデルのロード
ResNet_model = ResNet50(weights='imagenet', include_top=False, input_tensor=Input(shape=(224,224,3)))

# モデルの出力部分の定義
x = Flatten()(ResNet_model.output)
x = Dense(2048, kernel_regularizer='l2', activation='relu')(x)
x = Dropout(0.25)(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.25)(x)
prediction = Dense(8, activation='softmax')(x)

# モデルの定義
model = Model(inputs=ResNet_model.input, outputs=prediction)

# モデルのコンパイル
model.compile(optimizer=optimizers.RMSprop(),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 画像データのジェネレーターの定義
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    width_shift_range=0.2,
    height_shift_range=0.2,
    rotation_range=20,
    horizontal_flip=True,
    fill_mode='constant',
    cval=0
)

# トレーニングデータのジェネレーター
train_generator = train_datagen.flow_from_directory(
    "./train",
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=True
)

# 検証データのジェネレーター
validation_generator = train_datagen.flow_from_directory(
    "./test",
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=True
)

# 早期停止コールバックの定義
early_stopping = EarlyStopping(
    monitor='val_loss',
    min_delta=0.0,
    patience=3
)

# データセットのサイズを取得してsteps_per_epochとvalidation_stepsを設定
steps_per_epoch = train_generator.samples // train_generator.batch_size
validation_steps = validation_generator.samples // validation_generator.batch_size

# モデルのトレーニング
model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=30,
    verbose=1,
    validation_data=validation_generator,
    validation_steps=validation_steps,
    callbacks=[early_stopping]
)

# モデルの保存
model.save('ftmodel.h5')
