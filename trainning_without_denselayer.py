import os
import numpy as np
import tensorflow as tf
import coding_matrix as cm
import get_batch_data as gbd
import model_without_denselayer as mwd
N_CLASSES=3
IMG_H=19
IMG_W=128
CAPACITY = 1000
MAX_STEP=1000

learning_rate=0.01

PATH = "Cleaned_5sRNA_test/"

row = 19
column = 128
vec_len = 2
temp_batch_size = 16
logs_train_dir="Net_model/"  # 保存训练得来的模型的文件夹
inputs, Labels= gbd.get_Data(PATH=PATH,
                            row=row,
                            column=column)

train_X, train_Y, one_hot_train_Y = gbd.get_batch_data(inputs,Labels, batch_size=temp_batch_size)


train_logits, train_v_length=mwd.interface(inputs=train_X,
                                          Y=one_hot_train_Y,
                                          batch_size=temp_batch_size,
                                          vec_len=vec_len,
                                          temp_batch_size=temp_batch_size)
train_loss=mwd.loss(logits=train_logits,
                   v_length=train_v_length,
                   labels=train_Y,
                   Y=one_hot_train_Y,
                   temp_batch_size=temp_batch_size)
train_op = mwd.trainning(train_loss,learning_rate)
train_acc = mwd.evalution(train_logits,train_Y)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
sess.run(tf.local_variables_initializer())
saver = tf.train.Saver()
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

try:
    for step in np.arange(MAX_STEP):
        if coord.should_stop():
            break
        _, tra_loss, tra_acc = sess.run([train_op, train_loss, train_acc])

        if step % 100 == 0:
            print("Step %d,train loss = %.2f,train accuracy = %.2f" % (step, tra_loss, tra_acc))
            print(train_X.shape)
        if step % 200 == 0:
            # 每两百轮保存一次训练数据
            checkpoint_path = os.path.join(logs_train_dir, 'model.ckpt')
            saver.save(sess,
                       save_path=checkpoint_path,
                       global_step=step)

except tf.errors.OutOfRangeError:
    print('Done Trainning')
finally:
    coord.request_stop()

coord.join(threads)
sess.close()