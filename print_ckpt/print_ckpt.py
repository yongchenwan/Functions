import tensorflow as tf
# from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file
from inspect_checkpoint import print_tensors_in_checkpoint_file
savedir = "/Users/yongchenwan/Downloads/log_big"
# print_tensors_in_checkpoint_file(savedir + "linermodel.cpkt", None, True)
# W = tf.Variable(1.0, name="weight")
# b = tf.Variable(2.0, name="bias")
# # 放到一个字典里:
# saver = tf.train.Saver({'weight': b, 'bias': W})
# with tf.Session() as sess:
#     tf.global_variables_initializer().run()
#     saver.save(sess, savedir+"linermodel.cpkt")
# print_tensors_in_checkpoint_file(savedir+"linermodel.cpkt", None, True)
print_tensors_in_checkpoint_file(tf.train.latest_checkpoint(savedir), None, True)