from django.shortcuts import render,  redirect
from fnb.models import Fnb
from django.shortcuts import render
from review.models import Review, ReviewLike
from review.forms import ReviewForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.utils.html import strip_tags


def show_review(request):
    food_id = request.GET.get('id')
    fnb_object = Fnb.objects.get(pk=food_id)
    semua_review = Review.objects.filter(makanan=fnb_object)
    
    # Ambil semua review yang disukai oleh pengguna saat ini
    review_user = ReviewLike.objects.filter(user=request.user).values_list('review_id', flat=True)

    context = {
        'name': fnb_object.name,
        'price': fnb_object.price,
        'description': fnb_object.description,
        'reviews': semua_review,
        'id': fnb_object.id,
        'review_user': list(review_user)  # Ubah menjadi list untuk kemudahan penggunaan di template
    }
    return render(request, "main.html", context)
# Create your views here.


def add_review(request):
    # Ambil data dari request POST
    food_id = request.POST.get("food_id")
    rating = request.POST.get("rating")
    text = request.POST.get("text")
    fnb_object = Fnb.objects.get(pk=food_id)
    
    user = request.user  

    # Bersihkan input dari tag HTML untuk mencegah XSS (opsional)
    cleaned_text = strip_tags(text)

    # Buat instance Review baru dan simpan ke database
    review_entry = Review(
        rating=rating,
        text=cleaned_text,
        makanan=fnb_object,
        user=user
        
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
    user = request.user

    if not user.is_authenticated:
        return HttpResponse("User must be logged in", status=401)

    # Cek apakah user sudah like review ini
    existing_like = ReviewLike.objects.filter(review=review, user=user).first()

    if existing_like:
        # User sudah like, jadi kita hapus like
        existing_like.delete()
        review.like -=1
        review.save()
    else:
        # User belum like, jadi kita tambahkan like
        ReviewLike.objects.create(review=review, user=user)
        review.like +=1
        review.save()

    # Kembalikan response status 201 CREATED
    return HttpResponse(b"CREATED", status=201)
