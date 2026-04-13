# documents/models.py

from django.db import models
from django.conf import settings

class Document(models.Model):

    # All the conversion types we support
    # Each tuple is (stored_value, display_label)
    CONVERSION_CHOICES = [
        ("pdf_to_word",  "PDF to Word"),
        ("pdf_to_excel", "PDF to Excel"),
        ("pdf_to_jpg",   "PDF to JPG"),
        ("pdf_to_txt",   "PDF to TXT"),
        ("word_to_pdf",  "Word to PDF"),
        ("excel_to_pdf", "Excel to PDF"),
        ("ppt_to_pdf",   "PPT to PDF"),
        ("jpg_to_pdf",   "JPG to PDF"),
        ("txt_to_pdf",   "TXT to PDF"),
        ("html_to_pdf",  "HTML to PDF"),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")

    # The converted output file — blank/null because it doesn't exist yet
    converted_file = models.FileField(
        upload_to="converted/",
        blank=True,
        null=True
    )

    conversion_type = models.CharField(
        max_length=50,
        choices=CONVERSION_CHOICES,
        default="word_to_pdf"
    )
    # choices= tells Django (and forms) what the valid options are
    # The form will automatically render this as a <select> dropdown

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    converted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"
