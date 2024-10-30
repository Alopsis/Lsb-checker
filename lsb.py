import sys
import cv2 
import os

import argparse
# Argument 
# - Pas 
# - image 
# - direction 
# - les bits voulus 

## Récuperation des options 
parser = argparse.ArgumentParser(description="Script avec une option -p ou --pas")
parser.add_argument("-p", "--pas", type=int, default=1, help="Option pour spécifier un pas")
parser.add_argument("-i","--input", type=str,required=True, help="Image d'entrée")
parser.add_argument("-d","--direction", type=str,default="droite", help="Direction des LDB (droite,gauche,diagonale)")
parser.add_argument("-b","--bits", type=str, default="a" , help="LSB des bits voulus (r,g,b,a)")

args = parser.parse_args()

# Fonctions 
def file_exists(filepath):
    return os.path.isfile(filepath)

def is_image(fileName):
    extensions_images = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
    return fileName.lower().endswith(extensions_images)

def check_arg():
    step = args.pas
    inputFile = args.input
    direction = args.direction
    bits = args.bits
    if step < 0 or step > 100:
        usage()
    if not file_exists(inputFile):
        usage()
    if not is_image(inputFile):
        usage()
    if direction not in ["droite", "gauche", "diagonale"]:
        usage()
    if bits not in ["r","g","b","a"]:
        print("1")
        usage()
    extract_lsb(inputFile,step,direction,bits)
def usage():
    print("-------------------------")
    print("----------Usage----------")
    print("-------------------------")
    print("./lsb.py -i [Image.png] (-p N) (-d droite) (-b a)")
    print("")
    print(" -i    | image name")
    print(" -p    | pas de l'image (si il faut aller de 2 en 2 par exemple)")
    print(" -d    | direction du lsb (droite, gauche, diagonale)")
    print(" -b    | choix des bits a utiliser (r-> red,g-> green,b-> blue,a-> all bits)")
    exit()

def decode_binary_strings(s):
    return ''.join(chr(int(s[i*8:i*8+8], 2)) for i in range(len(s) // 8))

def extract_lsb(image_path, step, direction,bit):
    img = cv2.imread(image_path)
    bits = []
    for j in range(0, img.shape[1], step):
        if direction == "droite":
            pixel = img[0, j]
        elif direction == "gauche":
            pixel = img[j, 0]
        elif direction == "diagonale":
            if j < min(img.shape[0], img.shape[1]):
                pixel = img[j, j]
            else:
                break
        lsb_blue = pixel[0] & 1
        lsb_green = pixel[1] & 1
        lsb_red = pixel[2] & 1
        if bit == "r":
            bits.append(str(lsb_red))
        elif bit == "g":
            bits.append(str(lsb_green))
        elif bit == "b":
            bits.append(str(lsb_blue))
    
        elif bit == "a":
            bits.append(str(lsb_red))
            bits.append(str(lsb_green))
            bits.append(str(lsb_blue))
            
    text = ''.join(bits)
    print("Voici le message décodé")
    print(decode_binary_strings(text))  


# Lancement 
check_arg()
	