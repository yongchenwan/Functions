import tensorflow as tf
# from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file
from inspect_checkpoint import print_tensors_in_checkpoint_file
savedir = "/Users/yongchenwan/Downloads/log_big"
print_tensors_in_checkpoint_file(tf.train.latest_checkpoint(savedir), None, True)
