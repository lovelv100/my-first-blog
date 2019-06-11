# 장고 form 양식을 사용하기 위해 forms 호출
from django import forms
# Post 모델에 자료를 보내줄 것임
from .models import Post


# Pos에 대한form이기 때문에 이름은 PostForm
# forms.ModelForm을 괄호 사이에 집어 넣어야 form 구현 가능
class PostForm(forms.ModelForm):

    # PostForm 내부에 Meta라는 이름으로 작성할 경우
    # 타겟 모델은 model = 모델이름 형식으로
    # 사용자에세 입력받을 부분은 fields = ('1번 컬럼', '2번컬럼' ...)
    # 형식으로 작성할 수 있다.
    class Meta:
        model = Post           # 목적지는 Post이다!!
        fields = ('title', 'text',)          # Post에 있는 컬럼중에서 / 로그인 되어있는 사람이 author이기때문에 필요는 없다.(사용자가 무조건 입력해야 하는 부분만 사용한다.)
                                            # 나머지는 author는 포린키, create_date는 default......