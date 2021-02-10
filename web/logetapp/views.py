from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, EmailChangeForm, StyleGetForm, SkinGetForm, MuscleGetForm, HeadGetForm, FloraLightGetForm, FloraExpertGetForm, FoodProteinGetForm, OtherGetForm, DnaApplicationForm, ItemOrderForm
)
from .models import User, StyleDnaModel, SkinDnaModel, MuscleDnaModel, HeadDnaModel, FloraLightModel, FloraExpertModel, FoodProteinModel, OtherModel, StoreModel


User = get_user_model()


class Top(generic.TemplateView):
    template_name = 'register/top.html'
    def post(self, request, *args, **kwargs):
        user = self.request.user
    def get_context_data(self, **kwargs):
        allstoreemail = StoreModel.objects.values_list('email', flat=True)
        allstoreemail_list = list(allstoreemail)
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        context["allstoreemail_list"] = allstoreemail_list
        return context

class Sample(generic.TemplateView):
    """結果サンプルページ"""
    template_name = 'register/styledna/sample.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    form_class = LoginForm
    template_name = 'register/logout.html'


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        # user.is_active = False
        user.is_active = True
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('register/mail_template/create/subject.txt', context)
        message = render_to_string('register/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('logetapp:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # まだ仮登録で、他に問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class OnlyYouMixin(UserPassesTestMixin):
    """本人か、スーパーユーザーだけユーザーページアクセスを許可する"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    """ユーザーの詳細ページ"""
    model = User
    template_name = 'register/user_detail.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    """ユーザー情報更新ページ"""
    model = User
    form_class = UserUpdateForm
    template_name = 'register/user_form.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く

    def get_success_url(self):
        return resolve_url('logetapp:user_detail', pk=self.kwargs['pk'])


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('logetapp:password_change_done')
    template_name = 'register/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'register/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'register/mail_template/password_reset/subject.txt'
    email_template_name = 'register/mail_template/password_reset/message.txt'
    template_name = 'register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('logetapp:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'register/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('logetapp:password_reset_complete')
    template_name = 'register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'register/password_reset_complete.html'


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'register/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('register/mail_template/email_change/subject.txt', context)
        message = render_to_string('register/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('logetapp:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'register/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'register/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)


def listview(request):
    object_list = User.objects.all()
    object = {
        'object':object_list,
    }

    return render(request, 'register/list.html', object)


def storedetailview(request, pk):
    obj = User.objects.get(pk=pk)
    targetstyle = StyleDnaModel.objects.filter(stylestoreid=obj)
    object = {
        'object':obj,
        'targetstyle':targetstyle
    }
    return render(request, 'register/storedetail.html', object)


def dnaapplicationview(request, pk):

    if request.method == 'POST':
        form = DnaApplicationForm(request.POST)

        if form.is_valid():
            obj = User.objects.get(pk=pk)
            userid = obj.email
            objstore = StoreModel.objects.get(email=userid)
            storename = objstore.storename
            context =  {
                'storename': storename,
                'userid': userid,
                'testid': form.cleaned_data['testid'],
                'last_name': form.cleaned_data['last_name'],
                'first_name': form.cleaned_data['first_name'],
                'gender': form.cleaned_data['gender'],
                'course': form.cleaned_data['course'],
                'item': form.cleaned_data['item'],
                'print': form.cleaned_data['print'],
            }
            subject = "【遺伝子革命】検査申し込み"
            message = render_to_string('register/mail_template/dnaapplication/message.txt', context)
            sender = userid
            myself = form.cleaned_data['myself']
            recipients = [settings.EMAIL_HOST_USER]

            if myself:
                recipients.append(sender)
            try:
                send_mail(subject, message, sender, recipients)
            except BadHeaderError:
                return HttpResponse('無効なヘッダーが見つかりました。')

            return redirect('logetapp:dnaapplication_done')

    else:
        form = DnaApplicationForm()
    return render(request, 'register/dnaapplication.html', {'form': form})

def dnaapplication_doneview(request):
    return render(request, 'register/dnaapplication_done.html')


def itemorderview(request, pk):

    if request.method == 'POST':
        form = ItemOrderForm(request.POST)

        if form.is_valid():
            obj = User.objects.get(pk=pk)
            userid = obj.email
            objstore = StoreModel.objects.get(email=userid)
            storename = objstore.storename
            context =  {
                'storename':storename,
                'userid': userid,
                'kit_no_box': form.cleaned_data['kit_no_box'],
                'kit_box': form.cleaned_data['kit_box'],
                'kit_flora_light': form.cleaned_data['kit_flora_light'],
                'kit_flora_light_2set': form.cleaned_data['kit_flora_light_2set'],
                'kit_flora_light_3set': form.cleaned_data['kit_flora_light_3set'],
                'pop_diet': form.cleaned_data['pop_diet'],
                'dhs_c': form.cleaned_data['dhs_c'],
                'dhs_p': form.cleaned_data['dhs_p'],
                'dhs_f': form.cleaned_data['dhs_f'],
                'dhp_c': form.cleaned_data['dhp_c'],
                'dhp_p': form.cleaned_data['dhp_p'],
                'dhp_f': form.cleaned_data['dhp_f'],
                'shampoo_1': form.cleaned_data['shampoo_1'],
                'shampoo_2': form.cleaned_data['shampoo_2'],
                'shampoo_3': form.cleaned_data['shampoo_3'],
                'biyoueki_1': form.cleaned_data['biyoueki_1'],
                'biyoueki_2': form.cleaned_data['biyoueki_2'],
                'biyoueki_3': form.cleaned_data['biyoueki_3'],
                'minibook_1': form.cleaned_data['minibook_1'],
                'minibook_2': form.cleaned_data['minibook_2'],
                'pop_skincare': form.cleaned_data['pop_skincare'],
                'pop_typecheck': form.cleaned_data['pop_typecheck'],
                'pop_risk_c': form.cleaned_data['pop_risk_c'],
                'pop_risk_p': form.cleaned_data['pop_risk_p'],
                'pop_risk_f': form.cleaned_data['pop_risk_f'],
                'pop_supplement_1': form.cleaned_data['pop_supplement_1'],
                'pop_supplement_2': form.cleaned_data['pop_supplement_2'],
                'pop_protein_1': form.cleaned_data['pop_protein_1'],
                'pop_protein_2': form.cleaned_data['pop_protein_2'],
                'pop_shampoo_1': form.cleaned_data['pop_shampoo_1'],
                'pop_shampoo_2': form.cleaned_data['pop_shampoo_2'],
                'pop_biyoueki_1': form.cleaned_data['pop_biyoueki_1'],
                'pop_biyoueki_2': form.cleaned_data['pop_biyoueki_2'],
                'leaflet_with23': form.cleaned_data['leaflet_with23'],
                'leaflet_withflora': form.cleaned_data['leaflet_withflora'],
                'voice_paper': form.cleaned_data['voice_paper'],
                'voice_note': form.cleaned_data['voice_note'],
                'poster_body': form.cleaned_data['poster_body'],
                'poster_facial': form.cleaned_data['poster_facial'],
                'book_body': form.cleaned_data['book_body'],
                'book_facial': form.cleaned_data['book_facial'],
                'book_muscle': form.cleaned_data['book_muscle'],
                'book_head': form.cleaned_data['book_head'],
                'pop_stand': form.cleaned_data['pop_stand'],
                'price_card': form.cleaned_data['price_card'],

            }
            subject = "【アール・ワークス】資材発注"
            message = render_to_string('register/mail_template/itemorder/message.txt', context)
            sender = userid
            myself = form.cleaned_data['myself']
            recipients = [settings.EMAIL_HOST_USER]

            if myself:
                recipients.append(sender)
            try:
                send_mail(subject, message, sender, recipients)
            except BadHeaderError:
                return HttpResponse('無効なヘッダーが見つかりました。')

            return redirect('logetapp:itemorder_done')

    else:
        form = ItemOrderForm()
    return render(request, 'register/itemorder.html', {'form': form})

def itemorder_doneview(request):
    return render(request, 'register/itemorder_done.html')

def storedetailskinview(request, pk):
    obj = User.objects.get(pk=pk)
    targetskin = SkinDnaModel.objects.filter(skinstoreid=obj)
    object = {
        'object':obj,
        'targetskin':targetskin
    }
    return render(request, 'register/storedetail_skin.html', object)


def skinmypageview(request, pk):
    obj = User.objects.get(pk=pk)
    allcheckcode = SkinDnaModel.objects.values_list('skincheckcode', flat=True)
    allcheckcode_list = list(allcheckcode)
    if(request.method == 'POST'):
        a = str(request.POST['skintestid']) + str(request.POST['skintestpass'])

        if a in allcheckcode_list:
            data = SkinGetForm(request.POST, instance=obj)
            data.save()
            targetdna = SkinDnaModel.objects.get(skincheckcode=a)
            ansno = targetdna.skinansno
            name = targetdna.skinname
            storeid = targetdna.skinstoreid
            targetdata = User.objects.get(pk=pk)
            targetdata.skinansno = ansno
            targetdata.skintestername = name
            targetdata.storeid = storeid
            targetdata.save()

            object = {
                'object':targetdata,
                'message':'検査結果'
            }
        else:
            return render(request, 'register/getmiss.html')
    return render(request, 'register/top.html', object)

def skinmytestview(request, pk):
    object = User.objects.get(pk=pk)
    name = object.skintestername
    id = object.skintestid
    memo = "register/skindna/" + str(object.skinansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def skinmyteststoreview(request, pk):
    object = SkinDnaModel.objects.get(pk=pk)
    name = object.skinname
    id = object.skintestid
    memo = "register/skindna/" + str(object.skinansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def skindetailview(request, pk):
    object_list = User.objects.get(pk=pk)
    object = {
        'object':object_list,
        'form':SkinGetForm()
    }

    return render(request, 'register/skindetail.html', object)

def skinpaperview(request, pk):
    obj = SkinDnaModel.objects.get(pk=pk)
    ansno = obj.skinansno
    memo = "https://arr-works.com/with23/book/s" + str(ansno) + ".pdf"
    return render(request, 'register/skindna/skinpaper.html', {'memo': memo})

def storeskinrepoview(request, pk):
    obj = SkinDnaModel.objects.get(pk=pk)
    id = obj.skintestid
    date = obj.skindate
    memo = "https://arr-works.com/with23/book/s_r_" + id + ".pdf"
    return render(request, 'register/skindna/skinrepo.html', {'id': id,'memo': memo, 'date': date})

def storeskinadview(request, pk):
    obj = SkinDnaModel.objects.get(pk=pk)
    id = obj.skintestid
    date = obj.skindate
    memo = "https://arr-works.com/with23/book/s_a_" + id + ".pdf"
    return render(request, 'register/skindna/skinad.html', {'id': id,'memo': memo, 'date': date})

def skinwebview(request, pk):
    obj = SkinDnaModel.objects.get(pk=pk)
    id = obj.skintestid
    memo = "https://arr-works.com/with23/book/s_w_" + id + ".pdf"
    return render(request, 'register/skindna/skinweb.html', {'id': id,'memo': memo})

def storedetailmuscleview(request, pk):
    obj = User.objects.get(pk=pk)
    targetmuscle = MuscleDnaModel.objects.filter(musclestoreid=obj)
    object = {
        'object':obj,
        'targetmuscle':targetmuscle
    }
    return render(request, 'register/storedetail_muscle.html', object)


def musclemypageview(request, pk):
    obj = User.objects.get(pk=pk)
    allcheckcode = MuscleDnaModel.objects.values_list('musclecheckcode', flat=True)
    allcheckcode_list = list(allcheckcode)
    if(request.method == 'POST'):
        a = str(request.POST['muscletestid']) + str(request.POST['muscletestpass'])

        if a in allcheckcode_list:
            data = MuscleGetForm(request.POST, instance=obj)
            data.save()
            targetdna = MuscleDnaModel.objects.get(musclecheckcode=a)
            ansno = targetdna.muscleansno
            name = targetdna.musclename
            storeid = targetdna.musclestoreid
            targetdata = User.objects.get(pk=pk)
            targetdata.muscleansno = ansno
            targetdata.muscletestername = name
            targetdata.storeid = storeid
            targetdata.save()

            object = {
                'object':targetdata,
                'message':'検査結果'
            }
        else:
            return render(request, 'register/getmiss.html')
    return render(request, 'register/top.html', object)

def musclemytestview(request, pk):
    object = User.objects.get(pk=pk)
    name = object.muscletestername
    id = object.muscletestid
    memo = "register/muscledna/" + str(object.muscleansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def musclemyteststoreview(request, pk):
    object = MuscleDnaModel.objects.get(pk=pk)
    name = object.musclename
    id = object.muscletestid
    memo = "register/muscledna/" + str(object.muscleansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def muscledetailview(request, pk):
    object_list = User.objects.get(pk=pk)
    object = {
        'object':object_list,
        'form':MuscleGetForm()
    }

    return render(request, 'register/muscledetail.html', object)

def musclepaperview(request, pk):
    obj = MuscleDnaModel.objects.get(pk=pk)
    ansno = obj.muscleansno
    memo = "https://arr-works.com/with23/book/t" + str(ansno) + ".pdf"
    return render(request, 'register/muscledna/musclepaper.html', {'memo': memo})

def storemusclerepoview(request, pk):
    obj = MuscleDnaModel.objects.get(pk=pk)
    id = obj.muscletestid
    date = obj.muscledate
    memo = "https://arr-works.com/with23/book/t_r_" + id + ".pdf"
    return render(request, 'register/muscledna/musclerepo.html', {'id': id,'memo': memo, 'date': date})

def storemuscleadview(request, pk):
    obj = MuscleDnaModel.objects.get(pk=pk)
    id = obj.muscletestid
    date = obj.muscledate
    memo = "https://arr-works.com/with23/book/t_a_" + id + ".pdf"
    return render(request, 'register/muscledna/musclead.html', {'id': id,'memo': memo, 'date': date})

def musclerepoview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.muscletestid
    targetmuscle = MuscleDnaModel.objects.get(muscletestid = obj.muscletestid)
    date = targetmuscle.muscledate
    memo = "https://arr-works.com/with23/book/t_r_" + id + ".pdf"
    return render(request, 'register/muscledna/musclerepo.html', {'id': id,'memo': memo, 'date': date})

def muscleadview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.muscletestid
    targetmuscle = MuscleDnaModel.objects.get(muscletestid = obj.muscletestid)
    date = targetmuscle.muscledate
    memo = "https://arr-works.com/with23/book/t_a_" + id + ".pdf"
    return render(request, 'register/muscledna/musclead.html', {'id': id,'memo': memo, 'date': date})

def musclewebview(request, pk):
    obj = MuscleDnaModel.objects.get(pk=pk)
    id = obj.muscletestid
    memo = "https://arr-works.com/with23/book/t_w_" + id + ".pdf"
    return render(request, 'register/muscledna/muscleweb.html', {'id': id,'memo': memo})

def storedetailheadview(request, pk):
    obj = User.objects.get(pk=pk)
    targethead = HeadDnaModel.objects.filter(headstoreid=obj)
    object = {
        'object':obj,
        'targethead':targethead
    }
    return render(request, 'register/storedetail_head.html', object)


def headmypageview(request, pk):
    obj = User.objects.get(pk=pk)
    allcheckcode = HeadDnaModel.objects.values_list('headcheckcode', flat=True)
    allcheckcode_list = list(allcheckcode)
    if(request.method == 'POST'):
        a = str(request.POST['headtestid']) + str(request.POST['headtestpass'])

        if a in allcheckcode_list:
            data = HeadGetForm(request.POST, instance=obj)
            data.save()
            targetdna = HeadDnaModel.objects.get(headcheckcode=a)
            ansno = targetdna.headansno
            name = targetdna.headname
            storeid = targetdna.headstoreid
            targetdata = User.objects.get(pk=pk)
            targetdata.headansno = ansno
            targetdata.headtestername = name
            targetdata.storeid = storeid
            targetdata.save()

            object = {
                'object':targetdata,
                'message':'検査結果'
            }
        else:
            return render(request, 'register/getmiss.html')
    return render(request, 'register/top.html', object)

def headmytestview(request, pk):
    object = User.objects.get(pk=pk)
    name = object.headtestername
    id = object.headtestid
    memo = "register/headdna/" + str(object.headansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def headmyteststoreview(request, pk):
    object = HeadDnaModel.objects.get(pk=pk)
    name = object.headname
    id = object.headtestid
    memo = "register/headdna/" + str(object.headansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def headdetailview(request, pk):
    object_list = User.objects.get(pk=pk)
    object = {
        'object':object_list,
        'form':HeadGetForm()
    }

    return render(request, 'register/headdetail.html', object)

def headpaperview(request, pk):
    obj = HeadDnaModel.objects.get(pk=pk)
    ansno = obj.headansno
    memo = "https://arr-works.com/with23/book/h" + str(ansno) + ".pdf"
    return render(request, 'register/headdna/headpaper.html', {'memo': memo})

def storeheadrepoview(request, pk):
    obj = HeadDnaModel.objects.get(pk=pk)
    id = obj.headtestid
    date = obj.headdate
    memo = "https://arr-works.com/with23/book/h_r_" + id + ".pdf"
    return render(request, 'register/headdna/headrepo.html', {'id': id,'memo': memo, 'date': date})

def storeheadadview(request, pk):
    obj = HeadDnaModel.objects.get(pk=pk)
    id = obj.headtestid
    date = obj.headdate
    memo = "https://arr-works.com/with23/book/h_a_" + id + ".pdf"
    return render(request, 'register/headdna/headad.html', {'id': id,'memo': memo, 'date': date})

def headrepoview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.headtestid
    targethead = HeadDnaModel.objects.get(headtestid = obj.headtestid)
    date = targethead.headdate
    memo = "https://arr-works.com/with23/book/h_r_" + id + ".pdf"
    return render(request, 'register/headdna/headrepo.html', {'id': id,'memo': memo, 'date': date})

def headadview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.headtestid
    targethead = HeadDnaModel.objects.get(headtestid = obj.headtestid)
    date = targethead.headdate
    memo = "https://arr-works.com/with23/book/h_a_" + id + ".pdf"
    return render(request, 'register/headdna/headad.html', {'id': id,'memo': memo, 'date': date})

def headwebview(request, pk):
    obj = HeadDnaModel.objects.get(pk=pk)
    id = obj.headtestid
    memo = "https://arr-works.com/with23/book/h_w_" + id + ".pdf"
    return render(request, 'register/headdna/headweb.html', {'id': id,'memo': memo})

def storedetailfloralightview(request, pk):
    obj = User.objects.get(pk=pk)
    targetfloralight = FloraLightModel.objects.filter(floralightstoreid=obj)
    object = {
        'object':obj,
        'targetfloralight':targetfloralight
    }
    return render(request, 'register/storedetail_floralight.html', object)


def floralightmypageview(request, pk):
    obj = User.objects.get(pk=pk)
    allcheckcode = FloraLightModel.objects.values_list('floralightcheckcode', flat=True)
    allcheckcode_list = list(allcheckcode)
    if(request.method == 'POST'):
        a = str(request.POST['floralighttestid']) + str(request.POST['floralighttestpass'])

        if a in allcheckcode_list:
            data = FloraLightGetForm(request.POST, instance=obj)
            data.save()
            targetdna = FloraLightModel.objects.get(floralightcheckcode=a)
            ansno = targetdna.floralightansno
            name = targetdna.floralightname
            storeid = targetdna.floralightstoreid
            targetdata = User.objects.get(pk=pk)
            targetdata.floralightansno = ansno
            targetdata.floralighttestername = name
            targetdata.storeid = storeid
            targetdata.save()

            object = {
                'object':targetdata,
                'message':'検査結果'
            }
        else:
            return render(request, 'register/getmiss.html')
    return render(request, 'register/top.html', object)

def floralightmytestview(request, pk):
    object = User.objects.get(pk=pk)
    name = object.floralighttestername
    id = object.floralighttestid
    memo = "https://arr-works.com/with-portal/flora/fl_" + id + ".html"
    return render(request, 'register/floralight/floralightans.html', {'object':object, 'name':name, 'id':id, 'memo':memo})

def floralightmyteststoreview(request, pk):
    object = FloraLightModel.objects.get(pk=pk)
    name = object.floralightname
    id = object.floralighttestid
    memo = "https://arr-works.com/with-portal/flora/fl_" + id + ".html"
    return render(request, 'register/floralight/floralightans.html', {'object':object, 'name':name, 'id':id, 'memo':memo})

def floralightdetailview(request, pk):
    object_list = User.objects.get(pk=pk)
    object = {
        'object':object_list,
        'form':FloraLightGetForm()
    }

    return render(request, 'register/floralightdetail.html', object)

def floralightwebview(request, pk):
    obj = FloraLightModel.objects.get(pk=pk)
    id = obj.floralighttestid
    memo = "https://arr-works.com/with23/book/fl_w_" + id + ".pdf"
    return render(request, 'register/floralight/floralightweb.html', {'id': id,'memo': memo})

def storedetailfloraexpertview(request, pk):
    obj = User.objects.get(pk=pk)
    targetfloraexpert = FloraExpertModel.objects.filter(floraexpertstoreid=obj)
    object = {
        'object':obj,
        'targetfloraexpert':targetfloraexpert
    }
    return render(request, 'register/storedetail_floraexpert.html', object)


def floraexpertmypageview(request, pk):
    obj = User.objects.get(pk=pk)
    allcheckcode = FloraExpertModel.objects.values_list('floraexpertcheckcode', flat=True)
    allcheckcode_list = list(allcheckcode)
    if(request.method == 'POST'):
        a = str(request.POST['floraexperttestid']) + str(request.POST['floraexperttestpass'])

        if a in allcheckcode_list:
            data = FloraExpertGetForm(request.POST, instance=obj)
            data.save()
            targetdna = FloraExpertModel.objects.get(floraexpertcheckcode=a)
            ansno = targetdna.floraexpertansno
            name = targetdna.floraexpertname
            storeid = targetdna.floraexpertstoreid
            targetdata = User.objects.get(pk=pk)
            targetdata.floraexpertansno = ansno
            targetdata.floraexperttestername = name
            targetdata.storeid = storeid
            targetdata.save()

            object = {
                'object':targetdata,
                'message':'検査結果'
            }
        else:
            return render(request, 'register/getmiss.html')
    return render(request, 'register/top.html', object)

def floraexpertmytestview(request, pk):
    object = User.objects.get(pk=pk)
    name = object.floraexperttestername
    id = object.floraexperttestid
    memo = "register/floraexpert/" + str(object.floraexpertansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def floraexpertmyteststoreview(request, pk):
    object = FloraExpertModel.objects.get(pk=pk)
    name = object.floraexpertname
    id = object.floraexperttestid
    memo = "register/floraexpert/" + str(object.floraexpertansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def floraexpertdetailview(request, pk):
    object_list = User.objects.get(pk=pk)
    object = {
        'object':object_list,
        'form':FloraExpertGetForm()
    }

    return render(request, 'register/floraexpertdetail.html', object)

def storefloraexpertrepoview(request, pk):
    obj = FloraExpertModel.objects.get(pk=pk)
    id = obj.floraexperttestid
    memo = "https://arr-works.com/with23/book/fe_r_" + id + ".pdf"
    return render(request, 'register/floraexpert/floraexpertrepo.html', {'id': id,'memo': memo})

def floraexpertrepoview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.floraexperttestid
    memo = "https://arr-works.com/with23/book/fe_r_" + id + ".pdf"
    return render(request, 'register/floraexpert/floraexpertrepo.html', {'id': id,'memo': memo})

def floraexpertwebview(request, pk):
    obj = FloraExpertModel.objects.get(pk=pk)
    id = obj.floraexperttestid
    memo = "https://arr-works.com/with23/book/fe_w_" + id + ".pdf"
    return render(request, 'register/floraexpert/floraexpertweb.html', {'id': id,'memo': memo})

def storedetailfoodproteinview(request, pk):
    obj = User.objects.get(pk=pk)
    targetfoodprotein = FoodProteinModel.objects.filter(foodproteinstoreid=obj)
    object = {
        'object':obj,
        'targetfoodprotein':targetfoodprotein
    }
    return render(request, 'register/storedetail_foodprotein.html', object)


def foodproteinmypageview(request, pk):
    obj = User.objects.get(pk=pk)
    allcheckcode = FoodProteinModel.objects.values_list('foodproteincheckcode', flat=True)
    allcheckcode_list = list(allcheckcode)
    if(request.method == 'POST'):
        a = str(request.POST['foodproteintestid']) + str(request.POST['foodproteintestpass'])

        if a in allcheckcode_list:
            data = FoodProteinGetForm(request.POST, instance=obj)
            data.save()
            targetdna = FoodProteinModel.objects.get(foodproteincheckcode=a)
            ansno = targetdna.foodproteinansno
            name = targetdna.foodproteinname
            storeid = targetdna.foodproteinstoreid
            targetdata = User.objects.get(pk=pk)
            targetdata.foodproteinansno = ansno
            targetdata.foodproteintestername = name
            targetdata.storeid = storeid
            targetdata.save()

            object = {
                'object':targetdata,
                'message':'検査結果'
            }
        else:
            return render(request, 'register/getmiss.html')
    return render(request, 'register/top.html', object)

def foodproteinmytestview(request, pk):
    object = User.objects.get(pk=pk)
    name = object.foodproteintestername
    id = object.foodproteintestid
    memo = "register/foodprotein/" + str(object.foodproteinansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def foodproteinmyteststoreview(request, pk):
    object = FoodProteinModel.objects.get(pk=pk)
    name = object.foodproteinname
    id = object.foodproteintestid
    memo = "register/foodprotein/" + str(object.foodproteinansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def foodproteindetailview(request, pk):
    object_list = User.objects.get(pk=pk)
    object = {
        'object':object_list,
        'form':FoodProteinGetForm()
    }

    return render(request, 'register/foodproteindetail.html', object)

def foodproteinwebview(request, pk):
    obj = FoodProteinModel.objects.get(pk=pk)
    id = obj.foodproteintestid
    memo = "https://arr-works.com/with23/book/fp_w_" + id + ".pdf"
    return render(request, 'register/foodprotein/foodproteinweb.html', {'id': id,'memo': memo})

def storedetailotherview(request, pk):
    obj = User.objects.get(pk=pk)
    targetother = OtherModel.objects.filter(otherstoreid=obj)
    object = {
        'object':obj,
        'targetother':targetother
    }
    return render(request, 'register/storedetail_other.html', object)


def othermypageview(request, pk):
    obj = User.objects.get(pk=pk)
    allcheckcode = OtherModel.objects.values_list('othercheckcode', flat=True)
    allcheckcode_list = list(allcheckcode)
    if(request.method == 'POST'):
        a = str(request.POST['othertestid']) + str(request.POST['othertestpass'])

        if a in allcheckcode_list:
            data = OtherGetForm(request.POST, instance=obj)
            data.save()
            targetdna = OtherModel.objects.get(othercheckcode=a)
            ansno = targetdna.otheransno
            name = targetdna.othername
            storeid = targetdna.otherstoreid
            targetdata = User.objects.get(pk=pk)
            targetdata.otheransno = ansno
            targetdata.othertestername = name
            targetdata.storeid = storeid
            targetdata.save()

            object = {
                'object':targetdata,
                'message':'検査結果'
            }
        else:
            return render(request, 'register/getmiss.html')
    return render(request, 'register/top.html', object)

def othermytestview(request, pk):
    object = User.objects.get(pk=pk)
    name = object.othertestername
    id = object.othertestid
    memo = "register/other/" + str(object.otheransno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def othermyteststoreview(request, pk):
    object = OtherModel.objects.get(pk=pk)
    name = object.othername
    id = object.othertestid
    memo = "register/other/" + str(object.otheransno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def otherdetailview(request, pk):
    object_list = User.objects.get(pk=pk)
    object = {
        'object':object_list,
        'form':OtherGetForm()
    }

    return render(request, 'register/otherdetail.html', object)

def storeotherrepoview(request, pk):
    obj = OtherModel.objects.get(pk=pk)
    id = obj.othertestid
    memo = "https://arr-works.com/with23/book/o_r_" + id + ".pdf"
    return render(request, 'register/other/otherrepo.html', {'id': id,'memo': memo})

def otherrepoview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.othertestid
    memo = "https://arr-works.com/with23/book/o_r_" + id + ".pdf"
    return render(request, 'register/other/otherrepo.html', {'id': id,'memo': memo})

def otheradview(request, pk):
    obj = OtherModel.objects.get(pk=pk)
    id = obj.othertestid
    memo = "https://arr-works.com/with23/book/o_a_" + id + ".pdf"
    return render(request, 'register/other/otherad.html', {'id': id,'memo': memo})

def otherwebview(request, pk):
    obj = OtherModel.objects.get(pk=pk)
    id = obj.othertestid
    memo = "https://arr-works.com/with23/book/o_w_" + id + ".pdf"
    return render(request, 'register/other/otherweb.html', {'id': id,'memo': memo})

def storedetailbodyview(request, pk):
    obj = User.objects.get(pk=pk)
    targetstyle = StyleDnaModel.objects.filter(stylestoreid=obj)
    object = {
        'object':obj,
        'targetstyle':targetstyle
    }
    return render(request, 'register/storedetail_body.html', object)


def stylemypageview(request, pk):
    obj = User.objects.get(pk=pk)
    allcheckcode = StyleDnaModel.objects.values_list('stylecheckcode', flat=True)
    allcheckcode_list = list(allcheckcode)
    if(request.method == 'POST'):
        a = str(request.POST['styletestid']) + str(request.POST['styletestpass'])

        if a in allcheckcode_list:
            data = StyleGetForm(request.POST, instance=obj)
            data.save()
            targetdna = StyleDnaModel.objects.get(stylecheckcode=a)
            ansno = targetdna.styleansno
            name = targetdna.stylename
            storeid = targetdna.stylestoreid
            targetdata = User.objects.get(pk=pk)
            targetdata.styleansno = ansno
            targetdata.styletestername = name
            targetdata.storeid = storeid
            targetdata.save()

            object = {
                'object':targetdata,
                'message':'検査結果'
            }
        else:
            return render(request, 'register/getmiss.html')
    return render(request, 'register/top.html', object)

def stylemytestview(request, pk):
    object = User.objects.get(pk=pk)
    name = object.styletestername
    id = object.styletestid
    memo = "register/styledna/" + str(object.styleansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def stylemyteststoreview(request, pk):
    object = StyleDnaModel.objects.get(pk=pk)
    name = object.stylename
    id = object.styletestid
    memo = "register/styledna/" + str(object.styleansno) + ".html"
    return render(request, memo, {'object':object, 'name':name, 'id':id})

def styledetailview(request, pk):
    object_list = User.objects.get(pk=pk)
    object = {
        'object':object_list,
        'form':StyleGetForm()
    }

    return render(request, 'register/styledetail.html', object)

def stylepaperview(request, pk):
    obj = StyleDnaModel.objects.get(pk=pk)
    ansno = obj.styleansno
    memo = "https://arr-works.com/with23/book/d" + str(ansno) + ".pdf"
    return render(request, 'register/styledna/stylepaper.html', {'memo': memo})

def storestylerepoview(request, pk):
    obj = StyleDnaModel.objects.get(pk=pk)
    id = obj.styletestid
    date = obj.styledate
    memo = "https://arr-works.com/with23/book/d_r_" + id + ".pdf"
    return render(request, 'register/styledna/stylerepo.html', {'id': id,'memo': memo, 'date': date})

def storestyleadview(request, pk):
    obj = StyleDnaModel.objects.get(pk=pk)
    id = obj.styletestid
    date = obj.styledate
    memo = "https://arr-works.com/with23/book/d_a_" + id + ".pdf"
    return render(request, 'register/styledna/stylead.html', {'id': id,'memo': memo, 'date': date})

def stylewebview(request, pk):
    obj = StyleDnaModel.objects.get(pk=pk)
    id = obj.styletestid
    memo = "https://arr-works.com/with23/book/d_w_" + id + ".pdf"
    return render(request, 'register/styledna/styleweb.html', {'id': id,'memo': memo})

def stylerepoview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.styletestid
    targetstyle = StyleDnaModel.objects.get(styletestid = obj.styletestid)
    date = targetstyle.styledate
    memo = "https://arr-works.com/with23/book/d_r_" + id + ".pdf"
    return render(request, 'register/styledna/stylerepo.html', {'id': id,'memo': memo, "date": date})

def styleadview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.styletestid
    targetstyle = StyleDnaModel.objects.get(styletestid = obj.styletestid)
    date = targetstyle.styledate
    memo = "https://arr-works.com/with23/book/d_a_" + id + ".pdf"
    return render(request, 'register/styledna/stylead.html', {'id': id,'memo': memo, "date": date})

def skinrepoview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.skintestid
    targetskin = SkinDnaModel.objects.get(skintestid = obj.skintestid)
    date = targetskin.skindate
    memo = "https://arr-works.com/with23/book/s_r_" + id + ".pdf"
    return render(request, 'register/skindna/skinrepo.html', {'id': id,'memo': memo, "date": date})

def skinadview(request, pk):
    obj = User.objects.get(pk=pk)
    id = obj.skintestid
    targetskin = SkinDnaModel.objects.get(skintestid = obj.skintestid)
    date = targetskin.skindate
    memo = "https://arr-works.com/with23/book/s_a_" + id + ".pdf"
    return render(request, 'register/skindna/skinad.html', {'id': id,'memo': memo, "date": date})

