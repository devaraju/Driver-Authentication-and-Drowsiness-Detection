import os
from PIL import Image
from datetime import datetime


def getCombinedImage():
    combinedImageName = None
    basePath = os.getcwd()
    filepath = os.path.join(basePath, "test")
    anonymousImagesPath = os.path.join(basePath, "anonymous images")
    
    cnt = 0
    for dirpath, dirnames, filenames in os.walk(filepath):
        if(len(filenames) == 0):
            break

        combinedImage = Image.new('RGB', (640, 480*(len(filenames))))
        for filename in filenames:
            try:
                imagePath = os.path.join(filepath, filename)
                image = Image.open(imagePath)
                combinedImage.paste(image, (0, 480*cnt))
                cnt += 1
            except:
                print("ERROR")
                pass
        combinedImageName = os.path.join(anonymousImagesPath, "anonymous_"+str(datetime.now())+".jpg")
        combinedImage.save(combinedImageName)

    return combinedImageName

if __name__ == "__main__":
    getCombinedImage()