from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404

from product.models import Category, Product


def homepage(request):
    categories = Category.objects.all()
    return render(request, 'product/index.html', {'categories': categories})


def products_list(request, category_slug):
    if not Category.objects.filter(slug=category_slug).exists():
        raise Http404('Нет такой категории')
    products = Product.objects.filter(category_id=category_slug)
    return render(request, 'product/products_list.html', {'products': products})


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/product_details.html', {'product': product})


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


# TODO: переписать вьюшки на CBV (Class Based Views)

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
