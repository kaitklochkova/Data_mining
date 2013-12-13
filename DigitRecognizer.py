from numpy import savetxt, loadtxt
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from PIL import Image,ImageDraw 
import math


print('Введите название файла полностью с расширением')
nameI = str(raw_input('(оно должно быть на английском языке): '))

image = Image.open(nameI + ".jpg") 
widthI = image.size[0] 
heightI = image.size[1] 	
drawI = ImageDraw.Draw(image)
arrayI = image.load()

for i in range(widthI):
    for j in range(heightI):
        S = (arrayI[i, j][0] + arrayI[i, j][1] + arrayI[i, j][2]) // 3
        drawI.point((i, j), (S, S, S))

for i in range(widthI):
    for j in range(heightI):
        S = arrayI[i, j][0] + arrayI[i, j][1] + arrayI[i, j][2]
        if (S > (((255 + 100) // 2) * 3)):
            S = 255
        else:
            S = 0
        drawI.point((i, j), (S, S, S))

white = 0
black = 0
for i in range(widthI):
    for j in range(heightI):
        if arrayI[i, j][0] == 0:
            black = black + 1
        if arrayI[i, j][0] == 255:
            white = white + 1

if white > black:
    for i in range(widthI):
        for j in range(heightI):
            S = 255 - arrayI[i, j][0]
            drawI.point((i, j), (S, S, S))

image = image.resize((20, 20), Image.NEAREST)
widthI = image.size[0] 
heightI = image.size[1]
arrayI = image.load()


# считаю центр масс
numX = 0
denumX = 0
numY = 0
denumY = 0 
for i in range(widthI):
    for j in range(heightI):
        numX = numX + arrayI[i, j][0] * i
        denumX = denumX + arrayI[i, j][0]
        numY = numY + arrayI[i, j][0] * j
        denumY = denumY + arrayI[i, j][0]

# координаты центра масс
centerX = round(numX / denumX)
centerY = round(numY / denumY)

# мне было лень руками заводить матрицу нулей 28*28,
# так что я беру черный квадратик 28*28 пикселей
# и выгружаю значения пикселей
# в будущем там будет наш результат
image28 = Image.open("28black.jpg")
draw28 = ImageDraw.Draw(image28) # заодно используем это как полотно, чтобы нарисовать результат	
width28 = image28.size[0] 
height28 = image28.size[1]
result = image28.load() 

# идея проста, чтобы изображение 20*20 было в центре 28*28
# надо чтобы верхний левый угол маленького изображение было в точке (4, 4).
# значит, если у нас центр в центре масс,
# надо сместить левый верхний угол настолько же, насколько смещен центр.
startX = 4 - centerX + 10    
startY = 4 - centerY + 10

# "рисуем" поверх чёрного квадрата 28*28 пикселей нашу картинку 20*20
# то есть копируем значения пикселей маленькой картинки в массив result
# с правильными координатами
for i in range(widthI):
    for j in range(heightI):
        result[i + startX, j + startY] = arrayI[i, j]

test = []
    
for j in range(width28):
    for i in range(height28):
        S = (result[i, j][0] + result[i, j][1] + result[i, j][2]) // 3
        test.append(S);

joblib.dump(test, 'test_set.pkl')
test = joblib.load('test_set.pkl')

print('Строю лес')

forest = joblib.load('forest.pkl')

print('Ответ:')
print(int(forest.predict(test)[0]))
