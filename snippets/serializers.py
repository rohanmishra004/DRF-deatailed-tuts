from rest_framework import serializers
from snippets.models import Snippet , LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

'''
class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title= serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template':'textarea.html'})
    linenos=serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self,validated_data):
        #Creates and returns a new 'Snippet' instance given the validated data
        return Snippet.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        #Update and return an existing 'Snippet' instance given the validated data
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code',instance.code)
        instance.linenos = validated_data.get('linesos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
    


    # The first part of the serializer class defines the fields that get serialized.

    # The create() and update() methods define how fully fledged instances are created or modified when calling serialzer.save()

    # Serializer class is very similar to Django form class and includes similar validation flags on various fields such as required,max_length and default

'''


'''

#MODEL SERIALIZERS


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model=Snippet
        fields=['id','title','code','linenos','language','style', 'owner']
        
class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields=['id','username','snippets']
        #we need to explicity add snippets to the user model

        
'''


#HYPERLINKED MODEL SERIALIZERS
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style']
#we've also added a new 'highlight' field. This field is of the same type as the url field, except that it points to the 'snippet-highlight' url pattern, instead of the 'snippet-detail' url pattern.

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    class Meta:
        model=User
        fields = ['url', 'id','username','snippets']



