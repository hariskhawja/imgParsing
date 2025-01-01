from PIL import Image
from typing import List
import os

def imgConv(img : str, fileType="png") -> str:
    """Replaces image with itself of a 
    specified file type, returns the new image
    file path.

    If the argument `fileType` isn't passed in, the default png 
    file type will be used.

    Parameters
    ----------
    img : str
        the file path of the image
    
    fileType : str, optional
        the file type to convert to (default is png)

    Returns
    -------
    str
        new image file path with the appropriate file type

    Raises
    ------
    NotImplementedError
        If image doesn't exist.
        If file type is not supported for images.
    """

    curExt = os.path.splitext(img)[1]

    if not os.path.exists(img): 
        raise NotImplementedError("Image File Path Does Not Exist")
    
    if curExt ==  f".{fileType}": return img

    if f".{fileType}" not in Image.registered_extensions(): 
        raise NotImplementedError("File Type Not Supported")

    newImg = Image.open(img)
    newImg = newImg.convert("RGB")
    newFilePath = os.path.splitext(img)[0] + f".{fileType}"
    newImg.save(newFilePath, fileType.upper())

    os.remove(img)

    return newImg

def parseImage(img : str, saveFolder : str, colour : str, step=1, highlight=(0,0,0), background=(255,255,255)) -> None:
    """Extracts specified colour components of a given image and
    saves the result in the desired folder.

    If the argument `step` isn't passed in, it will be defaulted to 1.
    If the argument `highlight` isn't passed in, it will be defaulted to (0,0,0).
    If the argument `background` isn't passed in, it will be defaulted to (255,255,255).

    Parameters
    ----------
    img : str
        the file path of the image
    
    saveFolder : str
        the save location for the parsed image
    
    colour : str
        the colour to be parsed
    
    step : int, optional
        the degree of pixelation for the parsing (default is 1)

    highlight : (int,int,int), optional
        the colour for the parsed components (default is (0,0,0))
    
    background : (int,int,int), optional
        the colour for the background of the parsed image (default is (255,255,255))

    Raises
    ------
    NotImplementedError
        If image doesn't exist.
        If save location doesn't exist.
        If file type is not a png.
        If inputted colour is not recognised.
        If step value is invalid.
    """
    
    colourDict = {
        'r' : "r >= 120 and r > g and r > b and (r-b) >= 10",
        'g' : "g >= 95 and g > r and g > b and (g-r) >= 10",
        'b' : "b >= 95 and b > g and b > r and (b-r) >= 10"
    }
    
    if not os.path.exists(img): 
        raise NotImplementedError("Image File Path Does Not Exist")
    
    if not os.path.exists(saveFolder):
        raise NotImplementedError("Save Folder Path Does Not Exist")
    
    if os.path.splitext(img)[1] != ".png":
        raise NotImplementedError("Image File Type Not Supported")

    colour = colour[0].lower()

    if colour not in colourDict:
        raise NotImplementedError("Unrecognised Colour")

    if step <= 0:
        raise NotImplementedError("Invalid Step Amount")

    name = os.path.basename(img)

    img = Image.open(img).convert("RGB")
    newImg = img.load()

    width, height = img.size

    for i in range(0, width, step):
        for j in range(0, height, step):

            r, g, b = img.getpixel((i,j))
            conditional = eval(colourDict[colour])

            # Isolate by Specified Colour
            if (conditional): 
                for row in range(step):
                    for col in range(step):
                        newImg[i+row, j+col] = highlight
            
            else: 
                for row in range(step):
                    for col in range(step):
                        newImg[i+row, j+col] = background

    img.save(os.path.join(saveFolder, name))