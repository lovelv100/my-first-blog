from django.db import models
from django.utils import timezone


class Post(models.Model):            # Post라는 모델을 만들었다.                  # admin계정으로 글쓴이의 글쓰기를 하겠다. CASCADE는 계정 삭제시 올린글도 함께 삭제 된다는 옵션.
    # author는 auth.User모델과 연동, auth.User는 admin 계정을 위해 장고에서 자동으로 생성하는 모델명. createsuperuser 명령어 등으로 생성한 계정을 저장한다.
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)      # 블로그 주인이 admin계정이 되어야 한다. 패키지 만들시 USer라는 창고가 같이 만들어진다. auth에게 user라는 창고를 쓰게 하겠다.
    # 제목을 나타내는 부분, CharField는 글자수가 제한된 필드이며 최대 글자수 200글자
    title = models.CharField(max_length=200)
    # 본문을 나타내는 부분, TextField는 글자수 제한이 없음을 의미함.
    text = models.TextField()
    # 작성시간을 나타내는 부분, timezone은 django.utils의 것을 사용함
    # 글 최초 작성 시간을 나타내는 부분. default는 미입력시 자동기입할 자료
    created_date = models.DateTimeField(default=timezone.now)     # 여기의 now는 변수로 작용하기 때문에 괄호 없음.
    # 최종 수정시간을 나타내는 부분.
    # blank는 공백으로 둬도 되는지, null은 입력을 안 해도 되는지를 나타냄.
    published_date = models.DateTimeField(blank=True, null=True)                   # blank, null의 True는 공백으로 넣어도, 입력하지 않아도 된다는 표현.????

    # 글을 수정할 때 실행할 함수. 사용자가 날짜를 기입하는게 아니라 수정시 매법 호출되어 최종 수정시각을 갱신한다.
    def publish(self):
        # published_date의 값만 수정 당시의 현재 시간으로 바꾸기
        self.published_date = timezone.now()
        # 바꾼 시간은 저장까지 해 줘야 DB에 반영됨
        self.save()
    # admin페이지에서 Post 모델에 관련된 내용 조회시 글 제목이 나옴.
    def __str__(self):
        return self.title
