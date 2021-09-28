
from app.model import Model

m = Model(
        './data/couplet/train/in.txt',
        './data/couplet/train/out.txt',
        './data/couplet/test/in.txt',
        './data/couplet/test/out.txt',
        './data/couplet/vocabs',
        num_units=1024, layers=4, dropout=0.2,
        batch_size=32, learning_rate=0.001,
        output_dir='./models/output_couplet1',
        restore_model=True)

m.train(500000)
