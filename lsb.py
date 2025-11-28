import sys
import cv2 
import os

import argparse
# Argument 
# - Pas 
# - image 
# - direction 
# - les bits voulus 

print("---------------------------------------------------------------------------")
print(",--.          ,--.             ,--.                  ,--.                  ")
print("|  |    ,---. |  |-.      ,---.|  ,---.  ,---.  ,---.|  |,-. ,---. ,--.--. ")
print("|  |   (  .-' | .-. '    | .--'|  .-.  || .-. :| .--'|     /| .-. :|  .--' ")
print("|  '--..-'  `)| `-' |    \\ `--.|  | |  |\\   --.\\ `--.|  \\  \\\\   --.|  |    ")
print("`-----'`----'  `---'      `---'`--' `--' `----' `---'`--'`--'`----'`--'    ")
print("---------------------------------------------------------------------------")

                                                                           
## Récuperation des options 
parser = argparse.ArgumentParser(description="Script avec une option -p ou --pas")
parser.add_argument("-p", "--pas", type=int, default=1, help="Option pour spécifier un pas")
parser.add_argument("-i","--input", type=str,required=True, help="Image d'entrée")
parser.add_argument("-d","--direction", type=str,default="droite", help="Direction des LDB (droite,bas,diagonale,carre)")
parser.add_argument("-b","--bits", type=str, default="a" , help="LSB des bits voulus (r,g,b,a)")
parser.add_argument("-bf", "--brute-force", action="store_true", help="Mode brute force")
parser.add_argument("-pX","--pixelX", type=int, default=0, help="Position X du pixel de départ")
parser.add_argument("-pY","--pixelY", type=int, default=0, help="Position Y du pixel de départ")
parser.add_argument("-largeur","--largeur", type=int, default=0, help="Largeur du message a extraire (0 = tout)")
parser.add_argument("-hauteur","--hauteur", type=int, default=0, help="Hauteur du message a extraire (0 = tout)")
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
    pX = args.pixelX
    pY = args.pixelY
    largeur = args.largeur
    hauteur = args.hauteur  
    if pX < 0 or pY < 0:
        print("Les coordonnées des pixels doivent être positives.")
        usage()
    if largeur < 0 or hauteur < 0:
        print("La largeur et la hauteur doivent être positives.")
        usage()
    if not file_exists(inputFile):
        print("Votre fichier n'existe pas.")
        usage()
    if not is_image(inputFile):
        print("Votre fichier n'est pas une image")
        usage()
    if args.brute_force:
        extract_lsb_brute_force(inputFile)

    if step < 0 or step > 100:
        usage()
    if direction not in ["droite", "bas", "diagonale","carre"]:
        usage()
    if bits not in ["r","g","b","a"]:
        usage()
    extract_lsb(inputFile,step,direction,bits,pX,pY)
def usage():
    print("-------------------------")
    print("----------Usage----------")
    print("-------------------------")
    print("./lsb.py -i [Image.png] (-p N) (-d droite) (-b a)")
    print("")
    print(" -i    | image name")
    print(" -p    | pas de l'image (si il faut aller de 2 en 2 par exemple)")
    print(" -d    | direction du lsb (droite, bas, diagonale)")
    print(" -b    | choix des bits a utiliser (r-> red,g-> green,b-> blue,a-> all bits)")
    exit()

def decode_binary_strings(s):
    return ''.join(chr(int(s[i*8:i*8+8], 2)) for i in range(len(s) // 8)) # Récupere le dernier bit de l'octet 





def extract_lsb_brute_force(image_path):
    img = cv2.imread(image_path)
    bits = []
    for bit in ["r","g","b","a"]:
        for step in range(1,3,1):
            for direction in ["droite","bas","diagonale"]:
                bits = []
                for j in range(0, img.shape[1], step):
                    if direction == "droite":
                        pixel = img[0, j]
                    elif direction == "bas":
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
                print("\033[31m----------------------------\033[0m")  # Rouge
                print("\033[31m-------Message décodé-------\033[0m")  # Rouge
                print("\033[31m----------------------------\033[0m")  # Rouge
                print(f"Pas = \033[32m{step}\033[0m Direction = \033[32m{direction}\033[0m bit(s) = \033[32m{bit}\033[0m")
                print("Voici le message décodé")
                print(decode_binary_strings(text))  


def extract_lsb(image_path, step, direction, bit, pX, pY):
    img = cv2.imread(image_path)
    bits = []
    height, width = img.shape[0], img.shape[1]
    if largeur == 0:
        max_largeur = width
    else:
        max_largeur = min(pY + largeur, width)
    if hauteur == 0:
        max_hauteur = height
    else:
        max_hauteur = min(pX + hauteur, height)
    if direction == "carre":
        if largeur == 0 or hauteur == 0:
            print("ERREUR : Pour le mode 'carre', vous devez spécifier une largeur et une hauteur non nulles")
            return
        
        for x in range(pX, max_hauteur, step):
            for y in range(pY, max_largeur, step):
                pixel = img[x, y]
                lsb_blue  = pixel[0] & 1
                lsb_green = pixel[1] & 1
                lsb_red   = pixel[2] & 1
                
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
    else:
        for k in range(0, 999999999, step):  # boucle très large car break manuel
            if direction == "droite":
                x = pX
                y = pY + k
                if y >= max_largeur:
                    break
            elif direction == "bas":
                x = pX + k
                y = pY
                if x >= max_hauteur:
                    break
            elif direction == "diagonale":
                x = pX + k
                y = pY + k
                if x >= max_hauteur or y >= max_largeur:
                    break
            else:
                print("Direction inconnue")
                return
            pixel = img[x, y]
            lsb_blue  = pixel[0] & 1
            lsb_green = pixel[1] & 1
            lsb_red   = pixel[2] & 1
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
        print("Voici le message décodé :")
        print(decode_binary_strings(text))



# Lancement 
check_arg()
	