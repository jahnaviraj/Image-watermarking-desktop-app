"""
IMAGE WATERMARKING APP
"""

##Imports
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageFont, ImageDraw

##Constants
BACKGROUND_COLOR = '#FED6BE'
LABEL_COLOR = '#624464'

##Make tkinter window 
windows = Tk()
windows.title("Image Watermarking App")
windows.config(padx=30, pady=30, bg=BACKGROUND_COLOR)
windows.minsize(height=600, width=870)

##Intial image data 
curr_img = {
    'file': None,
    'wm_img':None
}

##Functions
def file_input():
    file = filedialog.askopenfile()
    curr_img['file'] = file
    if file:
        status.config(text="Got your file!")
        
    
def wm_input():
    file = filedialog.askopenfile()
    curr_img['wm_img'] = file
    if file:
        status.config(text="Got your watermark image!")

def save_img():
    watermark_text = text_input.get(1.0, "end-1c")
    img = watermark_image(watermark_text)
    img.save("watermark-img.jpg")
    if img:
        status.config(text="The file 'watermark-img.jpg' is saved successfully!")

def watermark_image(text):
    file = curr_img['file']
    logo = curr_img['wm_img']
    image = Image.open(file.name)
    if text:
        wm_img = image.copy()
        draw = ImageDraw.Draw(wm_img)
        font = ImageFont.truetype('arial.ttf',18)
        x = image.size[0]/2 - 50
        y = image.size[1]/2
        draw.text((x, y), text, (255,255,255), font=font)
        return wm_img

    elif logo:
        image.convert("RGBA")
        logo = Image.open(logo.name).convert("RGBA")
        logo_resize = logo.resize((round(image.size[0]*.35), round(image.size[1]*.35)))
        logo_mask = logo_resize.convert("RGBA")

        position = (image.size[0] - logo_resize.size[0], image.size[1] - logo_resize.size[1])
        transparent = Image.new("RGBA", image.size, (255,255,255,0))
        transparent.paste(image, (0,0))
        transparent.paste(logo_mask, position, mask=logo_mask) 

        return transparent.convert("RGB")
                    
##Photoimage objects
circle = PhotoImage(file='circle.png').subsample(5, 5)
upload = PhotoImage(file='upload.png').subsample(10, 10)
download = PhotoImage(file='download.png').subsample(26, 26)

##Labels
def make_index_label(text):
    return Label(windows, text=text, font=("Arial", 25), image=circle, height=100, width=100, compound='center', background=BACKGROUND_COLOR)

def make_info_label(text):
    return Label(windows, text=text, padx=30, pady=30, font=("Palatino", 25), background=BACKGROUND_COLOR, foreground=LABEL_COLOR)

one = make_index_label("1").grid(row=1, column=0)
two = make_index_label("2").grid(row=2, column=0)
three = make_index_label("3").grid(row=4, column=0)

label1 = make_info_label("Select image to watermark").grid(row=1, column=1)
label2 = make_info_label("Enter text for watermark:").grid(row=2, column=1)
label3 = make_info_label("Upload image for watermark:").grid(row=4, column=1)

heading = Label(windows, text="IMAGE WATERMARKING APP", padx=30, pady=30, font=("Courier", 40, "underline", "bold"), justify='center', foreground='#D02E77', background=BACKGROUND_COLOR)
heading.grid(row=0, column=0, columnspan=3)
or_label = Label(windows, text="OR", font=("Palatino", 20), background=BACKGROUND_COLOR, foreground=LABEL_COLOR)
or_label.grid(row=3, column=1)
status = Label(windows, text="Save watermarked image:", padx=30, pady=30, font=("Palatino", 20), background=BACKGROUND_COLOR, foreground='#D02E77')
status.grid(row=5, column=1)

##Buttons
Button(windows, image=upload, command=file_input, height=50, width=50, bg=BACKGROUND_COLOR, relief=GROOVE).grid(row=1, column=2)
Button(windows, image=upload, command=wm_input, height=50, width=50, bg=BACKGROUND_COLOR, relief=GROOVE).grid(row=4, column=2)

down_btn = Button(windows, image=download, command=save_img, height=50, width=50, bg=BACKGROUND_COLOR, relief=GROOVE).grid(row=5, column=2)

##Text input
text_input = Text(windows,height=2, width=30)
text_input.grid(row=2, column=2)

##Main loop
windows.mainloop()
