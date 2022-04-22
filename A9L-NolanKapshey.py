#   LAB 9 PYTHON 
#   -----------------------------------------------------------------
#   -----------------------------------------------------------------
#   PROGRAM DESCRIPTION: This lab is designed to create a GUI page of
#   the POKEAPI and allow the user to select a certain pokemon, and 
#   their results will show up on the GUI information page after 
#   getting the results from the PokeAPI, adding on, they will be
#   able to change their desktop background image if they wish 
#   within the GUI interface.
#   -----------------------------------------------------------------
#   -----------------------------------------------------------------
#   USAGE: python A9L-NolanKapshey.py
#
#   -----------------------------------------------------------------
#   -----------------------------------------------------------------
#
#   DUE DATE: MONDAY APRIL 25TH, 2022
#
#   -----------------------------------------------------------------
#   -----------------------------------------------------------------
#   HISTORY:
#       DATE        AUTHOR      Description
#       2022-04-20  N.KAPSHEY   Initial Creation
#
#   _________________________________________________________________

#   Gather all the imports 
from tkinter import * 
from tkinter import ttk
from requests import request
import requests
from Poke_API import get_poke_list, get_pokemon_image_url
import os
import sys
import ctypes

#   Create the main function of the program
def main(): 
    
    script_dir = sys.path[0]
    images_dir = os.path.join(script_dir, 'images')
    if not os.path.isdir(images_dir):
        os.makedirs(images_dir)

#   Create the window/GUI page
    root = Tk()
    root.title ('Pokemon Image Getta 3000')
    app_id = 'COMP593.PokemonImageViewer'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    root.iconbitmap(os.path.join(script_dir, 'poke.ico'))
    root.columnconfigure(0, weight = 80)
    root.rowconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 1)
    root.geometry('600x600')
    
    
    frm = ttk.Frame(root)
    frm.grid(sticky =( N,S,E,W))
    frm.columnconfigure(0, weight = 80)
    frm.rowconfigure(0, weight = 10)

#   Get the image of the pokemon   
    img_poke = PhotoImage(file = os.path.join(script_dir, 'poke_ball.png'))
    lbl_image = Label(frm, image= img_poke)
    lbl_image.grid(row=0, column=0, padx =10, pady=10)

#   Get the list of pokemon    
    pokemon_list = get_poke_list(limit=1000)
    pokemon_list.sort()
    cbo_poke_sel = ttk.Combobox(frm, values=pokemon_list, state= 'readonly')
    cbo_poke_sel.set('Select a Pokemon')
    cbo_poke_sel.grid(row = 1, column = 0)

#   Create the button of setting the desktop background image  
    def btn_set_desktop_click():
        pokemon_name = cbo_poke_sel.get()
        image_path = os.path.join(images_dir, pokemon_name + '.png')
        set_desktop_background_image(image_path)

#   Search the pokemon interface for the image of the pokemon    
    def handle_cbo_pokemon_sel(event):
        poke_name = cbo_poke_sel.get()
        image_url = get_pokemon_image_url(poke_name)
        image_path = os.path.join(images_dir, poke_name + '.png')
        if download_imgae_from_url (image_url, image_path):
            img_poke['file'] = image_path
            btn_set_desktop.state(['!disabled'])
    
    cbo_poke_sel.bind('<<ComboboxSelected>>', handle_cbo_pokemon_sel)   

#   Get the image URL from POKEAPI 
    def download_imgae_from_url(url, path):
        resp_msg = requests.get(url)
        if resp_msg.status_code == 200: 
            try:
                img_data = resp_msg.content
                with open (path, 'wb') as fp:
                    fp.write(img_data)
                return path
            except:
                return
        else:
            print ("ERROR: Failed to download the image.")
            print("RESPONCE CODE:", resp_msg.status_code)
            print (resp_msg.text)
    btn_set_desktop = ttk.Button(frm, text = 'Set as Desktop Background', command= btn_set_desktop_click)
    btn_set_desktop.state(['disabled'])
    btn_set_desktop.grid(row=2, column=0, padx = 10, pady = 10)    

#   Set the desktop image background 
    def set_desktop_background_image(path):
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        except:
            print("ERROR: Unable to set the desktop background.")  
    
    root.mainloop()
    
main()