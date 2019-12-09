from fastai.imports import *
from fastai.torch_imports import *
from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *
from fastai.plots import *
import os
import time
import argparse

parser = argparse.ArgumentParser(description="Script to Automate Classification Process")

parser.add_argument("--frame_dir", help="Path to the metadatadir")
parser.add_argument("--save_file", help="Path to the metadatadir")

arguments = parser.parse_args()

NEW_PATH = arguments.frame_dir
save_file = arguments.save_file

torch.cuda.set_device(0)

PATH = "/home/dheerajreddy.p/dheeraj2/"
sz = 224
arch = wrn
# resnet34, wrn, resnext50
bs = 58

label_csv = PATH+'train.csv'
n = len(list(open(label_csv))) - 1 # header is not counted (-1)
val_idxs = get_cv_idxs(n) # random 20% data for validation set

label_df = pd.read_csv(label_csv)
label_df.head()

#label_csv = f'{PATH}train.csv'
n = len(list(open(label_csv))) - 1
val_idxs = get_cv_idxs(n)
tfms = tfms_from_model(arch, sz, aug_tfms=transforms_side_on, max_zoom=1.1)
data = ImageClassifierData.from_csv(PATH, 'train', label_csv, test_name='test', val_idxs=val_idxs, suffix='.jpg',tfms=tfms, bs=bs)

def get_data(sz, bs): # sz: image size, bs: batch size
    tfms = tfms_from_model(arch, sz, aug_tfms=transforms_side_on, max_zoom=1.1)
    data = ImageClassifierData.from_csv(PATH, 'train', label_csv, test_name='test', val_idxs=val_idxs, suffix='.jpg', tfms=tfms, bs=bs)

    return data if sz > 300 else data.resize(340, 'tmp')

data = get_data(sz, bs)

learn = ConvLearner.pretrained(arch, data, precompute=False)

learn.load('wrn')

start_time = time.time()
# NEW_PATH = "/home/shashanks/final-download/21_12_2018/one_frame_per_sec/"
print(NEW_PATH)
predictions = []

for i, filename in enumerate(sorted(os.listdir(NEW_PATH))):
    try:
        if filename != "n_frames":
            trn_tfms, val_tfms = tfms_from_model(arch, sz)
            ds = FilesIndexArrayDataset([filename], np.array([0]), val_tfms, NEW_PATH + "/")
            dl = DataLoader(ds)
            preds = learn.predict_dl(dl)
            predictions.append([filename, np.argmax(preds)])
    except Exception as e:
        print("Error")

    if i % 5000 == 0:
        print(i, filename)

df = pd.DataFrame(predictions)
df.to_csv(save_file, index=False)
print(time.time() - start_time)
