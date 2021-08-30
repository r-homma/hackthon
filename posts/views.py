from django.shortcuts import render
from django.http import HttpResponse
from .forms import PostForm
from .models import Post
from django.shortcuts import redirect
from django.core.paginator import Paginator

def index(request,num=1):
    data = Post.objects.all()
    page = Paginator(data, 3)
    params = {
        'data': page.get_page(num)
    }
    return render(request, 'posts/index.html', params)

def create(request):
    if (request.method == 'POST'):
        obj = Post()
        post = PostForm(request.POST, instance=obj)
        post.save()
        return redirect(to='/posts')
    params = {
        'form': PostForm(),    
    }       
    return render(request,'posts/create.html',params)

def edit(request, num):
    obj = Post.objects.get(id=num)
    if(request.method == 'POST'):
        post = PostForm(request.POST, instance=obj)
        post.save()
        return redirect(to='/posts')
    params = {
        'title':'welcome！',
        'msg':'問題を編集',
        'id':num,
        'form': PostForm(instance=obj), 
    }
    return render(request, 'posts/edit.html', params)

def delete(request, num):
    post = Post.objects.get(id=num)
    if(request.method == 'POST'):
        post.delete()
        return redirect(to='/posts')
    params = {
        'title':'welcome!!',
        'msg':'問題を削除',
        'id':num,
        'obj': post,
    }
    return render(request, 'posts/delete.html', params)
#class PostCreateView(CreateView):
    template_name = 'index.html'
    form_class = PostForm


# 問題に回答する関数を定義。正解不正解の判定をさせるための条件分技をif文を使って定義。
def tyousen(request, num):
    obj = Post.objects.get(id=num)# 問題番号に応じたクエリセットのみをobjに代入
    if request.method == 'POST':# postsページ(index.html)でchallengeボタンを押した時の処理
        kaitouview = request.POST['kaitou']# tyousenページで回答欄に記入した文字列をkaitouviewに代入
        if kaitouview == obj.answer:# 正解の場合の処理
            dic_seikai = {
                'title':'welcome！',
                'msg':'問題に挑戦',
                'pulldown':obj.pulldown,# models.pyのpulldownフィールドのみを抽出。
                'text':obj.text,# models.pyのtextフィールドのみを抽出。
                'reference':obj.reference,# models.pyのreferenceフィールドのみを抽出。
                'id':num,
                'kaitou_hyouzi':'',
                }
            dic_seikai['kaitou_hyouzi'] = kaitouview# 文字列をdic_seikaiの要素の'kaitou_hyouzi'keyに対応する値として定義
            return render(request, 'posts/seikai.html', dic_seikai)  
        else:# 不正解の場合の処理
            dic_fuseikai = {
                'title':'welcome！',
                'msg':'問題に挑戦',
                'pulldown':obj.pulldown,# models.pyのpulldownフィールドのみを抽出。
                'text':obj.text,# models.pyのtextフィールドのみを抽出。
                'id':num,
                'answer':obj.answer,# models.pyのanswerフィールドのみを抽出。
                'reference':obj.reference,# models.pyのreferenceフィールドのみを抽出。
                'kaitou_hyouzi':'',
                }
            dic_fuseikai['kaitou_hyouzi'] = kaitouview# 文字列をdic_seikaiの要素の'kaitou_hyouzi'keyに対応する値として定義
            return render(request, 'posts/fuseikai.html', dic_fuseikai) 
    params = {
        'title':'welcome！',
        'msg':'問題に挑戦',
        'pulldown':obj.pulldown,
        'text':obj.text,
        'id':num,
    }
    return render(request, 'posts/tyousen.html', params) 
# Create your views here.
