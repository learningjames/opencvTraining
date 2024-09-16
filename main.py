import os
import zipfile
import time
from PIL import Image

pos_compressed = 'pos.zip'
neg_conpressed = 'neg.zip'

if __name__ == '__main__':
    print('Extracting...')
    start = time.time()
    print('Stage 0 of 1...')
    with zipfile.ZipFile(pos_compressed, 'r') as pos:
        pos.extractall('pos')
    print('done.')
    print('Stage 1 of 1...')
    with zipfile.ZipFile(neg_conpressed, 'r') as neg:
        neg.extractall('neg')
    print('done.', f'Time used:{time.time() - start} secs')
    print('Writing...')
    start = time.time()
    for file in os.listdir('neg'):
        if file.endswith('.jpg'):
            with open('neg.txt', 'a+') as f:
                f.write(f'neg/{file}\n')
                print(f'neg/{file}')
    for file in os.listdir('pos'):
        if file.endswith('.jpg'):
            width, height = Image.open('pos/' + file).size
            with open('pos.txt', 'a+') as f:
                f.write(f'pos/{file} 1 0 0 {width} {height}\n')
                print(f'pos/{file} 1 0 0 {width} {height}')
    print('done.', f'Time used:{time.time() - start} secs')
    try:
        os.mkdir('data')
    except FileExistsError:
        pass
    print(f'''opencv3\\opencv\\build\\x64\\vc15\\bin\\opencv_createsamples.exe -info pos.txt -num {len(os.listdir())} -w {width} -h {height} -vec pos.vec''')
    print(f'''opencv3\\opencv\\build\\x64\\vc15\\bin\\opencv_traincascade.exe -data data -vec pos.vec -bg neg.txt -numPos {len(os.listdir('pos'))} -numNeg {len(os.listdir('neg'))} -numStages 10 -w {width} -h {height}''')
