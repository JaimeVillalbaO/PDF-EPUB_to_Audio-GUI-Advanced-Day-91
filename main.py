from tkinter import Tk, Label, Button, Entry, filedialog
import PIL
from PIL import Image, ImageTk
import pyttsx3
from PyPDF2 import PdfReader
from epub_conversion.utils import open_book,  convert_epub_to_lines
from gtts import gTTS
import re


BACKGROUND_COLOR = "#000000"

def select_file():
    global filepath, filename
    try:
        filepath = filedialog.askopenfilename(filetypes=[('Choose File', '*.pdf  *.epub')])
        filename = filepath.split('/')[-1].split('.')[0]
        file_entry.delete(0, "end")
        file_entry.insert(0, filename)
    except AttributeError:
        pass

def clean_text(text):
    # Eliminar etiquetas HTML y otros caracteres no deseados usando expresiones regulares
    clean_text = re.sub(r'<[^>]+>', '', text)
    clean_text = re.sub(r'[^A-Za-z0-9ñáéíóúüÜÁÉÍÓÚ.,?!¡¿\s]', '', clean_text)
    return clean_text

def convert():
    if filepath.endswith('.pdf'):
    # Abrir el archivo PDF
        with open(filepath, 'rb') as file:
            # Crear un objeto PdfReader
            pdf_reader = PdfReader(file)
            
            # Obtener el número total de páginas en el PDF
            num_pages = len(pdf_reader.pages)
            
            # Inicializar el motor de texto a voz
            engine = pyttsx3.init()
            
            # Iterar sobre cada página del PDF
            for page_num in range(num_pages):
                # Obtener el texto de la página actual
                text = pdf_reader.pages[page_num].extract_text()
                
                # Convertir el texto en voz
                engine.say(text)
                engine.runAndWait()

    elif filepath.endswith('.epub'):  # Verificar si el archivo es un EPUB
        book = open_book(filepath)  # Abrir el archivo EPUB
        lines = convert_epub_to_lines(book)  # Convertir el contenido del libro a líneas de texto
        num_pages = len(lines)  # Obtener el número de páginas del libro
        # engine = pyttsx3.init()  # Inicializar el motor de texto a voz
        filename_mp3 = f'{filename}.mp3'
        total_text = ''  # Inicializar una cadena para almacenar todo el texto
        for page_num in range(num_pages):  # Iterar sobre cada página del EPUB
            # text = lines[page_num]  # Obtener el texto de la página actual
            # engine.say(text)  # Convertir el texto a voz
            # engine.runAndWait()   #Esperar a que se complete la conversión
            total_text += lines[page_num] # Agregar el texto de la página actual
            cleaned_text = clean_text(total_text) # Limpiar el texto
        tts = gTTS(cleaned_text, lang='es') # Crear un objeto gTTS con el texto limpio y el idioma especificado
        tts.save(filename_mp3)  # Guardar el audio en un archivo MP3



window = Tk()
window.title('Convert Files To AudioBook')


file = (Image.open('image.jpg'))
img = file.resize((900, 500), Image.LANCZOS)
final_img = ImageTk.PhotoImage(img)
panel = Label(window, image=final_img)
panel.image = final_img
panel.grid(column=0, row=0)


select_file_button = Button(text='Select File', font=("Arial", 12), bg=BACKGROUND_COLOR, fg='#fafafa', command=select_file)
select_file_button.grid(column=0, row=0,padx=(0,500), pady=(250, 0))

file_entry = Entry(width=60, bg=BACKGROUND_COLOR, fg='#fafafa',  font=("Arial", 12), justify='center')
file_entry.grid(column=0, row=0, padx=(150, 0), pady=(250, 0))

convert_button = Button(text='Convert to Audio', font=("Arial", 12), bg='red', fg='#fafafa', command=convert)
convert_button.grid(column=0, row=0, padx=(565, 0), pady=(310, 0))

window.mainloop()