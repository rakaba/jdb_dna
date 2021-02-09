from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()


class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ('last_name', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class StyleGetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['styletestid', 'styletestpass']
        labels={
           'styletestid':'検体ID',
           'styletestpass':'検体パスワード',
           }

class SkinGetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['skintestid', 'skintestpass']
        labels={
           'skintestid':'検体ID',
           'skintestpass':'検体パスワード',
           }

class DnaApplicationForm(forms.Form):
    coursedata=[
        ('遺伝子BODY革命','遺伝子BODY革命'),
        ('遺伝子FACIAL革命','遺伝子FACIAL革命'),
        ('遺伝子MUSCLE革命','遺伝子MUSCLE革命'),
        ('遺伝子HEAD革命','遺伝子HEAD革命'),
    ]
    itemdata=[
        ('BODY検査結果対応サプリメント｜2610円','BODY検査結果対応サプリメント｜2610円'),
        ('BODY検査結果対応プロテイン｜2610円','BODY検査結果対応プロテイン｜2610円'),
        ('FACIAL検査結果対応美容液｜4410円','FACIAL検査結果対応美容液｜4410円'),
        ('HEAD検査結果対応シャンプー｜2241円','HEAD検査結果対応シャンプー｜2241円'),
    ]
    testid = forms.CharField(label='検体ID')
    last_name = forms.CharField(label='姓')
    first_name = forms.CharField(label='名')
    gender = forms.ChoiceField(choices=(('女性', '女性'), ('男性', '男性')), label='性別')
    course = forms.MultipleChoiceField(choices=coursedata, label='コース', widget=forms.CheckboxSelectMultiple(attrs={'size':4}))
    item = forms.MultipleChoiceField(choices=itemdata, label='結果に合わせた二次商品（10%OFF）', widget=forms.CheckboxSelectMultiple(attrs={'size':4}), required=False)
    print = forms.ChoiceField(choices=(('印刷有り', '印刷有り'), ('印刷無し', '印刷無し')), label='印刷オプション')
    myself = forms.BooleanField(label='同じ内容を受け取る', required=False)

class ItemOrderForm(forms.Form):
    numberdata1 = [('0', '発注数を選択'), ('1', '1個'), ('2', '2個'), ('3', '3個'), ('4', '4個'), ('5', '5個'), ]
    numberdata2 = [('0', '発注数を選択'), ('5', '5個'), ('10', '10個'), ]
    numberdata3 = [('0', '発注数を選択'), ('1', '1セット（2個）'), ('2', '2セット（4個）'), ]
    numberdata4 = [('0', '発注数を選択'), ('1', '1セット（3個）'), ('2', '2セット（6個）'), ]
    numberdata5 = [('0', '発注数を選択'), ('1', '1セット（10枚）'), ('2', '2セット（20枚）'), ('3', '3セット（30枚）'), ('4', '4セット（40枚）'), ('5', '5セット（50枚）'), ]
    numberdata6 = [('0', '発注数を選択'), ('1', '1セット（5冊）'), ('2', '2セット（10冊）'), ('3', '3セット（15冊）'), ('4', '4セット（20冊）'), ('5', '5セット（25冊）'), ]
    numberdata7 = [('0', '発注数を選択'), ('1', '1枚'), ('2', '2枚'), ('3', '3枚'), ('4', '4枚'), ('5', '5枚'), ]
    kit_no_box = forms.ChoiceField(choices=numberdata2, label='【遺伝子革命】遺伝子サンプル採取セット（箱無し）｜0円')
    kit_box = forms.ChoiceField(choices=numberdata1, label='【遺伝子革命】遺伝子サンプル採取セット（箱有り）｜100円')
    kit_flora_light = forms.ChoiceField(choices=numberdata1, label='【美腸革命】light：1個｜4900円')
    kit_flora_light_2set = forms.ChoiceField(choices=numberdata3, label='【美腸革命】light：同一受検者2個セット｜8820円')
    kit_flora_light_3set = forms.ChoiceField(choices=numberdata4, label='【美腸革命】light：同一受検者3個セット｜12495円')
    dhs_c = forms.ChoiceField(choices=numberdata1, label='DHS-LOCK-　糖代謝リスク対策サプリメント｜2900円')
    dhs_p = forms.ChoiceField(choices=numberdata1, label='DHS-PLUS-　たんぱく質リスク対策サプリメント｜2900円')
    dhs_f = forms.ChoiceField(choices=numberdata1, label='DHS-CUT-　脂質代謝リスク対策サプリメント｜2900円')
    dhp_c = forms.ChoiceField(choices=numberdata1, label='DHP-LOCK-　糖代謝リスク対策プロテイン｜2900円')
    dhp_p = forms.ChoiceField(choices=numberdata1, label='DHP-PLUS-　たんぱく質リスク対策プロテイン｜2900円')
    dhp_f = forms.ChoiceField(choices=numberdata1, label='DHP-CUT-　脂質代謝リスク対策プロテイン｜2900円')
    shampoo_1 = forms.ChoiceField(choices=numberdata1, label='SCALP SELEB01　活性酸素リスク対策シャンプー｜2490円')
    shampoo_2 = forms.ChoiceField(choices=numberdata1, label='SCALP SELEB02　糖化リスク対策シャンプー｜2490円')
    shampoo_3 = forms.ChoiceField(choices=numberdata1, label='SCALP SELEB03　過酸化脂質リスク対策シャンプー｜2490円')
    biyoueki_1 = forms.ChoiceField(choices=numberdata1, label='美肌博士01　活性酸素リスク対策美容液｜4900円')
    biyoueki_2 = forms.ChoiceField(choices=numberdata1, label='美肌博士02　糖化リスク対策美容液｜4900円')
    biyoueki_3 = forms.ChoiceField(choices=numberdata1, label='美肌博士03　過酸化脂質リスク対策美容液｜4900円')
    minibook_1 = forms.ChoiceField(choices=numberdata6, label='【小冊子】遺伝子革命商品紹介：5冊セット｜150円')
    minibook_2 = forms.ChoiceField(choices=numberdata6, label='【小冊子】遺伝子検査の説明：5冊セット｜150円')
    pop_diet = forms.ChoiceField(choices=numberdata5, label='【商品紹介A4ポップ】BODY-diet&bodymake-：10枚セット｜80円')
    pop_skincare = forms.ChoiceField(choices=numberdata5, label='【商品紹介A4ポップ】FACIAL-skincare&anti-aging-：10枚セット｜80円')
    pop_typecheck = forms.ChoiceField(choices=numberdata5, label='【検査説明A4ポップ】DNAタイプチェック：10枚セット｜80円')
    pop_risk_c = forms.ChoiceField(choices=numberdata5, label='【検査説明A4ポップ】糖代謝リスク：10枚セット｜80円')
    pop_risk_p = forms.ChoiceField(choices=numberdata5, label='【検査説明A4ポップ】たんぱく質リスク：10枚セット｜80円')
    pop_risk_f = forms.ChoiceField(choices=numberdata5, label='【検査説明A4ポップ】脂質代謝リスク：10枚セット｜80円')
    pop_supplement_1 = forms.ChoiceField(choices=numberdata5, label='【二次商品紹介A4ポップ】リスク別サプリメント①：10枚セット｜80円')
    pop_supplement_2 = forms.ChoiceField(choices=numberdata5, label='【二次商品紹介A4ポップ】リスク別サプリメント②：10枚セット｜80円')
    pop_protein_1 = forms.ChoiceField(choices=numberdata5, label='【二次商品紹介A4ポップ】リスク別プロテイン①：10枚セット｜80円')
    pop_protein_2 = forms.ChoiceField(choices=numberdata5, label='【二次商品紹介A4ポップ】リスク別プロテイン②：10枚セット｜80円')
    pop_shampoo_1 = forms.ChoiceField(choices=numberdata5, label='【二次商品紹介A4ポップ】リスク別シャンプー①：10枚セット｜80円')
    pop_shampoo_2 = forms.ChoiceField(choices=numberdata5, label='【二次商品紹介A4ポップ】リスク別シャンプー②：10枚セット｜80円')
    pop_biyoueki_1 = forms.ChoiceField(choices=numberdata5, label='【二次商品紹介A4ポップ】リスク別美容液①：10枚セット｜80円')
    pop_biyoueki_2 = forms.ChoiceField(choices=numberdata5, label='【二次商品紹介A4ポップ】リスク別美容液②：10枚セット｜80円')
    leaflet_with23 = forms.ChoiceField(choices=numberdata5, label='【３つ折りリーフレット】遺伝子革命：10枚セット｜100円')
    leaflet_withflora = forms.ChoiceField(choices=numberdata5, label='【３つ折りリーフレット】美腸革命：10枚セット｜100円')
    voice_paper = forms.ChoiceField(choices=numberdata5, label='【お客様の声】記入用白紙：10枚セット｜0円')
    voice_note = forms.ChoiceField(choices=numberdata1, label='【お客様の声】記入済冊子：1冊｜240円')
    poster_body = forms.ChoiceField(choices=numberdata7, label='【ポスター】BODY-diet&bodymake-｜80円')
    poster_facial = forms.ChoiceField(choices=numberdata7, label='【ポスター】FACIAL-skincare&anti-aging-｜80円')
    book_body = forms.ChoiceField(choices=numberdata1, label='【サンプルブック】遺伝子BODY革命：2冊1組｜2000円')
    book_facial = forms.ChoiceField(choices=numberdata1, label='【サンプルブック】遺伝子FACIAL革命：2冊1組｜2000円')
    book_muscle = forms.ChoiceField(choices=numberdata1, label='【サンプルブック】遺伝子MUSCLE革命：2冊1組｜2000円')
    book_head = forms.ChoiceField(choices=numberdata1, label='【サンプルブック】遺伝子HEAD革命：2冊1組｜2000円')
    pop_stand = forms.ChoiceField(choices=numberdata5, label='ポップスタンド：1個｜80円')
    price_card = forms.ChoiceField(choices=numberdata5, label='料金カード：10枚セット｜80円')
    myself = forms.BooleanField(label='同じ内容を受け取る', required=False)

class SkinGetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['skintestid', 'skintestpass']
        labels={
           'skintestid':'検体ID',
           'skintestpass':'検体パスワード',
           }

class MuscleGetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['muscletestid', 'muscletestpass']
        labels={
           'muscletestid':'検体ID',
           'muscletestpass':'検体パスワード',
           }

class HeadGetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['headtestid', 'headtestpass']
        labels={
           'headtestid':'検体ID',
           'headtestpass':'検体パスワード',
           }

class FloraLightGetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['floralighttestid', 'floralighttestpass']
        labels={
           'floralighttestid':'検体ID',
           'floralighttestpass':'検体パスワード',
           }

class FloraExpertGetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['floraexperttestid', 'floraexperttestpass']
        labels={
           'floraexperttestid':'検体ID',
           'floraexperttestpass':'検体パスワード',
           }

class FoodProteinGetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['foodproteintestid', 'foodproteintestpass']
        labels={
           'foodproteintestid':'検体ID',
           'foodproteintestpass':'検体パスワード',
           }

class OtherGetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['othertestid', 'othertestpass']
        labels={
           'othertestid':'検体ID',
           'othertestpass':'検体パスワード',
           }
