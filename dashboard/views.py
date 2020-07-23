from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .exception import IncorrectAuthCredentials, IncorrectData
from .serializer import LoginSerializer
from django.http import JsonResponse

from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Metadata, Interpreter


global_data =None

def load_and_train():
    print(os.path.abspath(__file__))
    train_data  = load_data('dashboard/rasa_data_servers.json')
    trainer = Trainer(config.load('dashboard/config_spacy.yaml'))
    trainer.train(train_data)
    model_directory = trainer.persist('dashboard/projects')
    interpreter = Interpreter.load(model_directory)
    global global_data
    global_data =interpreter
    return interpreter




import os.path
import os

from .utility import saveJsonfiles, convertjson
import pickle

class Test(View):
    template_name='Flowchart_.html'

    def get(self,request,*args,**kwargs):

        return render(request,template_name =self.template_name)

test =Test.as_view()


class Login(View):
    template_name='login.html'

    def get(self,request,*args,**kwargs):
        return render(request,template_name =self.template_name)

login =Login.as_view()




class AuthApi(APIView):

    def post(self,request,*args,**kwargs):
        """ post method to authenticate the users provided email and password """
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data['username'])
            user = authenticate(username=serializer.data['username'], password=request.data['password'])
        else:
            raise IncorrectData(detail=serializer.errors,code=400)
        if not user:
            raise IncorrectAuthCredentials(detail="Incorrect authentication credentials", code=401)
        return Response({'Auth':True}, status=status.HTTP_200_OK)

auth = AuthApi.as_view()



class UploadApi(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self,request,*args,**kwargs):
        """ post method to authenticate the users provided email and password """
        folder = 'media/'
        myfile = request.FILES['files']
        print(myfile.name)
        if os.path.isfile('media/' + str(myfile.name)):
            os.remove('media/' + str(myfile.name))
        fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
        filename = fs.save(myfile.name, myfile)
        file_url = fs.url(filename)
        saveJsonfiles(myfile.name)
        return Response({'Auth':True}, status=status.HTTP_200_OK)

upload_api = UploadApi.as_view()



@method_decorator(csrf_exempt, name='dispatch')
class SaveFile(View):
    # parser_classes = (MultiPartParser, )

    def post(self,request,*args,**kwargs):
        folder = 'media/'
        if  request.FILES['myfile']:
            myfile = request.FILES['myfile']
            print(myfile.name)
            if os.path.isfile('media/'+str(myfile.name)):
               os.remove('media/'+str(myfile.name))
            fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
            filename = fs.save(myfile.name, myfile)
            file_url = fs.url(filename)
            saveJsonfiles(myfile.name)

            # pushTos3(file_url,filename)
            return JsonResponse({'file_url':file_url,'name':filename})


save_file = SaveFile.as_view()


class GetJsonAPi(APIView):

    def get(self,request,*args,**kwargs):
        data = convertjson()
        return Response({'data':data})
get_api_json =GetJsonAPi.as_view()


class GetSpecificJsonAPi(APIView):

    def get(self,request,genre,*args,**kwargs):
        data = convertjson()
        desired_val = None
        for item in data:
            if item['Redfish/Rest Testcases'] == genre:
                desired_val = item
                print(desired_val,"<<<<<<<<<<<<<<")
        return Response({'data':desired_val})

get_specific_api_json =GetSpecificJsonAPi.as_view()


class DisplayTable(APIView):

    template_name = 'dashboard.html'
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

tabletemplate= DisplayTable.as_view()



import json


class ManpulateJson(APIView):

    def post(self,request,*args,**kwargs):
        data = request.data
        comment =''
        # print(claer)
        data = json.loads(data['data'])
        duplicate_data = data
        for x in data:
            if 'category' in x:
                if x['category']=='Comment':
                    comment=x['text']
                    address = duplicate_data.index(x)
                    duplicate_data.pop(address)
                if x['category']=='Start':
                    address = duplicate_data.index(x)
                    duplicate_data.pop(address)
                if x['category']=='End':
                    address = duplicate_data.index(x)
                    duplicate_data.pop(address)
            if x['key']==-1:
                address = duplicate_data.index(x)
                duplicate_data.pop(address)
        duplicate_data.pop(0)
        final_data =[]
        if global_data is None:
            call = load_and_train()
            print(global_data)
            for x in duplicate_data:
                final_data.append(global_data.parse(x['text']))
        else:
            for x in duplicate_data:
                final_data.append(global_data.parse(x['text']))
            print(global_data,"elseeeee")


        print(comment.split(','))

        return Response({'data': duplicate_data,'tempdata':final_data})
manpulate_json = ManpulateJson.as_view()



