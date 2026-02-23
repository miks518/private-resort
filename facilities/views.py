from django.shortcuts import render, get_object_or_404
from .models import Facility


def facility_list(request):
    """Display all available facilities (supports search, Process 2.1)."""
    facilities = Facility.objects.filter(is_available=True)

    # Simple search
    query = request.GET.get('q', '').strip()
    if query:
        facilities = facilities.filter(name__icontains=query)

    return render(request, 'facilities/facility_list.html', {
        'facilities': facilities,
        'query': query,
    })


def facility_detail(request, slug):
    """Show facility details, gallery, and virtual tour content (Process 4.0)."""
    facility = get_object_or_404(Facility, slug=slug)
    gallery = facility.gallery_images.all()
    tours = facility.virtual_tours.all()

    return render(request, 'facilities/facility_detail.html', {
        'facility': facility,
        'gallery': gallery,
        'tours': tours,
    })


def virtual_tour_view(request, slug):
    """Dedicated virtual tour page for a facility."""
    facility = get_object_or_404(Facility, slug=slug)
    tours = facility.virtual_tours.all()

    return render(request, 'facilities/virtual_tour.html', {
        'facility': facility,
        'tours': tours,
    })
