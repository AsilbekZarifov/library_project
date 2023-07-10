from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializer
# Create your views here.
from rest_framework import generics, status, viewsets


# class BookListApiView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer




class BookListApiView(APIView):
    def get(self,request):
        books = Book.objects.all()
        serializer_data = BookSerializer(books,many=True).data
        data = {
            'status':f"Returned {len(books)} books",
            'books':serializer_data
        }
        return Response(data)


class BookCreateApiView(APIView):
    def post(self,request):
        data = request.data()
        serializer = BookSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {'status':f"Books are saved to the database",
                    'books':data
                    }
        return Response(data)

# class BookDetailApiView(generics.RetrieveAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer



# class BookDeleteApiView(generics.DestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# class BookUpdateApiView(generics.UpdateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


class BookCreateApiView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListCreateApiView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['GET'])
def books_list_view(request,*args,**kwargs):
    books = Book.objects.all()
    serializer = BookSerializer(books,many=True )
    return Response(serializer.data)
class BookDetailApiView(APIView):
    def get(self,request, pk):
        try:
            book = Book.objects.get(id=pk)
            serializer_data = BookSerializer(book).data

            data = {
                "status":"Successful",
                'book':serializer_data
            }
            return Response(data,status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"status":'False',
                 "message":"book in not found"},status=status.HTTP_404_NOT_FOUND
            )


class BookDeleteApiView(APIView):
    def delete(self,request,pk):
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            return Response(
                {"status": 'True',
                 "message": "Successfully Deleted"},status=status.HTTP_200_OK )
        except Exception:
            return Response(
                {"status": 'False',
                 "message": "book in not found"},status=status.HTTP_404_NOT_FOUND)

class BookUpdateApiView(APIView):
    def put(self,request,pk):
        book = get_object_or_404(Book.objects.all(), id=pk)
        data = request.data
        serializer = BookSerializer(instance=book,data=data,partial=True)
        if serializer.is_valid(raise_exception=True):
            book_saved = serializer.save()
        return Response(
            {"status": 'True',
             "message": "Successfully Updated"})

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    #CRUD uchun juda foydali Create,Read,Update,Delete

