import docx2txt
from odf import text, teletype
from odf.opendocument import load
from pdfminer.high_level import extract_text
import spacy
import re
from word2number import w2n
 
"""Functions to extract text of docs"""
def extract_text_from_docx(docx_path):

    txt = docx2txt.process(docx_path)
    if txt:
        return txt.replace('\t', ' ')
    return None

def extract_text_from_odt(odt_path):
    textdoc = load(odt_path)
    all_text = textdoc.getElementsByType(text.P)
    
    return teletype.extractText(all_text[0])

def extract_text_from_pdf(pdf_path):
        
    return extract_text(pdf_path)

"""Functions to extract info of text"""
def extract_name(text):
    """
    Function extracts full name from
    text, however the name must be the first set of words within the text
    else something besides the name will be extracted
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    name = ""
    for token in doc:
        if token.pos_ == "PROPN":
            name += token.text + " "
        else:
            break
    if name == '':
        return None
    else:
        return name[:-1]

def extract_phone(text):
    """
    Function extracts phone from text
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]*\d{3}[-.\s]*\d{4}')
    """phone_pattern edge case: (123)-456-7890, fix this"""
    match = re.findall(phone_pattern, doc.text)
    if match == []:
        return None
    else:
        return match[0]
    
def extract_email(text):
    """
    Function extracts email from text
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    match = re.findall(email_pattern, doc.text)
    if match == []:
        return None
    else:
        return match[0]
    
def extract_education(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    school_level = ['HS', 'H.S.', 'GED', 'SECONDARY EDUCATION', 'SCHOOL', 'HIGH SCHOOL']
    associate_level = ['AA', 'A.A.', 'ASSOCIATE OF ARTS', 'A.S.', 'ASSOCIATE OF SCIENCE', 'ASSOCIATE'] 
    bachelor_level = ['BA', 'B.A.', 'BACHELOR OF ARTS', 'BS', 'B.S.', 'BACHELOR OF SCIENCE', 'BACHELOR']
    master_level = ['MA', 'M.A.', 'MASTER OF ARTS', 'MS', 'M.S.', 'M.Sc.', 'MSc', 'MASTER OF SCIENCE', 'MASTER'] 
    doctor_level = ['M.D.', 'MD', 'DOCTOR OF MEDICINE', 'J.D.', 'JD', 'JURIS DOCTOR', 'PH.D.', 'PHD', 'DOCTOR OF PHILOSOPHY', 'ED.D.', 'EDD', 'DOCTOR OF EDUCATION', 'DOCTOR', 'DOCTORATE', 'DR.']
    next_token = 0

    for token in doc:
        next_token += 1
        if token.text.upper() in doctor_level:
            return 'Doctoral degree'
        elif token.text.upper() in master_level:
            return 'Master\'s degree'
        elif token.text.upper() in bachelor_level:
            return 'Bachelor\'s degree'
        elif token.text.upper() in associate_level:
            return 'Associate\'s degree'

        elif next_token < len(doc):
            compound_word_2 = ("{} {}".format(token.text.upper(), doc[next_token]).upper())
            if compound_word_2 in doctor_level:
                return 'Doctoral degree'
            elif compound_word_2 in master_level:
                return 'Master\'s degree'
            elif compound_word_2 in bachelor_level:
                return 'Bachelor\'s degree'
            elif compound_word_2 in associate_level:
                return 'Associate\'s degree'

        elif (next_token + 1) < len(doc):
            compound_word_3 = ("{} {} {}".format(token.text.upper(), doc[next_token]).upper(), doc[next_token + 1].upper())
            if compound_word_3 in doctor_level:
                return 'Doctoral degree'
            elif compound_word_3 in master_level:
                return 'Master\'s degree'
            elif compound_word_3 in bachelor_level:
                return 'Bachelor\'s degree'
            elif compound_word_3 in associate_level:
                return 'Associate\'s degree'

    for token in doc:
        next_token += 1
        if token.text.upper() in school_level:
            return 'Certificate'
        elif next_token < len(doc):
            compound_word_2 = ("{} {}".format(token.text.upper(), doc[next_token]).upper())
            if compound_word_2 in school_level:
                return 'Certificate'
        elif (next_token + 1) < len(doc):
            compound_word_3 = ("{} {} {}".format(token.text.upper(), doc[next_token]).upper(), doc[next_token + 1].upper())
            if compound_word_3 in school_level:
                return 'Certificate'

    return None

def extract_experience(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    next_token = 0

    for token in doc:
        next_token += 1
        if next_token < len(doc):
            if token.like_num and doc[next_token].text == 'years':
                if token.is_alpha:
                    word_to_num = w2n.word_to_num(token.text)
                    return f'{word_to_num} years'
                else:
                    return f'{token.text} years'
            elif token.like_num and doc[next_token + 1].text == 'years':
                if token.is_alpha:
                    word_to_num = w2n.word_to_num(token.text)
                    return f'{word_to_num} years'
                else:
                    return f'{token.text} years'

def extract_title(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    next_token = 0
    title_list = ['server']

    for token in doc:
        next_token += 1
        if token.text.lower() in title_list:
            title = token.text.capitalize()
            return title 
        elif next_token < len(doc):
            compound_word_2 = ("{} {}".format(token.text.lower(), doc[next_token]).lower())
            if compound_word_2 in title_list:
                title = compound_word_2.capitalize()
                return title
        elif (next_token + 1) < len(doc):
            compound_word_3 = ("{} {} {}".format(token.text.lower(), doc[next_token]).lower(), doc[next_token + 1].lower())
            if compound_word_3 in title_list:
                title = compound_word_3.capitalize()
                return title
    return None

def list_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    space_list = ['', ' ', '  ', '   ', '    ', '     ', '      ', '       ', '        ', '         ', '          ']
    text_list = []
    for token in doc:
        if token.dep_ != 'det' and not token.is_punct and "\n" not in token.text and "\uf0b7" not in token.text and token.like_num is not True and token.text != ' ' and token.text not in space_list:
            text_list.append(token.text.lower())
    
    combined = []
    next_word = 0
    for i in range(len(text_list)):
        next_word += 1
        if next_word < len(text_list):
            compound_word_2 = ("{} {}".format(text_list[i].lower(), text_list[next_word].lower()))
            combined.append(compound_word_2)
        if (next_word + 1) < len(text_list):
            compound_word_3 = ("{} {} {}".format(text_list[i].lower(), text_list[next_word].lower(), text_list[next_word + 1].lower()))
            combined.append(compound_word_3)

    text_list.extend(combined)
    return text_list

"""The following functions are related to fileDialog and tkinter windows"""

from tkinter import filedialog
from tkinter import Tk
from pathlib import Path
from tkinter import ttk
import tkinter as tk

def File_extract():
    """
    Opens file dialog and permits file selection
    with subsequent return of the file's path
        (In order to select multiple files you must hold the Ctrl button)
    """
    filetypes = [
        ('All files', '*.*'),
        ('pdf files', '*.pdf'),
        ('docx files', '*.docx'),
        ]

    files = filedialog.askopenfilename(multiple=True, initialdir='/home/holberton/Repo\'s/Resume_Parsing/ExampleResumes', filetypes=filetypes, title="Select files")
    return files

def Folder_extract():
    """
    Opens file dialog and permits folder ('directory')
    selection with subsequent return of the file paths
    of every file within the folder
        (This dialog require you to be inside of the folder that
        you want to select 'Selection:/DesiredFolder')
    """
    folder = filedialog.askdirectory(mustexist=True, title="Select a folder", initialdir='/home/holberton/Repo\'s/Resume_Parsing')
    if folder == "":
        pass
    else:
        try:
            files = Path(folder).glob('*')
            return files
        except Exception:
            pass

class OpenFileDialog:
    def __init__(self):
        self.file_path = None
    
    def set_file_path(self, window):
        self.file_path = File_extract()
        if not self.file_path or self.file_path == "":
            pass
        elif self.file_path is not type(tuple):
            if self.file_path == ():
                pass
            else:
                window.destroy()
        elif self.file_path is None:
            pass


class OpenFolderDialog:
    def __init__(self):
        self.folder_path = None

    def set_folder_path(self, window):
        self.folder_path = Folder_extract()
        if self.folder_path is None:
            pass
        elif self.folder_path == "":
            pass
        else:
            window.destroy()


class SelectFileButton:
    def __init__ (self, window, obj):
        self.button = ttk.Button(window, text="Select files", command=lambda: obj.set_file_path(window)).pack(expand=True)

class SelectFolderButton:
    def __init__(self, window, obj):
        self.button = ttk.Button(window, text="Select a folder", command=lambda: obj.set_folder_path(window)).pack(expand=True)


def AskOpenFilename():
    window = Tk()
    window.withdraw()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 600
    window_height = 300
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    # Set the window position
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    """
    Opens file dialog and permits file selection
    with subsequent return of the file's path
        (In order to select multiple files you must hold the Ctrl button)
    """
    filetypes = [
        ('All files', '*.*'),
        ('pdf files', '*.pdf'),
        ('docx files', '*.docx'),
        ]

    files = filedialog.askopenfilename(multiple=True, initialdir='/home/holberton/Repo\'s/Resume_Parsing/ExampleResumes', filetypes=filetypes, title="Select files")
    window.destroy()
    return files

def AskDirectory():
    window = Tk()
    window.withdraw()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 600
    window_height = 300
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    # Set the window position
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    """
    Opens file dialog and permits folder ('directory')
    selection with subsequent return of the file paths
    of every file within the folder
        (This dialog require you to be inside of the folder that
        you want to select 'Selection:/DesiredFolder')
    """
    folder = filedialog.askdirectory(mustexist=True, title="Select a folder", initialdir='/home/holberton/Repo\'s/Resume_Parsing')
    if folder == "":
        pass
    else:
        try:
            files = Path(folder).glob('*')
            if files != None:
                return files
        except Exception:
            pass
        window.destroy()