# Chinese_Couplet
* 具体代码分析可参考博客文章：https://jovenchu.cn/2020/07/16/2020-07-16-Chinese-Couplet/#more
* 使用Seq2Seq的模型实现【中文对联/对句/对词】生成功能，输入上联，输出下联。
* 中文对联数据下载：[70万中文对联/对句/对词数据](https://github.com/wb14123/couplet-dataset/releases/download/1.0/couplet.tar.gz)，分为训练集（input/target）、测试集、词表，放入项目data文件夹中，路径参考下文数据处理模块。

## Seq2Seq模型

整体思想：输入一个序列，用一个 RNN （Encoder）编码成一个向量 u，再用另一个 RNN （Decoder）解码成一个序列输出，且输出序列的长度是可变的。其中decoder要遵循【某一时刻的输入时上一时刻的输出】，期望输出向后一位。基于Tensorflow的Seq2Seq模型代码分析参考[全家桶](https://zhuanlan.zhihu.com/p/47929039)。

### 数据处理模块

1. 初始化模型函数，处理数据并传入参数：`couplet.py`————`model.py`——`class Model()`中的初始化函数，总控制训练集和测试集的数据处理，将文本初步转换为以字作为单一维度的向量。

   ```python
   from model import Model
   m = Model(
           './data/couplet/train/in.txt',
           './data/couplet/train/out.txt',
           './data/couplet/test/in.txt',
           './data/couplet/test/out.txt',
           './data/couplet/vocabs',
           num_units=1024, layers=4, dropout=0.2,
           batch_size=32, learning_rate=0.001,
           output_dir='./models/output_couplet',
           restore_model=True)# 此处为True则是加载上一次模型继续训练
   ```
