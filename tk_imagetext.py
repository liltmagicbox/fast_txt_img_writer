from shutil import copy
from os import makedirs
from os.path import isfile, exists, split, join

from datetime import datetime
from PIL import ImageTk, ImageGrab
from PIL import Image as Imageload
from PIL.Image import ANTIALIAS

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.title('fastimgnote')
root.geometry('800x700')



#-==-=-==-=-====-==-=-==-=-====-==-=-==-=-====-==-=-==-=-====-==-=-==-=-====
temp_img_path = 'tmpclipimg.png'
default_filename = 'tmp'

savesafe = False
opened_filename = default_filename
def open_txt(e=None , filepath = None):
    global images
    global savesafe
    global opened_filename

    lines = my_text.get(1.0, END)
    if not savesafe:
        if not lines.strip() == '':
            #print('no')
            #https://docs.python.org/ko/3/library/tkinter.messagebox.html
            iwillopen = messagebox.askyesno(title='File Not Saved', message='Open Without Save?' )
            if iwillopen:
                pass
            else:
                return False
    
    if filepath == None:
        text_file_dir = filedialog.askopenfilename(initialdir = get_dir(),title="open txt",filetypes=(("TEXT files", "*.txt"),("all files", "*.*") ))
    else:
        text_file_dir = filepath

    #---so,clear imgs.
    images = []

    if not text_file_dir == "":
        opened_filename = text_file_dir
        text_file = open(text_file_dir, 'r', encoding='utf-8')
        textline = text_file.read()
        text_file.close()
    else:
        opened_filename = default_filename
        textline= ''

    root.title(opened_filename)

    my_text.delete( 1.0, END)
    my_text.insert( END, textline)
    
    replace_image(text_file_dir)
    
    savesafe = True

def replace_image(text_file_dir):
    textline = my_text.get(1.0, END)
    splited_lines = textline.splitlines(True)
    lines_for_write = []
    for i,line in enumerate(splited_lines):
        idx = i+1 
        if line[0] == '[' and line.strip()[-1]==']' and 'png'in line:
            #print(idx, line)
            
            stin = line.index('[')+1
            enin = line.index(']')
            fdir = line[stin:enin]
            pathdir = split(text_file_dir)[0]
            fullfilepath = join(pathdir,fdir)

            #idx_of_img = my_text.index(name)
            lstart, lend = f'{idx}.0 linestart' , f'{idx}.0 lineend'
            my_text.delete(lstart, lend)
            #my_text.insert( lstart, 'ohohohohohohoh')
            add_image(imgpath = fullfilepath, insert = lstart)

        # if idx in idxs:
        #     line = '['+fnames[idxs.index(idx)]+']'+'\n'
        # lines_for_write.append(line)
    #------ replace image to filename.

def save_as(e=None):
    save_txt(saveas = True)
    
def save_txt(e=None, saveas = False):
    global savesafe
    global opened_filename
    filename= opened_filename
    if filename == default_filename or saveas == True:
        filename = make_filename()
        if not filename:
            return 0#not save, discard.
        opened_filename = filename
        root.title(opened_filename)
    
    idxs,fnames = imgnowsave()#for change text.

    #------ replace image to filename. lines_for_write=[]
    textline = my_text.get(1.0, END)
    splited_lines = textline.splitlines(True)    
    lines_for_write = []
    for i,line in enumerate(splited_lines):
        idx = i+1        
        if idx in idxs:
            line = '['+fnames[idxs.index(idx)]+']'+'\n'
        lines_for_write.append(line)
    #------ replace image to filename.

    f = open(filename, 'w' , encoding = 'utf-8')
    fullstring = ''.join(lines_for_write)    
    f.write(fullstring)
    f.close()
    savesafe = True
    
def make_filename(e=None):
    a = datetime.now()
    month = a.month
    day = a.day
    h = str(a.hour).zfill(2)
    m = str(a.minute).zfill(2)
    s = str(a.second).zfill(2)
    tmpname = f'{month}월{day}일_{h}{m}{s}.txt'
    filename = filedialog.asksaveasfilename(initialdir = get_dir(),title="save txt", initialfile = tmpname, filetypes=(("TEXT files", "*.txt"),("all files", "*.*") ))
    if filename == '':
        return False
    if not filename[-3:]=='txt':
        filename = filename+'.txt'
    return filename


#-==-=-==-=-====-==-=-==-=-====-==-=-==-=-====-==-=-==-=-====-==-=-==-=-====
images = []

def add_image(imgpath = None, insert = None):
    font_y_height = 21.25
    global images

    #-------- if gif, just save.
    if 'gif' in imgpath:        
        dest = join(get_dir() , split(imgpath)[1])
        copy(imgpath,dest)
        return False
    
    #---------------image file load
    try:
        image = Imageload.open(imgpath)
        if image.width>720:
            image = image.resize( (720,405), )
        my_image =  ImageTk.PhotoImage(image, ANTIALIAS)
        images.append(my_image)
    except:
        return False#fail to load, if no file exist...
    #---------------image file load
    
    position = my_text.index(INSERT)#where cursor is.
    

    #----for when copied was imgfiledir.
    #my_text.get(position.. too complex.later. what is LINE_END?
    #got it. my_text.get(1.0, '1.0 lineend')

    paste_test = my_text.get(f'{position} linestart' , position)
    if imgpath in paste_test:
        test = position.split('.')[0]+'.'+str(int(position.split('.')[1])-len(imgpath))
        my_text.delete(test , position)
    
    #input('break')    
    #fine. remained for history. replaced just 2 lines!ha.
##    paste_test = my_text.get(f'{position} linestart' , position)
##    if imgpath in paste_test:
##        pathstart = paste_test.index(imgpath)
##        #print(pathstart,position)
##        pathstart = position.split('.')[0]+'.'+str(int(position.split('.')[1])-pathstart)
##        #print(pathstart)
##        my_text.delete(pathstart , position)
##        my_text.insert( position, paste_test.replace(imgpath,'') )
##        my_text.insert( position, '\n')
##        position = my_text.index(INSERT)




    #if was [filename], just add img.
    if not insert == None:#means we know exact line, no need to +\n.
        position = insert
        my_text.image_create(position, image= my_image )
    


    else:#common situation. add \n b/after img.
    
        #or if was plane text , add \n.
        #----for when copied was imgfiledir.
        my_text.insert( position, '\n')
        #position = my_text.index(INSERT)#where cursor is.#+++
        position = str(int(position.split('.')[0])+1)+'.0'
        
        my_text.image_create(position, image= my_image )
        
        #position = my_text.index(INSERT)#where cursor is.#+++
        position = str(int(position.split('.')[0])+1)+'.0'
        my_text.insert( position, '\n')
        #text_scroll.set(0.8,1.0)

        #-to bottom of picture
        my_text.yview_pickplace( my_text.index(INSERT) )
        #---scroll.fine    

def current_line_is_filepath(path):
    position = my_text.index(INSERT)#where cursor is.#+++
    curline = my_text.get(f'{position} linestart', position)
    return path == curline
def current_line_contains_filepath(path):
    position = my_text.index(INSERT)#where cursor is.#+++
    curline = my_text.get(f'{position} linestart', position)
    return path in curline
def current_line_delete():
    position = my_text.index(INSERT)#where cursor is.#+++
    #curline = my_text.get(f'{position} linestart', position)
    my_text.delete(f'{position} linestart', position)

#too complex. not pythonic.
# if string[-3:] == 'txt':
#                 if current_line_is_filepath(string):
#                     current_line_delete()
#                     open_txt(filepath = string)
#                     return True

def from_cilp(event):
    try:
        string = root.clipboard_get()
        if isfile(string):            
            try:
                add_image(string)
            except:
                pass
    except:#means img.
        im = ImageGrab.grabclipboard()
        im.save(temp_img_path)
        add_image(temp_img_path)
        
root.bind('<Control-v>', from_cilp)




def imgnowsave():
    idxs = []
    fnames = []
    imgnames = my_text.image_names()
    imgnames_remain = []
    for imgname in imgnames:
        try:
            idx = my_text.index(imgname)            
            imgnames_remain.append(imgname)
        except:
            pass
    for image in images:        
        name = image._PhotoImage__photo.name        
        if name in imgnames_remain:
            #print(name,imgnames_remain)
            im = ImageTk.getimage( image )

            name2 = name.replace('pyimage','')
            fname2 = opened_filename.replace('.txt','')# if save not txt, you now..
            fname = f'{fname2}_{name2}.png'
            #print(fname)
            im.save(fname)

            #-----phase2, text replace.

            #fname_onlyf = fname.split('/')[-1]
            fname_onlyf = split(fname)[1]
            idx_of_img = my_text.index(name)
            idx_int = int(idx_of_img.split('.')[0])
            idxs.append(idx_int)
            fnames.append(fname_onlyf)
            #my_text.delete(f'{idx_of_img} linestart' , f'{idx_of_img} lineend')            
            #my_text.insert( f'{idx_of_img} linestart', f'[{fname_onlyf}]' )
    return idxs,fnames
            

#-capture---------------------------
def realcapture(a,b,c,d):
    bbox = (a,b,c,d)
    if not (a<c and b<d):
        return False
    capture_close(1)
    im = ImageGrab.grab(bbox=bbox)
    im.save(temp_img_path)
    add_image(temp_img_path)
    

capWindow = None
capture_pointa = (0,0)
def capture_area_a(event):
    global capture_pointa
    capture_pointa = (event.x,event.y)

def capture_area_b(event):
    a,b = capture_pointa
    c,d = (event.x,event.y)
    realcapture(a,b,c,d)
def capture_close(event):
    global capWindow
    capWindow.destroy()


def capture(event=None):
    global capWindow
    capWindow = Toplevel(root)
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    capWindow.geometry(f"{w}x{h}")
    capWindow.attributes("-fullscreen", True)
    capWindow.attributes('-alpha',0.4)
    #capWindow.configure(background='gold')
    label = Label(capWindow, text ="crop area")
    label.pack()
    capWindow.bind( '<ButtonPress-1>', capture_area_a )
    capWindow.bind( '<ButtonRelease-1>', capture_area_b )

    #capWindow.bind( '<B1-Motion>', capture_area_show )
    capWindow.bind( '<Key>', capture_close )
#-capture---------------------------




#-------------------savepy
def Minsec():
    a = datetime.now()
    h = str(a.hour).zfill(2)
    m = str(a.minute).zfill(2)
    s = str(a.second).zfill(2)
    tmpname = f'{h}{m}{s}'
    return tmpname

def save_code_py(e=None):
    position = my_text.index(INSERT)#where cursor is.    

    #check1, if no [].
    current_text = my_text.get(f'{position} linestart' , position)
    if not current_text == '[]':
        messagebox.showinfo(title='Save py code', message= 'type [] First!' )
        return False

    #check2, if not yet saved. tmp.py very bad..
    if opened_filename == default_filename:
        messagebox.showinfo(title='Save py code', message= 'Save txt First!' )
        return False

    #save py file.fine.
    string = root.clipboard_get()
    if 'if' in string or 'def' in string or 'import' in string:#means py code lol
        filename = opened_filename
        minsec = Minsec()
        fn = filename.replace('.txt','')+'_'+minsec+'.py'
        f = open(fn, 'w' , encoding = 'utf-8')
        f.write(string)
        f.close()

        frealname = split(fn)[1]
        position = my_text.index(INSERT)#where cursor is.    
        my_text.insert( position, frealname)

        messagebox.showinfo(title='Save py code', message= 'saved '+fn )
#-------------------savepy


#-dir---------------------------
def createdir(e=None):
    directory = textExample.get()
    if not exists(directory):
        try:        
            makedirs(directory)            
        except OSError:
            return False
            #print ('Error: Creating directory. ' +  directory)
    button['text']="ready"
    button["fg"]="green"

def get_dir():
    return textExample.get()+'/'
#-dir---------------------------


#--------------buttons
button_frame = Frame(root)
button_frame.pack(pady=5)

#image_button = Button(button_frame, text = "add_image", command = add_image)
#image_button.pack(side=LEFT,padx=10)


#---------------------------------


button = Button(button_frame,width=7, text ="create", command=createdir)
button.pack(side=LEFT,padx=10)

textExample = Entry(button_frame,width=10)
textExample.insert(0, "txt")
textExample.pack(side=LEFT,padx=0)

button = Button(button_frame,width=7, text ="------")
button.pack(side=LEFT,padx=10)
#---------------------------------


open_button = Button(button_frame, text="OPEN Text file", command = open_txt)
open_button.pack(side=LEFT,padx=10)

save_button = Button(button_frame, text='Save txt', command=save_txt)
save_button.pack(side=LEFT,padx = 10)

saveas_button = Button(button_frame, text='as', command=save_as)
saveas_button.pack(side=LEFT,padx = 10)

cap_button = Button(button_frame, text='CAPTURE(c+b)', command=capture)
cap_button.pack(side=LEFT,padx = 30)

py_button = Button(button_frame, text='savepy(c+f)', command=save_code_py)
py_button.pack(side=LEFT,padx = 20)

#----------------------------------------scroll bar
#text_frame = Frame(root)
#text_frame.pack(pady=5)

text_scroll = Scrollbar(root)
text_scroll.pack(side = RIGHT , fill = Y)

my_text = Text(root, width=83, height=31, font=("맑은 고딕",12) ,yscrollcommand = text_scroll.set)
my_text.pack()

text_scroll.config(command = my_text.yview)
#----------------------------------------scroll bar


def callback(event):
    global savesafe
    savesafe = False

my_text.bind("<Key>",callback)
my_text.bind('<Control-b>', capture)
my_text.bind('<Control-f>', save_code_py)

root.bind('<Control-s>', save_txt)
root.bind('<Control-o>', open_txt)

root.mainloop()
