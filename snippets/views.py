# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import HttpResponse, JsonResponse, Http404
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from snippets.models import Snippet
# from .serializers import SnippetSerializer

# # Create your views here.

# '''
# Function Based Views

# # @csrf_exempt
# @api_view(['GET','POST'])
# def snippet_list(request):
    
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer= SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data)
    
#     elif request.method =='POST':
#         serializer= SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #Note that because we want to be able to POST to this view from clients that won't have a CSRF token we need to mark the view as csrf_exempt. 



# #individual snippet and can be used to retrieve , update and delete the snippet


# # @csrf_exempt
# @api_view(['GET','PUT','DELETE'])
# def snippet_detail(request,pk):
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return JsonResponse(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method =='GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
    
#     elif request.method=='PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)  #request.data can handle incoming json request and other formats as well , so we no longer need to tie our request and responses to a particular given content type
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method=='DELETE':
#         snippet.delete()
#         return HttpResponse(staus=status.HTTP_204_NO_CONTENT)
    
# '''


# #CLASS BASED VIEWS - API_VIEWS
# class SnippetList(APIView):
#     def get(self,request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
    
#     def post(self,request,pk,format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# #similarly we write the case for SnippetDetail
# class SnippetDetail(APIView):

#     #Check for data
#     def get_object(self,pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             return Http404

#     def get(self,request,pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
    
#     def put(self,request,pk,format=None):
#         snippet= self.get_object(pk)

#         serializer = SnippetSerializer(snippet, data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self,request,pk,format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ############################################################################################################################3




#USING MIXINS
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import mixins
# from rest_framework import generics

# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
    
#     queryset = Snippet.objects.all()
#     serializer_class= SnippetSerializer

    
#     def get(self,request, *args, **kwargs):
#         return self.list(request,*args,**kwargs)
#     #for getting all data we use list 
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
#     #for posting ,we use create

# '''
# We are building our view with genericAPIView and adding listModelMixin and CreateModelMixin, we can do is similarly for SnippetDetail
# '''


# class SnippetDetail(mixins.RetrieveModelMixin, 
#                     mixins.UpdateModelMixin, 
#                     mixins.DestroyModelMixin, 
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class=SnippetSerializer

#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request, *args,**kwargs)
    
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
    
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request, *args,**kwargs)
    
# '''
# Pretty similar. Again we're using the GenericAPIView class to provide the core functionality, and adding in mixins to provide the .retrieve(), .update() and .destroy() actions
# '''


############################################################################################################################

#Using generic class-based views

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer , UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import viewsets

#end point for root of api
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users':reverse('user-list', request=request, format=format),
        'snippets':reverse('snippet-list', request=request, format=format)
    })

# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes=[permissions.IsAuthenticatedOrReadOnly]

#     #adding user to the snippet by overriding perform_create method
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

#     #the create() method of our serializer will now be passed as additional 'owner' field, along with the validated data from the request

# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class= SnippetSerializer
#     permission_classes=[permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


#Viewset - the viewset automatically provide default 'read-only' operations. We set querySet and serializer class attributes exactly as it is , but we no longer need to provide same info for two classes seperately 
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]


#     def get(self,requst,*args,**kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)
    

#We can use ViewSets to remove snippetlist , snippetDetail and snippethighlight class and replace them with a single class


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides 'list' , 'create' , 'retrieve' , 'update' and 'destroy' actions

    Addtionally we also provide an extra 'highlight' action
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    #we have used action decorator to create a custom action named 'highlight'
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highligh(self,request, *args,**kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


