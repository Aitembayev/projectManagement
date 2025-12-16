from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem


def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def home(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects.all().order_by("-id")
    if q:
        products = products.filter(title__icontains=q)

    return render(request, "home.html", {"products": products, "q": q})


# ✅ FIX: pk, потому что в urls.py product/<int:pk>/
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


def add_to_cart(request, product_id):
    session_key = _get_session_key(request)
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        product=product,
        defaults={"quantity": 1},
    )
    if not created:
        item.quantity += 1
        item.save()

    # ✅ не перекидываем в корзину — возвращаем назад
    back_url = request.META.get("HTTP_REFERER")
    return redirect(back_url if back_url else "shop:home")


def cart(request):
    session_key = _get_session_key(request)
    items = (
        CartItem.objects.select_related("product")
        .filter(session_key=session_key)
        .order_by("-id")
    )
    total = sum(i.get_total_price() for i in items)
    return render(request, "cart.html", {"items": items, "total": total})


def remove_from_cart(request, item_id):
    session_key = _get_session_key(request)
    item = get_object_or_404(CartItem, id=item_id, session_key=session_key)
    item.delete()
    return redirect("shop:cart")


def qty_change(request, item_id, action):
    session_key = _get_session_key(request)
    item = get_object_or_404(CartItem, id=item_id, session_key=session_key)

    if action == "inc":
        item.quantity += 1
        item.save()
    elif action == "dec":
        if item.quantity <= 1:
            item.delete()
        else:
            item.quantity -= 1
            item.save()

    return redirect("shop:cart")
