from django.db.migrations import serializer
from rest_framework import serializers
from .import models
from django.db.models import Sum
import datetime

from .models import Product, LessonModel, ViewsModel, UserModel


class LessonSerializer(serializer.ModelSerializer):
    status=serializer.SerializerMethodField()
    time_view=serializer.SerializerMethodField()
    class Meta:
        model=LessonModel
        columns=['title', 'description', 'link','time_view','duration', 'status']

    def all(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'data'):
            data = request.data
            try:
                view = ViewsModel.objects.get(user_id=data['ID_U'], lesson_id=obj.id)
                duration_coefficient = view.duration.total_seconds() / obj.duration.total_seconds()
                if duration_coefficient > 0.8:
                    return 'Просмотрено'
                else:
                    return 'Не просмотрено'
            except ViewsModel.DoesNotExist:
                return 'Ошибка'
        return 'Ошибка'

    def get_last_seen(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'data'):
            data = request.data
            try:
                view = ViewsModel.objects.get(user_id=data['ID_U'], lesson_id=obj.id)
                if view.date:
                    return view.date
            except ViewsModel.DoesNotExist:
                return 'Нет данных'
        return 'Нет данных'


class ProductSerializer(serializer.ModelSerializer):
    lessons=LessonSerializer(read_only=True, many=True)
    class Meta:
        model=Product
        column=['id','title', 'description','lessons']

class ListProduct(serializer.ModelSerializer):
    duration = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    view = serializers.SerializerMethodField()
    sum = serializers.SerializerMethodField()

    class Meta():
        model=Product
        list_model=['duration','students','view','sum','title']

        def views(self, obj):
            k = 0
            for lesson in obj.lessons.all():
                k += lesson.views.count()
            return k

        def all_benefit(self, obj):
            users = UserModel.objects.count()
            students = obj.access.count()
            try:
                sum_1 = students / users
            except ZeroDivisionError:
                return 0
            return str(sum_1 * 100) + ' %'

        def all_time(self, obj):
            k= 0
            for lesson in obj.lessons.all():
                for v in lesson.vws.all():
                    k+= v.duration.total_seconds()
            return str(datetime.timedelta(seconds=k))



        def students_1(self, obj):
            students = obj.access.count()
            return students

