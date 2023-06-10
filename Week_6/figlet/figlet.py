from pyfiglet import Figlet
import sys
import random

figlet = Figlet()
fonts = figlet.getFonts()

if (len(sys.argv) == 1):
    figlet.setFont(font=random.choice(fonts))

elif len(sys.argv) == 3 and (sys.argv[1] == "-f" or sys.argv[1] == "--font") and sys.argv[2] in fonts:
    figlet.setFont(font=sys.argv[2])

else:
    sys.exit("Invalid usage")


text = input("Input: ")
print(figlet.renderText(text))


