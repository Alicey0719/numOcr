import sys
from PIL import Image
import pyocr
import pyocr.builders
import glob
import shutil
import random

def ocr(path):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool")
        sys.exit(1)

    tool = tools[0]

    txt = tool.image_to_string(
        #文字認識対象の画像image.pngを用意する
        Image.open(path),
        lang="eng",
        builder=pyocr.builders.TextBuilder(tesseract_layout=8)
    )
    #print( txt )
    return txt
    
def file_list(path):
    files = glob.glob(path+'/*.png')
    return files
        
path = './data'
afterDir = './bunrui'
print('- Start -')
files = file_list(path)
print('FileCount:',len(files))
## 元ファイルをランダムに抽出する際に利用
#files = random.sample(files, 11000)
notFoundCount = 0

for f in files:
    txt = ocr(f)
    fname = f.split('/')
    fname = fname[len(fname)-1]
    #print(fname)
    try:
        if txt == '':
            shutil.copyfile(f, afterDir +'/sp/'+fname)
        else:
            shutil.copyfile(f, afterDir +"/"+txt+'/'+fname)
    except FileNotFoundError:
        notFoundCount += 1
        shutil.copyfile(f, afterDir +'/other/'+fname)
        print('FileNotFoundError:', afterDir + "/"+txt+'/'+fname)
        
print('FileNotFoundError:', notFoundCount)
print('- Finish -')

