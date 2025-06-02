from django.shortcuts import render, redirect, get_object_or_404
from .models import UserDoctor, Post, Comment,Booking
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from django.utils.text import slugify
from .forms import UserLoginForm,PostCreateUpdateForm,UserRegistrationForm,CommentCreateForm,BookingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Relation
from django.contrib.auth import views as auth_views

def Home(request):
    return render(request, 'appointments/home.html')

from django.shortcuts import render, redirect
from .models import UserDoctor
from django.contrib.auth.decorators import login_required

@login_required
def booking(request):
    doctors = UserDoctor.objects.all()
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes')
        doctor_id = request.POST.get('doctor')
        
        if not all([full_name, phone, email, date, time, doctor_id]):
            error = "لطفا همه فیلدهای ضروری را پر کنید."
            return render(request, 'appointments/booking.html', {'doctors': doctors, 'error': error})

        try:
            doctor = UserDoctor.objects.get(id=doctor_id)
        except UserDoctor.DoesNotExist:
            error = "دکتر انتخاب شده معتبر نیست."
            return render(request, 'appointments/booking.html', {'doctors': doctors, 'error': error})

        Booking.objects.create(
            user=request.user,
            patient_name=full_name,
            phone_number=phone,
            doctor=doctor,
            date=date,
            time=time,
            notes=notes
        )
        
        return redirect('appointments:booking_success')  
    return render(request, 'appointments/booking.html', {'doctors': doctors})


def booking_success(request):
    return render(request, 'appointments/booking_success.html')


def medicines(request):
    return render(request, 'appointments/medicines.html')

#def login(request):
    #if request.method == 'POST':
        #name = request.POST.get('name')
        #password = request.POST.get('password')
        #user = authenticate(username=name, password=password)

        #if user is not None:
            #django_login(request, user)
            #messages.success(request, "با موفقیت وارد شدید.")
            #return redirect('home')
        #else:
            #messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
            #return redirect('login')

    #return render(request, 'appointments/login.html')

def doctors_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'GET':
        return render(request, 'appointments/doctors_detail.html', {'post': post})

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'برای ثبت نظر باید وارد شوید.')
            return redirect('login')

        body = request.POST.get('body', '')
        title = request.POST.get('title', 'بدون عنوان')

        try:
            doctor = UserDoctor.objects.get(user=request.user)
        except UserDoctor.DoesNotExist:
            return render(request, 'appointments/doctors_detail.html', {
                'post': post,
                'error': 'شما دکتر نیستید و نمی‌توانید نظر ثبت کنید.'
            })

        Comment.objects.create(
            body=body,
            title=title,
            author=doctor,
            post=post
        )

        messages.success(request, 'نظر شما با موفقیت ثبت شد.')
        return render(request, 'appointments/doctors_detail.html', {'post': post})

#def logout(request):
    #django_logout(request)
    #messages.success(request, 'شما با موفقیت خارج شدید.')
    #return redirect('login')
#def register(request):
    #if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'signed up successfully')
            return redirect(reverse('login'))
        else:
            return render(request, 'appointments/register.html', {'form':form})
    #else:
        form = UserCreationForm()
        return render(request, "appointments/register.html", {"form": form})

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'appointments/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('appointments:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username=cd['username'],
                email=cd['email'],
                password=cd['password1']
            )
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
            return redirect('appointments:login')
        return render(request, self.template_name, {'form': form})

    
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'appointments/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('appointments:home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید.')
                return redirect('appointments:home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        return render(request, self.template_name, {'form': form})
    
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logout successfuly', 'success')
        return redirect('appointments:home')
    

class UserDoctoreView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.all()  # همه پست‌ها را می‌گیریم

        # اگر می‌خواهید نشان دهید که آیا کاربر دکتر است یا خیر:
        try:
            doctor = UserDoctor.objects.get(user=user)
        except UserDoctor.DoesNotExist:
            doctor = None

        is_following = False  # یا مقدار درست را اینجا بگذارید

        return render(request, 'appointments/doctors.html', {
            'user': user,
            'posts': posts,
            'is_following': is_following,
            'doctor': doctor,
        })

    def post(self, request):
        user = request.user
        try:
            doctor = UserDoctor.objects.get(user=user)
        except UserDoctor.DoesNotExist:
            doctor = None

        if not doctor:
            return redirect('appointments:doctors')

        body = request.POST.get('body')
        if body:
            post = Post.objects.create(
                author=doctor,
                title=body[:50],
                body=body
            )
            post.save()

        posts = Post.objects.all()

        return render(request, 'appointments/doctors.html', {
            'user': user,
            'posts': posts,
            'is_following': False
        })




class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'appointments/password_reset.html'
    email_template_name = 'appointments/password_reset_email.html'
    success_url = reverse_lazy('appointments:password_reset_done')

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'appointments/password_reset_done.html'
    
class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'appointments/password_reset_confirm.html'
    success_url = reverse_lazy('appointments:password_reset_complete')
    
class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'appointments/password_reset_complete.html'
    
class UserFollowView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            messages.error(request, 'you are already following this user', 'danger')
        else:
            Relation(from_user = request.user , to_user = user).save()
            messages.success(request, 'you are now following this user', 'success')
        return redirect('appointments:doctors', user_id=user_id)
    
class UserUnfollowView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you are now unfollowing this user', 'success')
        else:
            messages.error(request, 'you are not following this user', 'danger')
        return redirect('appointments:doctors', user_id=user_id)
    
class PostDetailView(View):
    form_class = CommentCreateForm
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comments = post.pcomments.filter(is_reply = False)
        return render(request , 'appointments/detail.html', {'post':post , 'comments':comments, 'form':self.form_class})
    
class PostDeleteView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post deleted successfully', 'success')
            return redirect('appointments:appointments')
        else:
            messages.error(request, 'you are not the owner of this post', 'danger')
            return redirect('appointments:appointments')
        
class PostUpdateView(View):
    form_class = PostCreateUpdateForm
    
    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'you cant update this post', 'danger')
            return redirect('appointments:appointments')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'appointments/update.html', {'form':form})
    
    def post(self,request):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit = False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'post updated successfully', 'success')
            return redirect('appointments:post_detail', post.id,post.slug )
        
class PostCreateView(View):
    form_class = PostCreateUpdateForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'appointments/create.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'post created successfully', 'success')
            return redirect('appointments:post_detail', new_post.id, new_post.slug)