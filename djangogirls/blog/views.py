from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse
from .models import Post
from django.utils import timezone
from .forms import PostForm

# Create your views here.
def post_list(request):
    # return HttpResponse('post_list 준비중')
    # HttpResponse 는  print()구문처럼 내부에 적은 문자열을 화면에 출력한다.
    # 단, HttpResponse는 콘솔창에 출력하지 않고, 웹 페이지에 출력해준다.
    # return HttpResponse('post_list 준비중')

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # render함수는 바로 템플릿 파일을 지정해서 사용할 수 있다.
    return render(request, 'blog/post_list.html', {'posts':posts})           # 딕셔너리 안에 왼쪽은 템플릿에서 사용할이름과 
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})       # view에서 완성한 자료는 템플릿으로 넘겨 주어야 한다.
        
def post_new(request):
    # 요청 방식이 POST방식으로 전달되었는지 검증한다.
    if request.method == "POST":   
        # PostForm 양식을 받아오되 POST방식으로 전달된 데이터를 채워 엏는다.
        # 이렇게 되면 title, text, create_date 세개의 컬럼에 자료가 채워 진다.
        # 단, 아직 author, published_date에는 자료가 채워 지지 않은 상태이다.
        form = PostForm(request.POST)
        # 들어온 자료가 올바른 자료인지 .is_valid()로 검사한다.
        # 자료가 올바른(폼을 통해 전달된 자료)라면 is_valid()는 True이다.
        if form.is_valid():
            # 나머지 2개 컬럼에 대해서도 자료를 모두 저장하기 위해서
            # 먼저 현재 들어와있는 3개 자료에 대해서 임시 저장을 한다.
            # commit=False로 save() 함수를 실행하면 임시저장 상태.
            post = form.save(commit=False)
            # author 컬럼에는 요청한 유저를 집어 넣는다.
            post.author = request.user
            # published_date 컬럼에는 현재 시간을 집어 넣는다.
            post.published_date = timezone.now()
            # 모자란 2개 컬럼을 다 채웠기 때문에 DB에 완전 저장.
            post.save()
            # 자료를 다 집어 넣었다면 올린 글을 확인할 수 있도록 상세페이지로 간다.
            # return redirect후 자동완성 -> django.shortcuts 선택
            # redirect의 'post_detail'은 urls.py의 post_detail 패턴.
            return redirect('post_detail', pk=post.pk)
    else:
#     form 양식을 작성할 경우에는 forms.py 내부의 자료를 
#     form 이라는 변수에 저장 받는다.
        form = PostForm()
    # 저장한 form을 render 함수를 이용하여 템플릿으로 보내준다.
    return render(request, 'blog/post_edit.html', {'form':form})

    
def post_edit(request, pk):
    # 사용자가 없는 pk로 접속하는 것을 방지하기 위해서 404처리.
    post = get_object_or_404(Post, pk=pk)
    # POST방식으로 요청받은 경우(수정버튼을 눌러서 요청받은 경우)
    if request.method == "POST":
        # instance는 미리 적혀있던 정보를 폼에 저장
        form = PostForm(request.POST, instance=post)        # instance/  기본적으로 form에  채워져있는것을 수정
        # 미리 적혀있던 정보가 유효한 정보인지 검증
        if form.is_valid():
            # 수정시에도 역시 published_date와 글쓴이 확인을 해야함.
            # 그래서 임시저장을 먼저 하고 author와 published_date를 다시 입력
            post = form.save(commit=False)
            post.author = request.user              # 로그인한 유저 정보
            post.published_date = timezone.now()
            # 정보를 모두 넘겨받으면 다시 최종저장
            post.save()
            # 최종저장 후 post_detail 주소로 다시 보내서 수정결과 확인
            return redirect('post_detail', pk=post.pk)
    else:
        # post가 이닌 get방식인 경우 수정결과 반영이 아닌 수정창만 보여줌
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
    
    '''
    Post.objects. 를 이용해서 다음 조건을 만족시키는 ORM을 사용해 보세요
    1. 배포 시간이 현재 시간 이전일 것.
    2. published_date 기준으로 내림차순
    '''
    
