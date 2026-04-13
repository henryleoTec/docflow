# documents/views.py

from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.http import require_http_methods
import threading

from .models import Document
from .forms import DocumentForm
from .utils import convert_document

# In-memory store for conversion progress
# Key = document pk, Value = dict with status and percent
conversion_progress = {}


# ── Class-Based Views (CRUD) ──────────────────────────────────────────────────

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = "documents/document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        # Only return documents belonging to the logged-in user
        return Document.objects.filter(owner=self.request.user)


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "documents/document_detail.html"
    context_object_name = "document"

    def get_queryset(self):
        # Security: users can only view their own documents
        return Document.objects.filter(owner=self.request.user)


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/document_form.html"
    success_url = reverse_lazy("document-list")

    def dispatch(self, request, *args, **kwargs):
        # dispatch() runs before get() or post()
        # Block upload if user has reached the 5-file free tier limit
        if request.user.is_authenticated:
            user_count = Document.objects.filter(owner=request.user).count()
            if user_count >= 5:
                messages.error(
                    request,
                    "You've reached the 5 document limit on the free tier."
                )
                return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Attach the logged-in user as owner before saving
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = "documents/document_confirm_delete.html"
    success_url = reverse_lazy("document-list")

    def get_queryset(self):
        # Security: users can only delete their own documents
        return Document.objects.filter(owner=self.request.user)


# ── Conversion Views ──────────────────────────────────────────────────────────

@login_required
@require_http_methods(["GET", "POST"])
def convert_view(request, pk):
    document = get_object_or_404(Document, pk=pk, owner=request.user)
    # get_object_or_404 returns 404 if not found or belongs to another user

    if document.converted:
        messages.info(request, "This document has already been converted.")
        return redirect("document-detail", pk=pk)

    # Mark conversion as started in the progress store
    conversion_progress[pk] = {"status": "running", "percent": 0}

    def run_conversion():
        # Step 1 — file picked up
        conversion_progress[pk]["percent"] = 30

        success, message = convert_document(document)

        # Step 2 — conversion done, now sending email
        conversion_progress[pk]["percent"] = 90

        if success:
            download_url = f"http://127.0.0.1:8000/documents/{document.pk}/"

            email_body = render_to_string(
                "documents/emails/conversion_done.html",
                {
                    "user": document.owner,
                    "document": document,
                    "download_url": download_url,
                }
            )

            email = EmailMessage(
                subject=f"Your file '{document.title}' is ready!",
                body=email_body,
                to=[document.owner.email]
            )
            email.content_subtype = "html"
            email.send()

            # Mark fully done
            conversion_progress[pk] = {"status": "done", "percent": 100}

        else:
            conversion_progress[pk] = {
                "status": "error",
                "percent": 0,
                "message": message,
            }

    # Run conversion in a background thread so the response returns immediately
    # Without threading, Django would freeze the page until conversion finishes
    thread = threading.Thread(target=run_conversion)
    thread.daemon = True
    # daemon=True — thread dies automatically when the server shuts down
    thread.start()

    # Return immediately so JS can start polling /status/
    return JsonResponse({"status": "started"})


@login_required
def conversion_status(request, pk):
    # Called by JS every second to check conversion progress
    # Returns JSON like: {"status": "running", "percent": 30}
    progress = conversion_progress.get(pk, {"status": "idle", "percent": 0})
    return JsonResponse(progress)


# ── Dashboard View ────────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    user = request.user
    documents = Document.objects.filter(owner=user)

    total = documents.count()
    converted = documents.filter(converted=True).count()
    pending = total - converted
    remaining = max(0, 5 - total)
    # max(0, ...) prevents showing a negative number when over the limit

    # Breakdown of which conversion types the user has used
    # values() groups by the field, annotate() adds a COUNT per group
    type_breakdown = (
        documents
        .values("conversion_type")
        .annotate(count=Count("id"))
        .order_by("-count")
        # -count means descending — most used type appears first
    )

    # Most recent 5 documents, newest first
    recent_documents = documents.order_by("-created_at")[:5]

    context = {
        "total": total,
        "converted": converted,
        "pending": pending,
        "remaining": remaining,
        "limit": 5,
        "usage_percent": int((total / 5) * 100) if total <= 5 else 100,
        # Clamp at 100% so the bar never overflows
        "type_breakdown": type_breakdown,
        "recent_documents": recent_documents,
    }

    return render(request, "documents/dashboard.html", context)
