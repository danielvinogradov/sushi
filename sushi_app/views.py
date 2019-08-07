from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.views.decorators.vary import vary_on_headers
from django.urls import reverse, reverse_lazy
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from wagtail.admin.utils import user_passes_test, permission_denied, PermissionPolicyChecker
from wagtail.users.forms import AvatarPreferencesForm
import wagtail.users.models
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.utils.encoding import force_text
from wagtail.admin.forms.search import SearchForm
from wagtail.core.models import Collection
from wagtail.documents.forms import get_document_form
from wagtail.documents.permissions import permission_policy
from mickroservices.models import DocumentSushi
from wagtail.documents.models import get_document_model

User = get_user_model()


class SushiShopDocListView(ListView):
    model = DocumentSushi
    paginate_by = 9
    context_object_name = "documents"
    template_name = "store.html"

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def get_documents(self):
        shop = Shop.objects.get(id=self.kwargs["shop_id"])
        documents = shop.docs
        documents = documents.order_by("title")
        return documents

    def get_invoices(self):
        shop = Shop.objects.get(id=self.kwargs["shop_id"])
        invoices = shop.checks
        invoices = invoices.order_by("title")
        return invoices

    def get_queryset(self):
        # Get documents (filtered by user permission)
        documents = self.get_documents()
        invoices = self.get_invoices()
        # Ordering

        ordering = None
        if "ordering" in self.request.GET and self.request.GET["ordering"] in [
            "title",
            "-created_at",
            "file_size",
        ]:
            ordering = self.request.GET["ordering"]
        else:
            ordering = "title"

        documents = documents.order_by(ordering)
        # Search
        query_string = None
        if "q" in self.request.GET:
            form = SearchForm(self.request.GET, placeholder="Search documents")
            if form.is_valid():
                query_string = form.cleaned_data["q"]
                documents = documents.search(query_string)

        return documents

    def get(self, request, *args, **kwargs):
        collections = permission_policy.collections_user_has_any_permission_for(
            request.user, ["add", "change"]
        )
        if len(collections) < 2:
            collections = None
        else:
            collections = Collection.order_for_display(collections)

        # Create response
        return super().get(request, *args, **kwargs)

    @vary_on_headers("X-Requested-With")
    def post(self, request, *args, **kwargs):

        DocumentForm = get_document_form(self.model)
        if not request.is_ajax():
            return HttpResponseBadRequest("Cannot POST to this view without AJAX")

        if not request.FILES:
            return HttpResponseBadRequest("Must upload a file")

        # Build a form for validation
        form = DocumentForm(
            {
                "title": request.FILES["file"].name,
                "collection": request.POST.get("collection"),
            },
            {"file": request.FILES["file"]},
            user=request.user,
        )

        if form.is_valid():
            # Save it
            doc = form.save(commit=False)

            doc.doc_type = self.doc_type
            doc.uploaded_by_user = request.user
            doc.file_size = doc.file.size

            # Set new document file hash
            doc.file.seek(0)
            doc._set_file_hash(doc.file.read())
            doc.file.seek(0)
            doc.save()
            shop = Shop.objects.get(id=self.kwargs["shop_id"])

            if request.POST.get("type") == "doc":
                shop.docs.add(doc)
            elif request.POST.get("type") == "invoice":
                shop.checks.add(doc)

            collections = permission_policy.collections_user_has_any_permission_for(
                request.user, ["add", "change"]
            )
            if len(collections) < 2:
                collections = None
            else:
                collections = Collection.order_for_display(collections)

            return JsonResponse(
                {
                    "success": True,
                    "documents": [
                        {"title": obj.title, "file_size": obj.file_size}
                        for obj in self.get_documents()
                    ],
                    "invoices": [
                        {"title": obj.title, "file_size": obj.file_size}
                        for obj in self.get_invoices()
                    ],
                    "collections": collections,
                    "doc_id": int(doc.id),
                }
            )
        else:
            # Validation error
            return JsonResponse(
                {
                    "success": False,
                    # https://github.com/django/django/blob/stable/1.6.x/django/forms/util.py#L45
                    "error_message": "\n".join(
                        [
                            "\n".join([force_text(i) for i in v])
                            for k, v in form.errors.items()
                        ]
                    ),
                }
            )


class ShopListView(SushiShopDocListView):
    doc_type = DocumentSushi.T_TEH_CARD

    def get_context_data(self, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["shop_id"])
        context = super().get_context_data(**kwargs)
        context["invoices"] = self.get_invoices()
        context["shop"] = shop
        context["breadcrumb"] = [
            {"title": "Личный кабинет", "url": reverse_lazy("partner_lk")},
            {"title": f"Магазин #{shop.id}"},
        ]

        return context


# # Create your views here
def manager_check(user):
    return user.user_profile.is_manager


def partner_check(user):
    return user.user_profile.is_partner


@login_required
def base(request):
    employee_list = UserProfile.objects.prefetch_related(
        "user", "wagtail_profile", "department"
    ).filter(head=request.user.user_profile)
    return render(request, "index.html", {"employee_list": employee_list})


@login_required
def employee_info(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "employee.html", {"employee": user})


@login_required
@user_passes_test(manager_check)
def manager_lk_view(request):
    partner_list = UserProfile.objects.prefetch_related(
        "user", "wagtail_profile"
    ).filter(manager=request.user.user_profile)
    request_list = Requests.objects.prefetch_related("responsible").filter(
        manager=request.user.user_profile
    )
    task_list = Task.objects.prefetch_related("responsible").filter(
        manager=request.user.user_profile
    )
    feedback_list = Feedback.objects.prefetch_related("responsible", "shop").filter(
        manager=request.user.user_profile
    )
    return render(
        request,
        "dashboard_manager.html",
        {
            "partner_list": partner_list,
            "request_list": request_list,
            "task_list": task_list,
            "feedback_list": feedback_list,
            "breadcrumb": [{"title": "Личный кабинет"}],
        },
    )


@login_required
@user_passes_test(partner_check)
def partner_lk_view(request):
    shop_list = Shop.objects.prefetch_related("checks", "docs").filter(
        partner=request.user.user_profile
    )
    request_list = Requests.objects.prefetch_related("responsible").filter(
        responsible=request.user
    )
    task_list = Task.objects.prefetch_related("responsible").filter(
        responsible=request.user
    )
    feedback_list = Feedback.objects.prefetch_related("responsible", "shop").filter(
        responsible=request.user.user_profile
    )
    return render(
        request,
        "dashboard_partner.html",
        {
            "shop_list": shop_list,
            "request_list": request_list,
            "task_list": task_list,
            "feedback_list": feedback_list,
            "breadcrumb": [{"title": "Личный кабинет"}],
            "manager": request.user.user_profile.manager,
        },
    )


@login_required
@user_passes_test(partner_check)
def form_request_view(request):
    form = RequestsForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = request.user
        form.manager = request.user.user_profile.manager
        form.save()
        return HttpResponseRedirect(reverse_lazy("partner_lk"))
    return render(
        request,
        "request_new.html",
        {
            "manager": request.user.user_profile.manager,
            "form": form,
            "breadcrumb": [
                {"title": "Личный кабинет", "url": reverse_lazy("partner_lk")},
                {"title": "Добавить запрос"},
            ],
        },
    )


@login_required
@user_passes_test(manager_check)
def form_task_view(request, partner_id):
    partner = get_object_or_404(UserProfile, id=partner_id)
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = partner.user
        form.manager = request.user.user_profile
        form.save()
        return HttpResponseRedirect(reverse_lazy("manager_lk"))
    return render(
        request,
        "task_new.html",
        {
            "partner": partner,
            "form": form,
            "breadcrumb": [
                {
                    "title": partner.user.get_full_name,
                    "url": reverse("employee_info", args=[partner.user.id]),
                },
                {"title": "Добавить задачу"},
            ],
        },
    )


@login_required
@user_passes_test(manager_check)
def feedback_form_view(request):
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = form.shop.partner.user_profile
        form.manager = request.user.user_profile
        form.save()
        return HttpResponseRedirect(reverse_lazy("manager_lk"))
    context = {
        "form": form,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить отзыв"},
        ],
    }
    return render(request, "review_new.html", context)


@login_required
@user_passes_test(manager_check)
def create_partner_view(request):
    form_user = RegistrationEmployeeMainForm(
        request.POST or None, request.FILES or None, prefix="user"
    )
    form_user_profile = RegistrationEmployeeAdditionForm(
        request.POST or None, request.FILES or None, prefix="user_profile"
    )
    if form_user.is_valid() and form_user_profile.is_valid():
        form_user = form_user.save(commit=False)
        form_user.save()
        wagtail_user = wagtail.users.models.UserProfile.get_for_user(form_user)
        wagtail_user.avatar = form_user_profile.cleaned_data["avatar"]
        wagtail_user.preferred_language = settings.LANGUAGE_CODE
        wagtail_user.current_time_zone = settings.TIME_ZONE
        wagtail_user.save()
        form_user_profile = form_user_profile.save(commit=False)
        form_user_profile.user = form_user
        form_user_profile.wagtail_profile = wagtail_user
        form_user_profile.manager = request.user.user_profile
        form_user_profile.is_partner = True
        form_user_profile.save()
        return HttpResponseRedirect(reverse("manager_lk"))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить франчайзи"},
        ],
    }
    return render(request, "user_new.html", context)


@login_required
@user_passes_test(manager_check)
def edit_partner_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form_user = EditEmployeeMainForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user),
        instance=user,
        prefix="user",
    )
    form_user_profile = EditEmployeeAdditionForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.user_profile),
        instance=user.user_profile,
        prefix="user_profile",
    )
    form_wagtail = AvatarPreferencesForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.wagtail_userprofile),
        instance=user.wagtail_userprofile,
        prefix="user_profile",
    )
    if (
        form_user.is_valid()
        and form_user_profile.is_valid()
        and form_wagtail.is_valid()
    ):
        form_user.save()
        form_user_profile.save()
        form_wagtail.save()
        return HttpResponseRedirect(reverse("employee_info", args=[user_id]))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "form_wagtail": form_wagtail,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Редактировать франчайзи"},
        ],
    }
    return render(request, "user_edit.html", context)


@login_required
@user_passes_test(manager_check)
def shop_form_view(request):
    form = ShopForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy("manager_lk"))
    context = {
        "form": form,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить магазин"},
        ],
    }
    return render(request, "store_new.html", context)


# @login_required
# def shop_view(request, shop_id):
#     shop = get_object_or_404(Shop, id=shop_id)
#     return render(request, 'store.html', {'shop': shop,
#                                           'breadcrumb': [{'title': 'Личный кабинет',
#                                                           'url': reverse_lazy('partner_lk')},
#                                                          {'title': f"Магазин #{shop.id}"}]})


@login_required
def task_view(request, task_id, user_id):
    task = get_object_or_404(Task, id=task_id)
    if task.responsible != request.user:
        if task.manager != request.user.user_profile:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_status = StatusTaskForm(
        request.POST or None, initial=model_to_dict(task), instance=task
    )
    if request.user.user_profile.is_manager:
        if form_status.is_valid():
            form_status.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    qs1 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        task=task, from_user=request.user.id
    )
    qs2 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        task=task, to_user=request.user.id
    )
    messeges = qs1.union(qs2).order_by("date_create")
    form = MessegesForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.task = task
        form.from_user = request.user
        if request.user == task.responsible:
            form.to_user = task.manager.user
        else:
            form.to_user = task.responsible
        form.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(
        request,
        "task.html",
        {
            "task": task,
            "messeges": messeges,
            "form": form,
            "form_status": form_status,
            "breadcrumb": [
                {
                    "title": "Личный кабинет",
                    "url": reverse_lazy("partner_lk")
                    if request.user.user_profile.is_partner
                    else reverse_lazy("manager_lk"),
                },
                {"title": f"Задача #{task.id}"},
            ],
        },
    )


@login_required
def requests_view(request, requests_id, user_id):
    requests = get_object_or_404(Requests, id=requests_id)
    if requests.responsible != request.user:
        if requests.manager != request.user.user_profile:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_status = StatusRequestsForm(
        request.POST or None, initial=model_to_dict(requests), instance=requests
    )
    if request.user.user_profile.is_manager:
        if form_status.is_valid():
            form_status.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    qs1 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        requests=requests, from_user=request.user.id
    )
    qs2 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        requests=requests, to_user=request.user.id
    )
    messeges = qs1.union(qs2).order_by("date_create")
    form = MessegesForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.requests = requests
        form.from_user = request.user
        if request.user == requests.responsible:
            form.to_user = requests.manager.user
        else:
            form.to_user = requests.responsible
        form.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(
        request,
        "request.html",
        {
            "requests": requests,
            "messeges": messeges,
            "form": form,
            "form_status": form_status,
            "breadcrumb": [
                {
                    "title": "Личный кабинет",
                    "url": reverse_lazy("partner_lk")
                    if request.user.user_profile.is_partner
                    else reverse_lazy("manager_lk"),
                },
                {"title": f"Запрос #{requests.id}"},
            ],
        },
    )


@login_required
def feedback_view(request, feedback_id, user_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if feedback.responsible != request.user:
        if feedback.manager != request.user.user_profile:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_status = StatusFeedbackForm(
        request.POST or None, initial=model_to_dict(feedback), instance=feedback
    )
    if request.user.user_profile.is_manager:
        if form_status.is_valid():
            form_status.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    qs1 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        feedback=feedback, from_user=request.user.id
    )
    qs2 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        feedback=feedback, to_user=request.user.id
    )
    messeges = qs1.union(qs2).order_by("date_create")
    form = MessegesForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.feedback = feedback
        form.from_user = request.user
        if request.user == feedback.responsible.user:
            form.to_user = feedback.manager.user
        else:
            form.to_user = feedback.responsible.user
        form.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(
        request,
        "review.html",
        {
            "feedback": feedback,
            "messeges": messeges,
            "form": form,
            "form_status": form_status,
            "breadcrumb": [
                {
                    "title": "Личный кабинет",
                    "url": reverse_lazy("partner_lk")
                    if request.user.user_profile.is_partner
                    else reverse_lazy("manager_lk"),
                },
                {"title": f"Отзыв #{feedback.id}"},
            ],
        },
    )


def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product.html", {"product": product})


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "details.html", {"product": product})

