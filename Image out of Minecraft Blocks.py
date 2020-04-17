import numpy as np
import cv2
import os

big_img_path = 'BigImage.jpg'
resolution = 0.05
small_img_path = 'Minecraft'

def LoadImages():
    global small_img_path
    
    imagelist = list(os.walk(small_img_path))[0][2]
    images = {}
    for im in imagelist:
        img = cv2.imread(small_img_path+'\\'+im)
        r = 0
        g = 0
        b = 0
        count = 0
        for y in img:
            for x in y:
                r += x[0]
                g += x[1]
                b += x[2]
                count += 1
        r /= count
        b /= count
        g /= count
        images[small_img_path+'\\'+im] = [r, g, b]

    return images

def change_resolution(img, resolution):
    res = []
    height = len(img)
    width = len(img[0])
    
    yy = 0
    for y in range(0, height, round(1/resolution)):
        yy += 1
        xx = 0
        res.append([])
        for x in range(0, width, round(1/resolution)):
            res[yy-1].append(img[y][x])
            xx += 1

    return np.array(res)

def ask_block(rgb):
    global images

    record_block = None
    record_value = 99999999999999
    for image in images.items():
        r = abs(rgb[0] - image[1][0])
        g = abs(rgb[1] - image[1][1])
        b = abs(rgb[2] - image[1][2])
        if r+g+b < record_value:
            record_block = image[0]
            record_value = r+g+b

    return record_block

def make_img_out_of_blocks(img):
    count = 0
    total = len(img) * len(img[0])
    rows = []
    yy = 0
    for y in img:
        yy += 1
        xx = 0
        row = []
        for x in y:
            block = ask_block(x)
            block = cv2.imread(block)
            try:
                row = np.concatenate((row, block), axis=1)
            except:
                row = block
            xx += 1
            count += 1
        rows.append(row)
        print(f'{round(count/total*100, 2)}% Completed')
    for row in rows:
        try:
            res = np.concatenate((res, row), axis=0)
        except:
            res = row
            
    return res


print('Loading Images...')
images = LoadImages()
img = cv2.imread(big_img_path)
print('Done')
if resolution != 1:
    print('Changing resolution...')
    img = change_resolution(img, resolution)
    print('Done')
print('Transforming to Blocks...')
img = make_img_out_of_blocks(img)
print('Done')
cv2.imwrite('output.jpg', img)
cv2.imshow('Result', img)
cv2.waitKey(0)

