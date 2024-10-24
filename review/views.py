from django.shortcuts import render,  redirect
from fnb.models import Fnb
from django.http import JsonResponse
from django.shortcuts import render
from review.models import Review
from review.forms import ReviewForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
import json

def show_review(request):
    food_id = request.GET.get('id')
    fnb_object = Fnb.objects.get(pk=food_id)
    semua_review = Review.objects.filter(makanan=fnb_object)
    
    
    context = {
        'name' : fnb_object.name,
        'price': fnb_object.price,
        'description': fnb_object.description,
        'reviews' : semua_review,
        'id' : fnb_object.id

    }
    return render(request, "main.html", context)
# Create your views here.


def add_review(request):
    # Ambil data dari request POST
    food_id = request.POST.get("food_id")
    rating = request.POST.get("rating")
    text = request.POST.get("text")
    fnb_object = Fnb.objects.get(pk=food_id)
    
    # user = request.user  # Ambil pengguna yang sedang login

    # Bersihkan input dari tag HTML untuk mencegah XSS (opsional)
    cleaned_text = strip_tags(text)

    # Buat instance Review baru dan simpan ke database
    review_entry = Review(
        rating=rating,
        text=cleaned_text,
        makanan=fnb_object
        
        # user_name=user.username  # Atau field user jika adaForeignKey
    )
    review_entry.save()

    # Kembalikan response status 201 CREATED
    return HttpResponse(b"CREATED", status=201)

@require_POST
def like_review(request):
    # Ambil data dari request POST
    review_id = request.POST.get("review_id")
    
    # Dapatkan objek Review atau return 404 jika tidak ditemukan
    review = Review.objects.get(pk=review_id)
    
    # Tambahkan jumlah like
    review.like += 1
    review.save()

    # Buat dictionary dengan data response

    # Kembalikan HttpResponse dengan JSON string dan status 200 OK
    return HttpResponse(b"CREATED", status=201)
