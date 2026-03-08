from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Vendor
from .forms import SignUpForm, VendorForm
from django.contrib.auth.decorators import login_required



def get_sorted_vendors():
    """
    Utility function to fetch and sort vendors by score.
    """
    vendors = list(Vendor.objects.all())
    vendors.sort(key=lambda v: v.vendor_score(), reverse=True)
    return vendors


def home(request):
    vendors = list(Vendor.objects.all())
    vendors.sort(key=lambda v: v.vendor_score(), reverse=True)

    # Add computed fields
    for index, vendor in enumerate(vendors, start=1):
        vendor.rank = index
        vendor.score = round(vendor.vendor_score(), 2)
        vendor.score_100 = round(vendor.vendor_score() * 20, 0)  # 1-5 scale to 0-100
        vendor.delivery_percent = round(vendor.delivery_rating * 20, 0)
        vendor.quality_percent = round(vendor.quality_rating * 20, 0)
        vendor.price_percent = round(vendor.price_rating * 20, 0)
        vendor.communication_percent = round(vendor.communication_rating * 20, 0)

    total_vendors = len(vendors)
    top_vendor = vendors[0] if vendors else None
    highest_score = top_vendor.score if top_vendor else 0
    top_three = vendors[:3]

    # Chart Data (Top 5 Vendors)
    top_five = vendors[:5]
    chart_labels = [v.name for v in top_five]
    chart_scores = [v.score for v in top_five]

    context = {
        'total_vendors': total_vendors,
        'top_vendor': top_vendor,
        'highest_score': highest_score,
        'top_three': top_three,
        'vendors': vendors,
        'chart_labels': chart_labels,
        'chart_scores': chart_scores,
    }

    return render(request, 'vendor/home.html', context)

@login_required
def dashboard(request):
    vendors = list(Vendor.objects.all())
    vendors.sort(key=lambda v: v.vendor_score(), reverse=True)

    # Add ranking and computed fields
    for index, vendor in enumerate(vendors, start=1):
        vendor.rank = index
        vendor.score = round(vendor.vendor_score(), 2)
        vendor.delivery_percent = round(vendor.delivery_rating * 20, 1)  # 1-5 scale to %
        vendor.quality_percent = round(vendor.quality_rating * 20, 1)

    total_vendors = len(vendors)

    top_vendor = vendors[0] if vendors else None
    highest_score = top_vendor.score if top_vendor else 0

    average_score = round(
        sum(v.score for v in vendors) / total_vendors, 2
    ) if total_vendors > 0 else 0

    context = {
        'vendors': vendors,
        'total_vendors': total_vendors,
        'top_vendor': top_vendor,
        'highest_score': highest_score,
        'average_score': average_score,
    }

    return render(request, 'vendor/dashboard.html', context)

@login_required
def vendor_list(request):
    vendors = get_sorted_vendors()
    for v in vendors:
        v.score = round(v.vendor_score(), 2)
    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})


@login_required
def add_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            messages.success(request, f'Vendor "{vendor.name}" added successfully!')
            return redirect('dashboard')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = VendorForm()

    return render(request, 'vendor/add_vendor.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'vendor/signup.html', {'form': form})
