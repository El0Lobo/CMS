# app/pos/views.py
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.db import transaction, models as djmodels
from django.utils import timezone

from app.menu.models import Item, ItemVariant  # your real models
from .models import POSQuickButton, DiscountReason, Sale, SaleItem, Payment


# === Config ===
TAX_RATE_DEFAULT = Decimal("19.00")  # 19% VAT default


# === Money helpers ===
def _money(v):
    return Decimal(v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# === Cart session helpers ===
def _get_cart(req):
    """
    Cart structure in session:
    {
      "lines": [
        {"id": variant_id, "title": "...", "qty": 1, "unit_price": "4.20",
         "discount": {"type": "PERCENT|AMOUNT|FREE", "value": "10.00"} or None,
         "tax_rate": "19.00",
         "calc_subtotal": "…", "calc_discount": "…", "calc_tax": "…", "calc_total": "…"}
      ],
      "order_discount": {"type": "...", "value": "...", "reason_id": 1} or None,
      "totals": {"subtotal": "...", "discount_total": "...", "tax_total": "...", "grand_total": "..."}
    }
    """
    return req.session.get("pos_cart", {"lines": [], "order_discount": None})


def _save_cart(req, cart):
    req.session["pos_cart"] = cart
    req.session.modified = True


def _reprice_cart(cart: dict) -> dict:
    subtotal = Decimal("0.00")
    discount_total = Decimal("0.00")
    tax_total = Decimal("0.00")
    grand_total = Decimal("0.00")

    lines = cart.get("lines", [])
    for line in lines:
        qty = int(line.get("qty", 0))
        unit = _money(line.get("unit_price", "0.00"))
        line_sub = _money(unit * qty)

        # per-line discount
        line_disc = Decimal("0.00")
        d = line.get("discount")
        if d:
            dtype = d.get("type")
            dval = _money(d.get("value", "0"))
            if dtype == "FREE":
                line_disc = line_sub
            elif dtype == "PERCENT":
                line_disc = (line_sub * dval / Decimal("100")).quantize(Decimal("0.01"))
            elif dtype == "AMOUNT":
                line_disc = min(dval, line_sub)

        line_after_disc = _money(line_sub - line_disc)

        tax_rate = _money(line.get("tax_rate", TAX_RATE_DEFAULT))
        line_tax = (line_after_disc * tax_rate / Decimal("100")).quantize(Decimal("0.01"))
        line_total = _money(line_after_disc + line_tax)

        line["calc_subtotal"] = str(_money(line_sub))
        line["calc_discount"] = str(_money(line_disc))
        line["calc_tax"] = str(_money(line_tax))
        line["calc_total"] = str(_money(line_total))

        subtotal += line_sub
        discount_total += line_disc
        tax_total += line_tax
        grand_total += line_total

    # order-level discount
    order_disc_amount = Decimal("0.00")
    od = cart.get("order_discount")
    if od:
        base = _money(subtotal - discount_total)
        dtype = od.get("type")
        dval = _money(od.get("value", "0"))
        if dtype == "FREE":
            order_disc_amount = base
        elif dtype == "PERCENT":
            order_disc_amount = (base * dval / Decimal("100")).quantize(Decimal("0.01"))
        elif dtype == "AMOUNT":
            order_disc_amount = min(dval, base)

        # naive proportional tax reduction to reflect order discount
        if base > 0:
            fraction = (base - order_disc_amount) / base
            tax_total = (tax_total * fraction).quantize(Decimal("0.01"))
            grand_total = _money((base - order_disc_amount) + tax_total)
        else:
            tax_total = Decimal("0.00")
            grand_total = Decimal("0.00")

        discount_total += order_disc_amount

    cart["totals"] = {
        "subtotal": str(_money(subtotal)),
        "discount_total": str(_money(discount_total)),
        "tax_total": str(_money(tax_total)),
        "grand_total": str(_money(grand_total)),
    }
    return cart


def _variant_display_title(variant: ItemVariant) -> str:
    """
    "{Item.name} — {label or '<qty> <unit>'}"
    """
    base = variant.item.name
    if variant.label:
        tail = variant.label
    else:
        # e.g. "0.3 L"
        q = f"{variant.quantity.normalize():g}" if hasattr(variant.quantity, "normalize") else str(variant.quantity)
        tail = f"{q} {variant.unit.code}"
    return f"{base} — {tail}"


# === Views ===
@method_decorator([login_required], name="dispatch")
class IndexView(View):
    template_name = "pos/index.html"

    def get(self, request):
        cart = _reprice_cart(_get_cart(request))
        return render(request, self.template_name, {"cart": cart})


@login_required
def api_search_items(request):
    q = request.GET.get("q", "").strip()

    qs = ItemVariant.objects.select_related("item", "unit", "item__category")
    # Only public items
    qs = qs.filter(item__visible_public=True)

    if q:
        qs = qs.filter(
            djmodels.Q(item__name__icontains=q) |
            djmodels.Q(label__icontains=q)
        )

    results = []
    for v in qs.order_by("item__name", "label")[:60]:
        # filter out sold-out parent items (your Item method)
        if v.item.is_sold_out():
            continue
        results.append({
            "id": v.id,  # variant pk
            "title": _variant_display_title(v),
            "price": str(_money(v.price)),
        })

    return JsonResponse({"results": results})


@login_required
@require_POST
def api_cart_add(request):
    var_id = request.POST.get("id")
    qty = int(request.POST.get("qty", "1"))
    if not var_id or qty < 1:
        return HttpResponseBadRequest("Invalid parameters")

    try:
        v = ItemVariant.objects.select_related("item", "unit").get(pk=var_id)
    except ItemVariant.DoesNotExist:
        return HttpResponseBadRequest("Variant not found")

    title = _variant_display_title(v)
    unit_price = _money(v.price)

    cart = _get_cart(request)
    # bump if present, else append
    for line in cart["lines"]:
        if str(line["id"]) == str(v.id):
            line["qty"] = int(line["qty"]) + qty
            break
    else:
        cart["lines"].append({
            "id": v.id,
            "title": title,
            "qty": qty,
            "unit_price": str(unit_price),
            "discount": None,
            "tax_rate": str(TAX_RATE_DEFAULT),
        })

    _reprice_cart(cart)
    _save_cart(request, cart)
    return JsonResponse(cart)


@login_required
@require_POST
def api_cart_remove(request):
    item_id = request.POST.get("id")
    if not item_id:
        return HttpResponseBadRequest("Missing id")
    cart = _get_cart(request)
    cart["lines"] = [l for l in cart["lines"] if str(l["id"]) != str(item_id)]
    _reprice_cart(cart)
    _save_cart(request, cart)
    return JsonResponse(cart)


@login_required
@require_POST
def api_cart_update(request):
    item_id = request.POST.get("id")
    qty = int(request.POST.get("qty", "1"))
    if not item_id or qty < 0:
        return HttpResponseBadRequest("Invalid parameters")
    cart = _get_cart(request)
    for l in list(cart["lines"]):
        if str(l["id"]) == str(item_id):
            if qty == 0:
                cart["lines"].remove(l)
            else:
                l["qty"] = qty
            break
    _reprice_cart(cart)
    _save_cart(request, cart)
    return JsonResponse(cart)


@login_required
@require_POST
def api_cart_clear(request):
    cart = {"lines": [], "order_discount": None}
    _reprice_cart(cart)
    _save_cart(request, cart)
    return JsonResponse(cart)


@login_required
def api_quick_buttons(request):
    btns = POSQuickButton.objects.filter(is_active=True).order_by("sort_order")
    data = [{
        "id": b.id,
        "label": b.label,
        "type": b.discount_type,
        "value": str(_money(b.value)),
        "scope": b.scope,
        "reason_id": b.reason_id,
    } for b in btns]
    return JsonResponse({"buttons": data})


@login_required
@require_POST
def api_cart_apply_discount(request):
    scope = request.POST.get("scope")  # ORDER or ITEM
    dtype = request.POST.get("type")   # PERCENT/AMOUNT/FREE
    value = request.POST.get("value", "0")
    reason_id = request.POST.get("reason_id")
    item_id = request.POST.get("item_id")

    if scope not in ("ORDER", "ITEM") or dtype not in ("PERCENT", "AMOUNT", "FREE"):
        return HttpResponseBadRequest("Invalid discount")

    cart = _get_cart(request)
    if scope == "ORDER":
        cart["order_discount"] = {
            "type": dtype,
            "value": value,
            "reason_id": int(reason_id) if reason_id else None,
        }
    else:
        if not item_id:
            return HttpResponseBadRequest("Missing item_id for item discount")
        for l in cart["lines"]:
            if str(l["id"]) == str(item_id):
                l["discount"] = {"type": dtype, "value": value}
                break

    _reprice_cart(cart)
    _save_cart(request, cart)
    return JsonResponse(cart)


@login_required
def api_cart_totals(request):
    cart = _reprice_cart(_get_cart(request))
    return JsonResponse(cart)


@login_required
@require_POST
@transaction.atomic
def api_checkout(request):
    """
    MVP: one payment per sale.
    POST body expects:
      - kind: CASH|CARD|OTHER
      - amount: "12.34"
      - note: optional
    """
    cart = _reprice_cart(_get_cart(request))
    if not cart["lines"]:
        return HttpResponseBadRequest("Cart is empty")

    p_kind = request.POST.get("kind", "CASH")
    p_amount = request.POST.get("amount")
    if not p_amount:
        return HttpResponseBadRequest("Missing payment amount")

    sale = Sale.objects.create(
        opened_by=request.user,
        status=Sale.STATUS_PAID,
        order_discount_type=(cart["order_discount"]["type"] if cart.get("order_discount") else None),
        order_discount_value=_money(cart["order_discount"]["value"]) if cart.get("order_discount") else Decimal("0.00"),
        order_discount_reason_id=(cart["order_discount"]["reason_id"] if cart.get("order_discount") else None),
        subtotal=_money(cart["totals"]["subtotal"]),
        discount_total=_money(cart["totals"]["discount_total"]),
        tax_total=_money(cart["totals"]["tax_total"]),
        grand_total=_money(cart["totals"]["grand_total"]),
        note=request.POST.get("note", ""),
        closed_by=request.user,
        closed_at=timezone.now(),
    )

    for l in cart["lines"]:
        SaleItem.objects.create(
            sale=sale,
            menu_variant_id=int(l["id"]),  # FK to ItemVariant
            title_snapshot=l["title"],
            quantity=int(l["qty"]),
            unit_price=_money(l["unit_price"]),
            discount_type=(l["discount"]["type"] if l.get("discount") else None),
            discount_value=_money(l["discount"]["value"]) if l.get("discount") else Decimal("0.00"),
            tax_rate=_money(l.get("tax_rate", TAX_RATE_DEFAULT)),
            tax_amount=_money(l["calc_tax"]),
            line_subtotal=_money(l["calc_subtotal"]),
            line_discount=_money(l["calc_discount"]),
            line_total=_money(l["calc_total"]),
        )

    Payment.objects.create(
        sale=sale, kind=p_kind, amount=_money(p_amount), received_by=request.user
    )

    # clear cart
    _save_cart(request, {"lines": [], "order_discount": None})
    return JsonResponse({"ok": True, "sale_id": sale.id})

# app/pos/views.py (NEW)
@login_required
def api_browse_items(request):
    """
    Returns categories with visible, not-sold-out variants:
    {
    "categories": [
        {"id": 3, "name": "Cocktails", "items": [{"id": 12, "title": "...", "price": "8.50"}, ...]},
        ...
    ]
    }
    """
    qs = ItemVariant.objects.select_related("item", "unit", "item__category") \
                            .filter(item__visible_public=True) \
                            .order_by("item__category__name", "item__name", "label")

    cats = {}  # cat_id -> {id, name, items: []}
    for v in qs:
        if v.item.is_sold_out():
            continue
        cat = v.item.category
        if not cat:
            continue
        cid = cat.id
        if cid not in cats:
            cats[cid] = {"id": cid, "name": cat.name, "items": []}
        cats[cid]["items"].append({
            "id": v.id,
            "title": _variant_display_title(v),
            "price": str(_money(v.price)),
        })

    # Only keep categories that actually have items
    categories = [c for c in cats.values() if c["items"]]
    # Sort by name
    categories.sort(key=lambda c: c["name"].lower())
    return JsonResponse({"categories": categories})
