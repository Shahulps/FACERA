import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import threading
import shutil
import cv2
from subprocess import call
from registerGUI import*
from capture import*
from recognitionleft import*
from recognitionright import*
from tkinter import ttk
from similarity import *
from eculadian_sim import*

'''from facerec import *
from register import *
from dbHandler import *'''

active_page = 0
thread_event = None
left_frame = None
right_frame = None
heading = None
webcam = None
img_label = None
img_read = None
img_list = []
slide_caption = None
slide_control_panel = None
current_slide = -1

root = tk.Tk()
root.geometry("1450x750+150+90")

pages = []
for i in range(4):
    pages.append(tk.Frame(root, bg="#202d42"))
    pages[i].pack(side="top", fill="both", expand=True)
    pages[i].place(x=0, y=0, relwidth=1, relheight=1)
    
def goBack():
    global active_page, thread_event, webcam

    if (active_page==3 and not thread_event.is_set()):
        thread_event.set()
        webcam.release()

    for widget in pages[active_page].winfo_children():
        widget.destroy()

    pages[0].lift()
    active_page = 0


def basicPageSetup1(pageNo):
    global left_frame, right_frame, heading
    
    '''back_img = tk.PhotoImage(file="back.png")
    back_button = tk.Button(pages[pageNo], image=back_img, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack)
    back_button.image = back_img
    back_button.place(x=10, y=10)'''
    
    
    content = tk.Frame(pages[pageNo], bg="#202d42", pady=20)
    content.pack(expand="true", fill="both")

    '''left_frame = tk.Frame(content, bg="#202d42")
    left_frame.grid(row=0, column=0, sticky="nsew")'''
    left_frame = tk.LabelFrame(content, text="Detected Criminals", bg="#202d42", font="Arial 20 bold", bd=4,
                             foreground="#2ea3ef", labelanchor="n")
    left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    right_frame = tk.LabelFrame(content, text="Detected Criminals", bg="#202d42", font="Arial 20 bold", bd=4,
                             foreground="#2ea3ef", labelanchor="n")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    content.grid_columnconfigure(0, weight=1, uniform="group1")
    content.grid_columnconfigure(1, weight=1, uniform="group1")
    content.grid_rowconfigure(0, weight=1)






def basicPageSetup(pageNo):
    global left_frame, right_frame, heading

    back_img = tk.PhotoImage(file="back.png")
    back_button = tk.Button(pages[pageNo], image=back_img, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack,width=25,height=25)
    back_button.image = back_img
    back_button.place(x=8, y=8)

    heading = tk.Label(pages[pageNo], fg="white", bg="#202d42", font="Arial 20 bold", pady=10)
    heading.pack()

    content = tk.Frame(pages[pageNo], bg="#202d42", pady=20)
    content.pack(expand="true", fill="both")

    left_frame = tk.Frame(content, bg="#202d42")
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = tk.LabelFrame(content, text="Detected Criminals", bg="#202d42", font="Arial 20 bold", bd=4,
                             foreground="#2ea3ef", labelanchor="n")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    content.grid_columnconfigure(0, weight=1, uniform="group1")
    content.grid_columnconfigure(1, weight=1, uniform="group1")
    content.grid_rowconfigure(0, weight=1)
    

    
    
def getNewSlide(control):
    global img_list, current_slide

    if(len(img_list) > 1):
        if(control == "prev"):
            current_slide = (current_slide-1) % len(img_list)
        else:
            current_slide = (current_slide+1) % len(img_list)

        img_size = left_frame.winfo_height() - 200
        showImage(img_list[current_slide], img_size)

        slide_caption.configure(text = "Image {} of {}".format(current_slide+1, len(img_list)))






def selectMultiImage(opt_menu, menu_var):
    global img_list, current_slide, slide_caption, slide_control_panel

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path_list = filedialog.askopenfilenames(title="Choose atleast 5 images", filetypes=filetype)

    if(len(path_list) < 3):
        messagebox.showerror("Error", "Choose atleast 3 images.")
    else:
        img_list = []
        current_slide = -1

        # Resetting slide control panel
        if (slide_control_panel != None):
            slide_control_panel.destroy()

        # Creating Image list
        for path in path_list:
            img_list.append(cv2.imread(path))

        # Creating choices for profile pic menu
        menu_var.set("")
        opt_menu['menu'].delete(0, 'end')

        for i in range(len(img_list)):
            ch = "Image " + str(i+1)
            opt_menu['menu'].add_command(label=ch, command= tk._setit(menu_var, ch))
            menu_var.set("Image 1")


        # Creating slideshow of images
        img_size =  left_frame.winfo_height() - 200
        current_slide += 1
        showImage(img_list[current_slide], img_size)

        slide_control_panel = tk.Frame(left_frame, bg="#202d42", pady=20)
        slide_control_panel.pack()

        back_img = tk.PhotoImage(file="previous.png")
        next_img = tk.PhotoImage(file="next.png")

        prev_slide = tk.Button(slide_control_panel, image=back_img, bg="#202d42", bd=0, highlightthickness=0,
                            activebackground="#202d42", command=lambda : getNewSlide("prev"))
        prev_slide.image = back_img
        prev_slide.grid(row=0, column=0, padx=60)

        slide_caption = tk.Label(slide_control_panel, text="Image 1 of {}".format(len(img_list)), fg="#ff9800",
                              bg="#202d42", font="Arial 15 bold")
        slide_caption.grid(row=0, column=1)

        next_slide = tk.Button(slide_control_panel, image=next_img, bg="#202d42", bd=0, highlightthickness=0,
                            activebackground="#202d42", command=lambda : getNewSlide("next"))
        next_slide.image = next_img
        next_slide.grid(row=0, column=2, padx=60)







    
def showImage(filename,label ):
     global img_label, left_frame

     if not os.path.isfile(filename):
            print(f"Error: Image file '{filename}' not found.")
            return
     img = cv2.imread(filename)
     if img is not None:
            img = cv2.resize(img, (700, 540))
     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     img = Image.fromarray(img)
     img = ImageTk.PhotoImage(img)
     
     img_label = tk.Label(left_frame, image=img, bg="#202d42")
     img_label.image = img
     img_label.pack(padx=20)
    
     img_label.configure(image=img)
     img_label.image = img
        
     
        
        
def showImage1(filename1,label1):
     global img_label, left_frame

     

     if not os.path.isfile(filename1):
            print(f"Error: Image file '{filename1}' not found.")
            return
     img = cv2.imread(filename1)
     if img is not None:
            img = cv2.resize(img, (700, 540))
     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     img = Image.fromarray(img)
     img = ImageTk.PhotoImage(img)
     
     img_label = tk.Label(right_frame, image=img, bg="#202d42")
     img_label.image = img
     img_label.pack(padx=20)
    
     img_label.configure(image=img)
     img_label.image = img



def selectImage():
    global left_frame, img_label, img_read
    '''for wid in right_frame.winfo_children():
        wid.destroy()'''

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path = filedialog.askopenfilename(title="Choose a image", filetypes=filetype)

    if(len(path) > 0):
        img_read = cv2.imread(path)

        img_size =  left_frame.winfo_height() - 40
    
    showImage(img_read, img_size)

 


def selectImage1():
    global right_frame,left_frame, img_label, img_read
    ''' for wid in right_frame.winfo_children():
        wid.destroy()'''

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path = filedialog.askopenfilename(title="Choose a image", filetypes=filetype)

    if(len(path) > 0):
        img_read = cv2.imread(path)

        img_size =  right_frame.winfo_height() - 40
    
    showImage1(img_read, img_size,right_frame)
    

def on_configure(event, canvas, win):
    canvas.configure(scrollregion=canvas.bbox('all'))
    canvas.itemconfig(win, width=event.width)


def getPage1():
    global active_page, left_frame, right_frame, heading, img_label
    active_page = 1
    img_label = None
    opt_menu = None
    menu_var = tk.StringVar(root)
    pages[1].lift()

    basicPageSetup(1)
    heading.configure(text="Register faces")
    right_frame.configure(text="Enter Details")

    btn_grid = tk.Frame(left_frame, bg="#202d42")
    btn_grid.pack()

    tk.Button(btn_grid, text="Select Images" , command=lambda: selectMultiImage(opt_menu, menu_var), font="Arial 15 bold", bg="#2196f3",
           fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
           activeforeground="white").grid(row=0, column=10, padx=25, pady=25)
    tk.Button(btn_grid, text="capture Images" , command= capture_image, font="Arial 15 bold", bg="#2196f3",
           fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
           activeforeground="white").grid(row=0, column=0, padx=25, pady=25)


    # Creating Scrollable Frame
    canvas = tk.Canvas(right_frame, bg="#202d42", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand="true", padx=30)
    scrollbar = tk.Scrollbar(right_frame, command=canvas.yview, width=20, troughcolor="#202d42", bd=0,
                          activebackground="#00bcd4", bg="#2196f3", relief="raised")
    scrollbar.pack(side="left", fill="y")

    scroll_frame = tk.Frame(canvas, bg="#202d42", pady=20)
    scroll_win = canvas.create_window((0, 0), window=scroll_frame, anchor='nw')

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda event, canvas=canvas, win=scroll_win: on_configure(event, canvas, win))


    tk.Label(scroll_frame, text="* Required Fields", bg="#202d42", fg="yellow", font="Arial 13 bold").pack()
    # Adding Input Fields
    input_fields = ("id","name","preffered_profile")
    ip_len = len(input_fields)
    required = [1, 1,0]

    entries = []
    for i, field in enumerate(input_fields):
        row = tk.Frame(scroll_frame, bg="#202d42")
        row.pack(side="top", fill="x", pady=15)

        label = tk.Text(row, width=20, height=1, bg="#202d42", fg="#ffffff", font="Arial 13", highlightthickness=0, bd=0)
        label.insert("insert", field)
        label.pack(side="left")

        if(required[i] == 1):
            label.tag_configure("star", foreground="yellow", font="Arial 13 bold")
            label.insert("end", "  *", "star")
        label.configure(state="disabled")

        if(i != ip_len-1):
            ent = tk.Entry(row, font="Arial 13", selectbackground="#90ceff")
            ent.pack(side="right", expand="true", fill="x", padx=10)
            entries.append((field, ent))
        else:
            menu_var.set("Image 1")
            choices = ["Image 1"]
            opt_menu = tk.OptionMenu(row, menu_var, *choices)
            opt_menu.pack(side="right", fill="x", expand="true", padx=10)
            opt_menu.configure(font="Arial 13", bg="#2196f3", fg="white", bd=0, highlightthickness=0, activebackground="#90ceff")
            menu = opt_menu.nametowidget(opt_menu.menuname)
            menu.configure(font="Arial 13", bg="white", activebackground="#90ceff", bd=0)

    tk.Button(scroll_frame, text="Register" ''' command=lambda: register(entries, required, menu_var)''', font="Arial 15 bold",
           bg="#2196f3", fg="white", pady=10, padx=30, bd=0, highlightthickness=0, activebackground="#091428",
           activeforeground="white").pack(pady=25)
    
guidelines_text = """**Guidelines:**

1.  Sorry for inconvinience ,it takes some time for processing.
2.  please dont press any keys before processing
3.  on next window press "C" for capture image.
4.  Maintain a neutral facial expression while capturing images.
5.  Avoid capturing images with sunglasses or hats that obscure your face.
6. PRESS Q FOR EXIT
            thankyou for coperation ,team facera
"""

def show_error_message():
    tk.messagebox.showinfo(title="Guidelines", message=guidelines_text)
    recogri()
    img_naam1="frmeright.jpg"
    image_label = tk.Label(right_frame)
    showImage1(img_naam1, image_label)
    image_label.pack()
    
   

    hide_error_message() # Schedule removal after 4 seconds (4000 milliseconds)

def show_error_message1():
    tk.messagebox.showinfo(title="Guidelines", message=guidelines_text)
    recoglef()
    img_naam="frmeleft.jpg"
    image_label = tk.Label(left_frame)
    showImage(img_naam, image_label)
    image_label.pack()
    
    
    hide_error_message()  #

def hide_error_message():
    messagebox.destroy()  # Remove the message box

image_path1 = "frmeleft.jpg"
image_path2 = "frmeright.jpg"
#image1 = cv2.imread(image_path1) used when eculiadence distance was used
#image2 = cv2.imread(image_path2)
print(f"Image 1 type: {type(image_path1)}")
print(f"Image 2 type: {type(image_path2)}")

def simsim():
    
    score = compare_images_mse(image_path1, image_path2)
    tk.messagebox.showinfo(title="SIMILARITY", message="similarity of the given images was almost {:}%".format(score))
    print(f"MSE between {image_path1} and {image_path2} is {score:}%")



def getPage2():
    global active_page, left_frame, right_frame, img_label, heading
    img_label = None
    active_page = 2
    pages[2].lift()

    basicPageSetup1(2)
    
    back_img = tk.PhotoImage(file="back.png")           #ADD THE BACK BUTTON LIKE THESE IN EACH PAGE FOR EASE
    back_button = tk.Button( image=back_img, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack,width=25,height=28)
    back_button.image = back_img
    back_button.place(x=8, y=8)
    
    sim_button = tk.Button(text="Similarity", font="Arial 15 bold", padx=20, bg="#03b6fc",
         fg="white", pady=1, bd=10, highlightthickness=0, activebackground="#091428",command=simsim, activeforeground="white")
    sim_button.place(x=688 ,y=730)
    
    left_frame.configure(text="FACE1")
    right_frame.configure(text="FACE2")
    
    btn_grid = tk.Frame(left_frame, bg="#202d42")
    btn_grid1 = tk.Frame(right_frame,bg="#202d42")
    btn_grid.pack()
    btn_grid1.pack()
      # Stop the progress bar after processing


   

    '''tk.Button(btn_grid, text="Recognize", font="Arial 15 bold", padx=20, bg="#2196f3",
           fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
           activeforeground="white").grid(row=0, column=1, padx=25, pady=25)
    
    
    tk.Button(btn_grid1, text="Capture Image", font="Arial 15 bold", padx=20, bg="#2196f3",
            fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
            activeforeground="white").grid(row=0, column=1, padx=25, pady=25)

    tk.Button(btn_grid1, text="Recognize", font="Arial 15 bold", padx=20, bg="#2196f3",
           fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
           activeforeground="white").grid(row=0, column=0, padx=25, pady=25)'''
    first_button = tk.Button(btn_grid, text="Recog & Capture",command=show_error_message1, font="Arial 15 bold", padx=20, bg="#2196f3",
         fg="white", pady=10, bd=10, highlightthickness=0, activebackground="#091428",
         activeforeground="white")
    '''second_button = tk.Button(btn_grid, text="Recognize", font="Arial 15 bold", padx=20, bg="#2196f3",
         fg="white", pady=10, bd=10, highlightthickness=0, activebackground="#091428",
         activeforeground="white")'''

    #second_button.pack(side="bottom", padx=25, pady=25)
    first_button.pack(side="bottom", padx=25, pady=25)

    first_button1 = tk.Button(btn_grid1, text=" Recog & Capture ",command=show_error_message, font="Arial 15 bold", padx=20, bg="#2196f3",
         fg="white", pady=10, bd=10, highlightthickness=0, activebackground="#091428",
         activeforeground="white")
    '''second_button1 = tk.Button(btn_grid1, text="Recognize", font="Arial 15 bold", padx=20, bg="#2196f3",
         fg="white", pady=10, bd=10, highlightthickness=0, activebackground="#091428",
         activeforeground="white")'''

    #second_button1.pack(side="bottom", padx=25, pady=25)
    first_button1.pack(side="bottom", padx=25, pady=25)
    




    

    




tk.Label(pages[0], text="Facera", fg="white", bg="#202d42",
      font="Arial 35 bold", pady=30).pack()

logo = tk.PhotoImage(file = "logo.png")
tk.Label(pages[0], image=logo, bg="#202d42").pack()

btn_frame = tk.Frame(pages[0], bg="#202d42", pady=30)
btn_frame.pack()
'''tk.Button(btn_frame, text="Register Criminal", command=getPage1)
tk.Button(btn_frame, text="Detect Criminal", command=getPage2)
tk.Button(btn_frame, text="Video Surveillance", command=getPage3)'''#this was actual button format 

tk.Button(btn_frame, text="RECOG/SIMIL",command=getPage2)
tk.Button(btn_frame, text="CREATE DATA SET",command=getPage1)

for btn in btn_frame.winfo_children():
    btn.configure(font="Arial 20", width=17, bg="#2196f3", fg="white",
        pady=15, bd=0, highlightthickness=0, activebackground="#091428", activeforeground="white")
    btn.pack(pady=30)



pages[0].lift()
root.mainloop()