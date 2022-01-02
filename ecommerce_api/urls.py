from django.contrib import admin
from django.urls import path

# from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphview/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
]
