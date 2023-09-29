from django.shortcuts import render
from rest_framework import generics

from Bee.Line.models import Product
from Bee.Line.serializers import ListProduct
from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, UserModel
from .serializers import ProductSerializer, LessonSerializer, ListProduct


def index(request):
    return HttpResponse('Hello!', 200)

@api_view(['GET', 'POST'])
def list_all_products(request):
	if request.method == 'POST':
		try:
			user_id = request.data['ID_U']
			user = UserModel.objects.get(id=user_id)
			products = Product.objects.filter(acc__user_id=user.id, acc__value=True)
			products = ProductSerializer(products, many=True, context={'request': request})
			return Response(products.data, status=status.HTTP_200_OK)
		except KeyError:
			return Response(
				{'error': 'Идентификатор пользователя'},
				status=status.HTTP_401_UNAUTHORIZED
			)
		except UserModel.DoesNotExist:
			return Response(
				{'error': 'Пользователь не существует'},
				status=status.HTTP_404_NOT_FOUND
			)

	data = {
		'error': 'Идентификатор пользователя'
	}
	return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
def items_from_product(request):

	if request.method == 'POST':
		try:
			user_id = request.data['ID_U']
			product_id = request.data['ID_P']
			user = UserModel.objects.get(id=user_id)
			lessons = Product.objects.get(id=product_id, acc__user_id=user.id, acc__value=True).lessons
			lessons = LessonSerializer(lessons, many=True, context={'request': request})
			return Response(lessons.data, status=status.HTTP_200_OK)
		except KeyError:
			return Response(
				{'error': 'ID пользователя и продукта'},
				status=status.HTTP_401_UNAUTHORIZED
			)
		except UserModel.DoesNotExist:
			return Response(
				{'error': 'Пльзователя не существует'},

			)
		except Product.DoesNotExist:
			return Response(
				{'error': 'Продукта не существует'},
				status=status.HTTP_404_NOT_FOUND
			)

	data = {
		'error': 'Отправьте ID пользователя и продукта'
	}
	return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def total(request):

	products = Product.objects.all()
	products = ListProduct(products, many=True)
	return Response(products.data, status.HTTP_200_OK)