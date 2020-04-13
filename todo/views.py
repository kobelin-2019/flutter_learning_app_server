import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from .models import TodoItem
from .models import Recommend
from .models import User
from django.http import HttpResponse
# Create your views here.

@csrf_exempt
def todoView(request):
    all_todo_items = TodoItem.objects.all()
    return render(request,'todo.html', {'all_items':all_todo_items})


@csrf_exempt
def addTodo(request):
    c = request.POST['content']
    new_item = TodoItem(content = c)
    new_item.save()
    return HttpResponseRedirect('/todo/')

@csrf_exempt
def deleteTodo(request, todo_id):
    item_to_delete = TodoItem.objects.get(id=todo_id)
    item_to_delete.delete()
    return HttpResponseRedirect('/todo/')

@csrf_exempt
def dispatch_funcs(request, request_string):
    print('linruier')
    if request_string == "idea_topic":
        return idea_topic(request)
    elif request_string == "message":
        return message(request)
    elif(request_string == "myhome_recommend"):
        return myhome_recommend(request)
    elif(request_string == "recommend_articles"):
        return recommend_articles(request)
    elif(request_string == "publish_article"):
        return publish_article(request)
    elif(request_string == "add_count"):
        return add_count(request)
    elif(request_string == "del_count"):
        return del_count(request)
    elif(request_string == 'registerUser'):
        return register(request)
    elif(request_string == 'login'):
        return login(request)
    elif(request_string == 'get_photo_id'):
        return get_photo_id(request)

@csrf_exempt
def idea_topic(request):
    return render(request, 'idea_topic.json')

@csrf_exempt
def message(request):
    return render(request, 'message.json')

def makeJson(datalist):
    ans = "{ \"data\" : [ "
    print(datalist)
    datalist.reverse()
    for item in datalist:
        res = ""
        name = item.author_name
        cnt = item.voteup_count
        title = item.title
        details = item.details
        photo_id = 0;
        idx = item.identifier
        res = res + "{"
        res = res + "\"photo_id\" :"
        user_list = list(User.objects.filter(name=name))
        if (user_list.__len__() > 0):
            photo_id = user_list[0].photo_id

        res = res + "\"" + photo_id.__str__()
        res = res + "\""
        res = res +", \"id\": \""+idx+"\""
        res = res + ", \"author\": {\"id\": 2016001, \"name\": \"" + name +"\"}, \"voteup_count\": "+cnt.__str__()
        res = res + ", \"target\": {\"id\": 2016001, \"details\": \"" + details + "\", \"title\": \"" +title+ "\", \"voteup_count\": "+cnt.__str__()+", \"author\": {\"id\": 2016001, \"name\": \""
        res = res + name + "\"}}} "
        if(item != datalist[datalist.__len__() - 1]):
            res = res + ", "
        ans = ans + res
    ans = ans + "] }"

    print(ans)
    return ans


@csrf_exempt
def myhome_recommend(request):
    datalist = list(Recommend.objects.all())
    jsonString = makeJson(datalist)
   # jsonString = "???"
    return HttpResponse(jsonString)

@csrf_exempt
def recommend_articles(request):

    return render(request, 'recommend_articles.json')

@csrf_exempt
def publish_article(request):
    if request.method=='POST':
        received_json_data = json.loads(request.body)
        print('收到：')
        print(received_json_data)
        _name = "linruier"
        _cnt = 11
        _title = "88888"
        _details = "handsome"
        _name = received_json_data['author']['name']
        _cnt = 0
        _title = received_json_data['target']['title']
        _details = received_json_data['target']['details']
        _tmp = ""
        for i in range(0, len(_details), 1):
            if(_details[i] != '"' and _details[i]!='\n'):
                _tmp += _details[i]
            elif(_details[i] == '\n'):_tmp+='\\n'
        _details = _tmp;
        recommend = Recommend(author_name=_name,voteup_count=_cnt,title=_title,details=_details)
        recommend.save()
        recommend.identifier = "recommend_" + str(recommend.id)
        recommend.save()
        recommend_list = Recommend.objects.all()
        return HttpResponse('OK!!!')
    else :
        print('不是POST请求！')
        return HttpResponse("Failed")

@csrf_exempt
def add_count(request):
    if(request.method == 'POST'):
        received_json_data = json.loads(request.body)
        idx = received_json_data['id']
        recommends = list(Recommend.objects.filter(identifier=idx))
        for item in recommends:
            item.voteup_count=item.voteup_count+1
            item.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('NOT GET')

@csrf_exempt
def del_count(request):
    if(request.method == 'POST'):
        received_json_data = json.loads(request.body)
        idx = received_json_data['id']
        recommends = list(Recommend.objects.filter(identifier=idx))
        for item in recommends:
            item.voteup_count=item.voteup_count-1
            item.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('NOT GET')



@csrf_exempt
def register(request):
    if(request.method == 'POST'):
        received_json_data = json.loads(request.body)
        _name = received_json_data['name']
        _password = received_json_data['password']
        _photoid = received_json_data['photo_id']
        user_list = list(User.objects.filter(name=_name))
        if(user_list.__len__() > 0):
            return HttpResponse('name_repeat')
        else:
            new_user = User(name=_name,password=_password,photo_id=_photoid)
            new_user.save()
            return HttpResponse('ok')
    else:
        return HttpResponse('NOT GET')

@csrf_exempt
def login(request):
    if(request.method == 'POST'):
        received_json_data = json.loads(request.body)
        _name = received_json_data['name']
        _password = received_json_data['password']
        user_list = list(User.objects.filter(name=_name,password=_password))
        if(user_list.__len__() > 0):
               dic = dict({'status':'ok','photo_id':user_list[0].photo_id});
               _json = json.dumps(dic)
               return HttpResponse(_json)
        else:
            return HttpResponse('login failed')
    else:
        return HttpResponse('NOT GET')







