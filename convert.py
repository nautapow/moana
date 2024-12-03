import os, glob
import numpy as np
from PIL import Image
import tifffile

def split_raw(raw_frames, total_frames, tiff):
    n = total_frames//20000
    
    if n == 0:
        tifffile.imsave(tiff,raw_frames)
    else:
        for i in range(n+1):    
            filename = tiff.split('\\')[-1]
            filename = filename[:-5] + str(i) + filename[-4:]
            save_dir = ('\\').join(tiff.split('\\')[:-1])+'\\'+filename
            
            if i == n:
                tifffile.imsave(save_dir,raw_frames)
            else:
                tifffile.imsave(save_dir,raw_frames[:20000])
                raw_frames = raw_frames[20000:]


folder = r'Z:\Users\cwchiang\patch2p'
renames = glob.glob(os.path.join(folder, "*/ChanB_Preview.tif"))
for old_name in renames:
    new_name = old_name+'back'
    os.rename(old_name, new_name)
    
raw_dirs = glob.glob(os.path.join(folder, "*/Image_001_001.raw"))

for raw_dir in raw_dirs:
    tiff = ('\\').join(raw_dir.split('\\')[:-1])+('\\image_00.tif')
    
    if not os.path.isfile(tiff):
        raw_data = np.fromfile(raw_dir, dtype=np.int16)
        total_frames = int(len(raw_data)/(512*512))
        raw_frames = raw_data.reshape((total_frames, 512, 512))
        
        split_raw(raw_frames, total_frames, tiff)
        
        txt = ('\\').join(raw_dir.split('\\')[:-1])+('\\frame.txt')
        with open(txt, "w") as file:
            file.write(str(total_frames))
            file.close
            
        del raw_data
        del raw_frames