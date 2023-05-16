from django.db import models
from django.utils import timezone
import uuid
from .utils import extract_name, extract_phone, extract_email, extract_education, extract_experience, list_text, extract_text_from_pdf, extract_text_from_docx, OpenFileDialog, OpenFolderDialog, SelectFileButton, SelectFolderButton
from tkinter import Tk, ttk
import tkinter

# Create your models here.
class Opening(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.name} {self.__class__.__name__}: ({self.id}) created_at: {self.created_at}'
    
    def create(self, name):
        return Opening.objects.create(name=name)

class Candidate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    text_list = models.TextField()
    opening = models.ForeignKey(Opening, null=True, related_name='candidates', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.name} ({self.id}) created_at: {self.created_at}'

"""The following functions are for the creation of model objects"""
def createOpening(name):
    opening = Opening.objects.create(name=name)
    opening.save()
    return opening

def createCandidate(opening_object):
    """Creating Master Window"""
    window = Tk()
    window.title("Candidate Collection")
    window.resizable(True, True)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # Calculate the window position
    window_width = 600
    window_height = 300
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.configure(bg="#0076CE")
    # Set the window position
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.attributes('-topmost', True)
    """Creating Buttons and Returning FilePath"""
    file_pathContainer = OpenFileDialog()
    folder_pathContainer = OpenFolderDialog()
    SelectFileButton(window, file_pathContainer)
    SelectFolderButton(window, folder_pathContainer)
    ttk.Button(window, text="Quit", command=window.destroy).pack(expand=True)
    window.mainloop()
    """Printing file_path and Resume name, from files or folder"""
    candidate_list = []
    text = ""
    if file_pathContainer.file_path is not None:
        for file_path in file_pathContainer.file_path:
            if str(file_path).endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif str(file_path).endswith(".docx"):
                text = extract_text_from_docx(file_path)
            name = extract_name(text)
            phone = extract_phone(text)
            email = extract_email(text)
            education = extract_education(text)
            experience = extract_experience(text)
            text_list = list_text(text)
        
            candidate = Candidate.objects.create(
                name=name,
                phone=phone,
                email=email,
                education=education,
                experience=experience,
                text_list=text_list,
                opening=opening_object
            )
            candidate.save()
            candidate_list.append(candidate)
        return candidate_list
    elif folder_pathContainer.folder_path is not None:
        for file_path in folder_pathContainer.folder_path:
            if str(file_path).endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif str(file_path).endswith(".docx"):
                text = extract_text_from_docx(file_path)
            name = extract_name(text)
            phone = extract_phone(text)
            email = extract_email(text)
            education = extract_education(text)
            experience = extract_experience(text)
            text_list = list_text(text)
        
            candidate = Candidate.objects.create(
                name=name,
                phone=phone,
                email=email,
                education=education,
                experience=experience,
                text_list=text_list,
                opening=opening_object
            )
            candidate.save()
            candidate_list.append(candidate)
        return candidate_list


