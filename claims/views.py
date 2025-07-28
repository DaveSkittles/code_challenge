from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
import json

from .models import Claim, Annotation


def index(request):
    """Main dashboard view"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Calculate statistics for dashboard
    stats = Claim.objects.aggregate(
        total_claims=Count('id'),
        flagged_claims=Count('id', filter=Q(flagged_for_review=True)),
        approved_claims=Count('id', filter=Q(status='approved')),
        denied_claims=Count('id', filter=Q(status='denied')),
    )
    
    return render(request, 'claims/index.html', stats)


def login_view(request):
    """Simple login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'claims/login.html')


@login_required
def claim_list(request):
    """HTMX-powered claim list with search and filtering"""
    claims = Claim.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        claims = claims.filter(
            Q(claim_id__icontains=search_query) |
            Q(patient_name__icontains=search_query) |
            Q(insurer_name__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        claims = claims.filter(status=status_filter)
    
    # Filter by flagged status
    flagged_filter = request.GET.get('flagged', '')
    if flagged_filter == 'true':
        claims = claims.filter(flagged_for_review=True)
    elif flagged_filter == 'false':
        claims = claims.filter(flagged_for_review=False)
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(claims, 20)  # 20 claims per page
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'flagged_filter': flagged_filter,
        'status_choices': Claim.STATUS_CHOICES,
    }
    
    # Return partial template for HTMX requests
    if request.headers.get('HX-Request'):
        return render(request, 'claims/partials/claim_list.html', context)
    
    return render(request, 'claims/claim_list.html', context)


@login_required
def claim_detail(request, claim_id):
    """Claim detail view for modal/panel"""
    claim = get_object_or_404(Claim, id=claim_id)
    annotations = claim.annotations.all()
    
    context = {
        'claim': claim,
        'annotations': annotations,
    }
    
    return render(request, 'claims/partials/claim_detail.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_flag(request, claim_id):
    """Toggle claim flag status"""
    claim = get_object_or_404(Claim, id=claim_id)
    claim.flagged_for_review = not claim.flagged_for_review
    claim.save()
    
    return render(request, 'claims/partials/flag_button.html', {'claim': claim})


@login_required
@require_http_methods(["POST"])
def add_annotation(request, claim_id):
    """Add annotation to claim"""
    claim = get_object_or_404(Claim, id=claim_id)
    content = request.POST.get('content', '').strip()
    
    if content:
        annotation = Annotation.objects.create(
            claim=claim,
            user=request.user,
            content=content
        )
        
        # Return the new annotation HTML
        return render(request, 'claims/partials/annotation_item.html', {
            'annotation': annotation
        })
    
    return HttpResponse('')


@login_required
@require_http_methods(["DELETE"])
def delete_annotation(request, annotation_id):
    """Delete annotation"""
    annotation = get_object_or_404(Annotation, id=annotation_id, user=request.user)
    annotation.delete()
    return HttpResponse('')


@login_required
def get_annotations(request, claim_id):
    """Get all annotations for a claim"""
    claim = get_object_or_404(Claim, id=claim_id)
    annotations = claim.annotations.all()
    
    return render(request, 'claims/partials/annotations_list.html', {
        'annotations': annotations,
        'claim': claim
    })
