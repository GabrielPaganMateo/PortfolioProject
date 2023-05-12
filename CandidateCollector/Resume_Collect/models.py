from django.db import models
from django.utils import timezone
import uuid
from .utils import extract_name, extract_phone, extract_email, extract_education, extract_experience, list_text, Folder_extract, File_extract, extract_text_from_pdf, extract_text_from_docx


# Create your models here.
class Opening(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.name} {self.__class__.__name__}: ({self.id}) created_at: {self.created_at}'
    
    def create_Opening(self, name):
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
    
    def create_Candidate_from_files(self):
        files = File_extract()
        for file_path in files:
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
                text_list=text_list
            )
            candidate.save()

    def create_Candidates_from_folder(self):
        pass
    
class Extract_from_file():
    def __init__(self):
        files = File_extract()
        for file_path in files:
            if str(file_path).endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif str(file_path).endswith(".docx"):
                text = extract_text_from_docx(file_path)
        return text

