import streamlit as st
from PIL import Image
import base64
import requests
from translate import Translator
import os
import base64
import ocrmypdf 
import pytesseract

pwd = os.getcwd()
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href


def MyOcr(file_path=pwd+'/input.pdf', save_path=pwd+'/output.pdf', lang='pol'):
    
    ocrmypdf.ocr(file_path, save_path, rotate_pages=True, remove_background=True,language=lang, deskew=True, force_ocr=True)
    
   
    return True;

def save_uploadedfile(uploadedfile):
     #os.remove(pwd+'/output.pdf')
     with open('input.pdf',"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} on Server".format(uploadedfile.name))

translator = Translator(to_lang="la")


image = Image.open("cerowanie.jpg")

st.image(image, width = 500)

st.title('HIPER TŁUMACZ')


s = st.text_input('Wpisz tutaj swoje słówko')
translation = translator.translate(s)


st.text(translation)


upload_pdf = st.file_uploader("put PDF file")
if(upload_pdf is None): 
    flag = False
if(upload_pdf is not None ):
    
    save_uploadedfile(upload_pdf)
    flag=True
    option = st.selectbox(
     'Jakiego języku potrzebujesz',
     ('Polski', 'Hiszpański', 'Angielski','Niemiecki','Portugalski','Francuski','Włoski','Łacina'))

    language = {
            'Polski' :  'pol',
            'Hiszpański' :  'spa',
            'Angielski' :  'eng',
            'Niemiecki' :  'deu',
            'Portugalski' :  'por',
            'Łacina' :  'lat',
            'Francuski' :  'fra',
            'Włoski' :  'ita'
                }[option]
        

    st.write('You selected:', option)
    btn_ocr = st.button("START OCR")
    if btn_ocr:
        MyOcr(lang=language)
        
    if(os.path.isfile(pwd+'/output.pdf')):
        btn_download = st.button("Click to Download")

        if btn_download:
            st.markdown(get_binary_file_downloader_html(pwd+'/output.pdf','PDF'),unsafe_allow_html=True)



