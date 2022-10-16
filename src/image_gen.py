from PIL import Image
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

img = Image.open("images/test1.jpg")
greyImg = Image.open("images/test1.jpg").convert('L')

# a = np.asarray(img)
# print(type(a))
# print(type(a[0]))

width, height = img.size

GREEN = (77, 149, 70)
YELLOW = (181, 159, 59)
DARK_GRAY = (58, 58, 60)


imgMatrix = []

for x in range(width):
    temp = []
    for y in range(height):
        if greyImg.getpixel((x, y)) < int(255*0.4):
            greyImg.putpixel((x, y), 0)
            temp.append(0)
            img.putpixel((x, y), DARK_GRAY)
        elif greyImg.getpixel((x, y)) >= int(255*0.4) and greyImg.getpixel((x, y)) < int(255*0.6):
            greyImg.putpixel((x, y), 128)
            temp.append(1)
            img.putpixel((x, y), GREEN)
        else:
            greyImg.putpixel((x, y), 255)
            temp.append(2)
            img.putpixel((x, y), YELLOW)
    imgMatrix.append(temp)


img.save("images/newColorImage.jpg")
greyImg.save("images/greyOuputImage.jpg")

print(width, height)

imgMatrix = np.array(imgMatrix)

def coarseImage(matrix, coarseVal):
    width, height = len(matrix), len(matrix[0])
    newWidth, newHeight = width//coarseVal, height//coarseVal

    coarseMatrix = []
    coarseMatplot = np.zeros((newWidth, newHeight))
    for x in range(newWidth):
        tempArray = []
        for y in range(newHeight):
            matrixChunk = imgMatrix[x*coarseVal:(x+1)*coarseVal, y*coarseVal:(y+1)*coarseVal]
            
            colorVal = mostCommonVal(matrixChunk)
            if colorVal == 0:
                tempArray.append(DARK_GRAY)
                coarseMatplot[x][y] = 0
            elif colorVal == 1:
                tempArray.append(GREEN)
                coarseMatplot[x][y] = 1
            else:
                tempArray.append(YELLOW)
                coarseMatplot[x][y] = 2
        coarseMatrix.append(tempArray)

    return coarseMatrix, coarseMatplot
    
def mostCommonVal(matrixChunk):
    flatChunk = matrixChunk.flatten()
    maxCountVal = -1
    for i in range(3):
        if maxCountVal < np.count_nonzero(flatChunk == i):
            maxCountVal = i
    return maxCountVal

def RGBtoColormap(color):
    return (color[0]/235, color[1]/235, color[2]/235)


cmap = matplotlib.colors.ListedColormap([RGBtoColormap(DARK_GRAY), RGBtoColormap(GREEN), RGBtoColormap(YELLOW)])
bounds=[-0.25,0.25,1.25,2]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

coarseN = [[1, 3, 9],
          [27, 64, 81]]

def coarseFig(coarseN, rows, cols, save=False):
    # coarseN = np.zeros((rows, cols))
    
    fig, ax = plt.subplots(nrows=rows, ncols=cols)

    for i in range(2):
        for j in range(3):
            newCoarseImage, newCoarseMatplot = coarseImage(imgMatrix, coarseN[i][j])
            
            newCoarseMatplot = np.flip(np.rot90(newCoarseMatplot, k=3), 1)
            xNum, yNum = len(newCoarseMatplot)//2, len(newCoarseMatplot[0])//2
            ax[i,j].imshow(newCoarseMatplot, cmap= cmap, norm=norm)
            
    plt.savefig(f'images/outputCoarseImage.png')
    plt.show()

coarseFig(coarseN, 2, 3, save=True)



