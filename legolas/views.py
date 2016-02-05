from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Store, Review, Comment
from accounts.models import UserProfile
from .forms import StoreForm, ReviewForm, CommentForm

from django.contrib.auth.models import User


def index(request):
    stores_per_cateogry = 5
    food_stores = Store.objects.all().filter(categories__pk=1).order_by('-store_rating')[ :stores_per_cateogry]
    drink_stores = Store.objects.all().filter(categories__pk=2).order_by('-store_rating')[ :stores_per_cateogry]
    shopping_stores = Store.objects.all().filter(categories__pk=3).order_by('-store_rating')[ :stores_per_cateogry]
    entertain_stores = Store.objects.all().filter(categories__pk=4).order_by('-store_rating')[ :stores_per_cateogry]
    culture_stores = Store.objects.all().filter(categories__pk=5).order_by('-store_rating')[ :stores_per_cateogry]
    beauty_stores = Store.objects.all().filter(categories__pk=6).order_by('-store_rating')[ :stores_per_cateogry]

    reviews_per_scrolling = 5
    recent_reviews = Review.objects.all().order_by('-created_at')[ :reviews_per_scrolling]

    context = {
        'food_stores': food_stores,
        'drink_stores': drink_stores,
        'shopping_stores': shopping_stores,
        'entertain_stores': entertain_stores,
        'culture_stores': culture_stores,
        'beauty_stores': beauty_stores,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'legolas/index.html', context)


'''
def store_list(request , pk):
    ## 이거 대신에paginator를 아래에서 이용.

    per_page = 10
    start_pos = (int(pk) - 1) * per_page
    end_pos = start_pos + per_page
    store_list = Store.objects.all().order_by('-store_rating')[start_pos:end_pos]

    return render(request, 'legolas/store_list.html', {'store_list': store_list})
'''

def store_list(request):

    query_sort = request.GET.get('sortby')

    print(query_sort)

    if query_sort == 'n_reivew':
        store_list = Store.objects.all().order_by('-n_reivew')
    else:
        store_list = Store.objects.all().order_by('-store_rating')


    ## 검색파트
    query_where = request.GET.get('where')
    query_what = request.GET.get('what')

    if query_where and query_what:
        store_list = store_list.filter(
            (Q(area__name__contains=query_where) |
            Q(sub_area__name__contains=query_where)) &
            (Q(intro__contains=query_what) |
            Q(menu__contains=query_what) |
            Q(categories__name__contains=query_what) |
            Q(sub_categories__name__contains=query_what))
        ).distinct()
    elif query_where and not query_what:
        store_list = store_list.filter(
            (Q(area__name__contains=query_where) |
            Q(sub_area__name__contains=query_where))
        ).distinct()
    elif not query_where and query_what:
        store_list = store_list.filter(
            Q(intro__contains=query_what) |
            Q(menu__contains=query_what) |
            Q(categories__name__contains=query_what) |
            Q(sub_categories__name__contains=query_what)
        ).distinct()
    else:
        pass

    # 페이지네이션 파트
    paginator = Paginator(store_list, 10)
    page = request.GET.get('page')

    try:
        stores = paginator.page(page)
    except PageNotAnInteger:
        stores = paginator.page(1)
    except EmptyPage:
        stores = paginator.page(paginator.num_pages)

    context = {
        'stores':stores,
        'query_sort': query_sort,
    }

    return render(request, 'legolas/store_list.html', context)


def store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk)
    reviews = store.review_set.all().order_by('-created_at')

    return render(request, 'legolas/store_detail.html', {'store':store, 'reviews':reviews, 'review_form':ReviewForm, 'comment_form':CommentForm})


def store_menu(request, pk):
    store = get_object_or_404(User, pk=pk)
    return render(request, 'legolas/store_menu.html', {'store': store})


def store_new(request):
    if (request.method == "POST"):
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save()
            return redirect(store_detail, pk=store.pk)
    else:
        form = StoreForm()
    return render(request, 'legolas/store_form.html', {'form': form})


def store_edit(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if (request.method == "POST"):
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            store = form.save()
            return redirect(store_detail, pk=store.pk)
    else:
        form = StoreForm(instance=store)
    return render(request, 'legolas/store_form.html', {'form': form})


@login_required
def review_new(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    if (request.method == "POST"):
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.store = store
            review.author = request.user
            review.created_at = timezone.now()
            review.save()
            old_n_review = store.n_review
            store.n_review += 1
            store.store_rating = (store.store_rating*old_n_review + review.user_rating)/store.n_review
            store.save()
            return redirect(store_detail, pk=store_id)
    else:
        form = ReviewForm()
    return render(request, 'legolas/review_form.html', {'form': form, 'store':store})


@login_required
def review_edit(request, store_id, review_id):
    store = get_object_or_404(Store, pk=store_id)
    review = get_object_or_404(Review, pk=review_id)

    if review.author != request.user:
        return HttpResponseForbidden()

    old_rating = review.user_rating
    if (request.method == "POST"):
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.store = store
            review.author = request.user
            review.save()
            store.store_rating = (store.store_rating*store.n_review - old_rating + review.user_rating)/store.n_review
            store.save()
            return redirect(store_detail, pk=store_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'legolas/store_detail.html', {'form': form, 'store':store})


@login_required
def comment_new(request, store_id, review_id):
    store = get_object_or_404(Store, pk=store_id)
    review = get_object_or_404(Review, pk=review_id)

    if (request.method == "POST"):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.review = review
            comment.save()
            messages.success(request, '새 Comment 등록')
            return redirect(store_detail, pk=store.pk)
    else:
        form = CommentForm()
    return render(request, 'legolas/store_detail.html', {'store':store, 'reviews':reviews, 'form':form})



