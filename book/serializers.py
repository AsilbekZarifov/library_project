from rest_framework import serializers
from .models import Book
from rest_framework.exceptions import ValidationError



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model =Book
        fields = ('id', 'title','subtitle','author','isbn','price','content',)

    def validate(self,data):
        title = data.get('title',None)
        author = data.get('author',None)

        #check title if it contains only alpha chars
        if not title.isalpha():
            raise ValidationError(
                {
                    'status':False,
                    'messagee':'Sarlavhasi harfladan tashkil topgan bulishi kerak'
                }
            )
        #check title and author from database existence
        if Book.objects.filter(title=title,author=author).exists():
            raise ValidationError(
                {
                    'status': False,
                    'messagee': 'Title va author bir xil bulgan kitobni yuklay olmaysiz  '
                }
            )

        return data

    def validate_price(self,data):
        if data < 0 or data >999999999:
            raise ValidationError(
                {
                    'status': False,
                    'messagee': "Narx noto'g'ri kiritilgan"
                }
            )
