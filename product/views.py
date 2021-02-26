from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.base import View

from product.forms import CreateProductForm, UpdateProductForm, ImagesFormSet
from product.models import Category, Product, ProductImage


# def homepage(request):
#     categories = Category.objects.all()
#     return render(request, 'product/index.html', {'categories': categories})


# class HomePageView(View):
#     def get(self, request):
#         categories = Category.objects.all()
#         return render(request, 'product/index.html', {'categories': categories})
#

class HomePageView(ListView):
    model = Category
    template_name = 'product/index.html'
    context_object_name = 'categories'


# def products_list(request, category_slug):
#     if not Category.objects.filter(slug=category_slug).exists():
#         raise Http404('Нет такой категории')
#     products = Product.objects.filter(category_id=category_slug)
#     return render(request, 'product/products_list.html', {'products': products})


# class ProductsListView(View):
#     def get(self, request, category_slug):
#         if not Category.objects.filter(slug=category_slug).exists():
#             raise Http404('Нет такой категории')
#         products = Product.objects.filter(category_id=category_slug)
#         return render(request, 'product/products_list.html', {'products': products})

class ProductsListView(ListView):
    model = Product
    template_name = 'product/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if not Category.objects.filter(slug=category_slug).exists():
            raise Http404('Нет такой категории')
        queryset = queryset.filter(category_id=category_slug)
        return queryset

    # def get(self,request, category_slug):
    #     if not Category.objects.filter(slug=category_slug).exists():
    #         raise Http404('Нет такой категории')
    #     products = self.get_queryset().filter(category_id=category_slug)
    #     return render(request, 'product/products_list.html', {'products': products})


class IsAdminCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and \
               (self.request.user.is_staff or self.request.user.is_superuser)


class ProductDetailsView(IsAdminCheckMixin, DetailView):
    model = Product
    template_name = 'product/product_details.html'


class ProductCreateView(IsAdminCheckMixin, View):
    def get(self, request):
        form = CreateProductForm()
        formset = ImagesFormSet(queryset=ProductImage.objects.none())
        return render(request, 'product/create.html', locals())

    def post(self, request):
        form = CreateProductForm(request.POST)
        formset = ImagesFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if form.is_valid() and formset.is_valid():
            product = form.save()
            for form in formset.cleaned_data:
                image = form.get('image')
                if image is not None:
                    pic = ProductImage(product=product, image=image)
                    pic.save()
            return redirect(product.get_absolute_url())
        else:
            print(form.errors, formset.errors)


class ProductEditView(IsAdminCheckMixin, UpdateView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product)
        formset = ImagesFormSet(queryset=product.images.all())
        return render(request, 'product/edit.html', locals())

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product, data=request.POST)
        formset = ImagesFormSet(request.POST, request.FILES, queryset=product.images.all())
        if form.is_valid() and formset.is_valid():
            product = form.save()
            print(formset.deleted_forms)
            for form in formset.cleaned_data:
                image = form.get('image')
                if image is not None and not ProductImage.objects.filter(product=product, image=image).exists():
                    pic = ProductImage(product=product, image=image)
                    pic.save()
            for form in formset.deleted_forms:
                print(form.cleaned_data)
                image = form.cleaned_data.get('id')
                if image is not None:
                    image.delete()
            return redirect(product.get_absolute_url())
        else:
            print(form.errors, formset.errors)


class ProductDeleteView(IsAdminCheckMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('index-page')

# def product_details(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'product/product_details.html', {'product': product})

# 1 вариант
# products/category
# def products_list(request, category_slug):
# 1
# # products = Product.objects.all()
# if Category.objects.filter(slug=category_slug).exists()
#     raise  Http404
# products = Product.objects.filter(category_id=category_slug)  # queryset

# 2
# category = get_object_or_404(Category, slug=category_slug)
# products= Product.objects.filter(category=category)

# 3
# products = get_list_or_404(Product, category_id=category_slug)
# return render(request, 'product/products_list.html', {'products': products})


# all() - выводит все объекты модели
# select * all from table;


# filter() - фильтрует результат QuerySet.
# select * from table where ...;


# exclude(условие) - исключает из результатов объекты, отвечающие условию;
# select * from table Where category != 1;
# exclude(title__startswith='Apple')
# select * from Product Where title not like 'Apple'


# order_by() - сортировка резултатов запроса
# Product.objects.order_by('price');
# Select * from product ORDER_BY price ASC;
# Product.objects.order_by('-price');
# Select * from product ORDER_BY price DESC;

# Product.object.order_by('price', 'popularity')
# SELECT * FROM product ORDER BY price ASC, popularity ASC;

# Product.objects.order_by('?') произвольная сортировка или же рандомная сортировка

# Product.object.all().reverse()

# Distinct() исключает повторения
# Product.objects.values('category' flat=True).distinct()


# Product.object.values(можно передавать нужные поля или же все) -> вернет список из словарей


# Product.object.values_list(можно передавать нужные поля или же все) -> вернет список из tuple

# none() - пустой QuerySet()

# select_related()
# product = Product.objects.get(id=1)
# product.category - запрос в БД

# product =Product.objects.select_related('category').get(id=1)
# product.category - запрос в БД нет

# prefetch_related()
# categories = Category.objects.filter(...)
# for cat in categories:
#     cat.product_set.all()
#
#
# categories = Category.objects.prefetch_related('products').filter(...)


# defer(указанное поле)
# Category.objects.(указанное поле) - вернет все кроме указзаных полей

# only(указзаное поле)
# Category.objects.only(указзаное поле) - вернет только указзаные поля

# get(id) возвращает объект
# Product.objects.get(id=1) -> возвращает один объект

# Если нет объекта по условию:
# Product.objects.get(1d=100) -> Product.DoesNotExist

# Если get находит несоклько объектов:
# ошибка Product.MultipleObjectsReturned


# create() - создает объекты

# get_or_create(условие) - выбирает объект, отвечающий условию, если объекта нет то создает

# explain() - Возвращает Sql запрос queryset


# Основные lookup Field
# числовые
# gt -> '>'
# lt -> '<'
# lte -> '<='
# gte -> '>='
# = -> '='


# текстовые числовые
# startswith 'A' -> LIKE 'A%'
# istartswith 'A'-> ILIKE 'A%'
# endswith 'A'-> LIKE '%A'
# iendswith 'A'-> ILIKE '%A'
# contains 'A'-> LIKE '%A%'
# icontains 'A'-> ILIKE '%A%'
# title__exact='Milk' -> WHERE title like 'Milk'
# title__iexact='Milk' -> WHERE title ilike= 'Milk'
# category__isnull=True - > WHERE category is null:
# category__isnull=False - > WHERE category is null:
# id__in = [1, 2, 3, 4, ] -> WHERE id IN (1,2,3,4)
# range=(start,end) -> WHERE date BETWEEN start and end;


# Проекты против приложений
#
# В чем разница между проектом и приложением? Приложение - это
# веб-приложение, которое что-то делает, например, система веб-журнала,
# база данных публичных записей или небольшое приложение для опросов.
# Проект - это набор конфигураций и приложений для определенного веб-сайта.
# Проект может содержать несколько приложений. Приложение может
# быть в нескольких проектах.
