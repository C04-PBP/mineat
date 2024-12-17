from django.shortcuts import render,  redirect
from fnb.models import Fnb
from django.shortcuts import render, reverse
from django.core import serializers

from review.models import Review, ReviewLike
from review.forms import ReviewForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404


def show_review(request):
    food_id = request.GET.get('id')
    fnb_object = Fnb.objects.get(pk=food_id)
    
    if request.user.is_authenticated:
    # Ambil semua review yang disukai oleh pengguna saat ini
        review_user = ReviewLike.objects.filter(user=request.user).values_list('review_id', flat=True)
        
    else:
        review_user = "Null"

    context = {
        'name': fnb_object.name,
        'image': fnb_object.image,
        'price': fnb_object.price,
        'description': fnb_object.description,
        'id': fnb_object.id,  # Ubah menjadi list untuk kemudahan penggunaan di template
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

def load_reviews(request):
    # Query untuk mendapatkan data review
    food_id = request.GET.get('id')
    fnb_object = Fnb.objects.get(pk=food_id)
    sort_option = request.GET.get('sort')

    # Apply different sorting based on the selected option
    print("awal")
    if sort_option == 'newest':
        reviews = Review.objects.filter(makanan=fnb_object).order_by('-created_at')
        print(reviews)
        print("masuk")
    elif sort_option == 'like':
        reviews = Review.objects.filter(makanan=fnb_object).order_by('-like')
    else:  # Default to sorting by date
        reviews = Review.objects.filter(makanan=fnb_object)
        print(reviews)
        print("masuk2")
    
    if request.user.is_authenticated:
    # Ambil semua review yang disukai oleh pengguna saat ini
        review_user = ReviewLike.objects.filter(user=request.user).values_list('review_id', flat=True)
        
    else:
        review_user = "Null"
        
    context = {'reviews': reviews,
               'review_user': list(review_user),
               'food_id' : food_id}
    return render(request, 'show_review.html', context)

def load_write_review(request):
    food_id = request.GET.get('id')  # Get the food_id from query parameters
    return render(request, 'add_review.html', {'food_id': food_id})

def delete_review(request, id):
    # Get mood berdasarkan id
    food_id = request.GET.get('id')
    review = Review.objects.get(pk=id)
    # Hapus mood
    review.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('review:show_review') + f'?id={food_id}')

def edit_review(request, id):
    # Get mood entry berdasarkan id
    food_id = request.GET.get('id')
    review = Review.objects.get(pk=id)

    # Set mood entry sebagai instance dari form
    form = ReviewForm(request.POST or None, instance=review, initial={'food_id': food_id})

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('review:show_review') + f'?id={food_id}')

    context = {'form': form,
               'id' : food_id}
    return render(request, "edit_review.html", context)

def show_json(request,id):
    data = []
    for i in Review.objects.filter(makanan = id):
        data.append({
            "user": i.user.username,
            "rating" : i.rating,
            "text" : i.text,
            "time_created": i.created_at
        })

    return JsonResponse(data,safe=False)