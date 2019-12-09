
# coding: utf-8

# In[10]:


from fastai.imports import *
from fastai.torch_imports import *
from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *
from fastai.plots import *
from sklearn.model_selection import KFold
import os


# In[11]:


torch.cuda.set_device(0)


# In[12]:


PATH = "working_directory"
sz = 224
arch = resnext50
# resnet34, wrn, resnext50
bs = 58


# In[13]:


label_csv = f'{PATH}train.csv'
label_df = pd.read_csv(label_csv)


# In[14]:


def get_data(sz, bs): # sz: image size, bs: batch size
    tfms = tfms_from_model(arch, sz, aug_tfms=transforms_side_on, max_zoom=1.1)
    data = ImageClassifierData.from_csv(PATH, 'train', f'{PATH}train.csv', test_name='test', val_idxs=val_idxs, suffix='.jpg', tfms=tfms, bs=bs)

    return data if sz > 300 else data.resize(340, 'tmp')


# In[ ]:


train_list = []
test_list = []
kf = KFold(n_splits=5, shuffle=True, random_state=42)
for i, (train_index, test_index) in enumerate(kf.split(label_df)):
    val_idxs = test_index
    tfms = tfms_from_model(arch, sz, aug_tfms=transforms_side_on, max_zoom=1.1)
    data = ImageClassifierData.from_csv(PATH, 'train', f'{PATH}train.csv', test_name='test', val_idxs=val_idxs, suffix='.jpg', tfms=tfms, bs=bs)

    data = get_data(sz, bs)

    learn = ConvLearner.pretrained(arch, data, precompute=True)

    learn.fit(1e-2, 4)
    # learning rate, epochs
    learn.precompute=False

    learn.unfreeze()
    lr=np.array([1e-4, 1e-3, 1e-2])
    learn.fit(lr, 3, cycle_len=1)

    learn.save('resnext50' + str(i))

    learn.load('resnext50' + str(i))

    log_preds, y = learn.TTA(is_test=True)
    probs = np.mean(np.exp(log_preds), 0)
    preds = np.argmax(probs, axis=1)

    df = pd.DataFrame(preds)
    df.columns = ["prediction"]
    df.insert(0, 'id', [o[5:-4] for o in data.test_ds.fnames])

    SUBM = os.path.join(PATH, "resnext")
    os.makedirs(SUBM, exist_ok=True)
    df.to_csv(os.path.join(SUBM, "prediction" + str(i) + ".csv"), index=False)
