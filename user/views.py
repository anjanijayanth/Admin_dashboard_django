from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, Organization, AgentDetail, AgencyDetail, StaffDetail, AgentStatusLogs
from django.core.paginator import Paginator


def my_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home page if user is authenticated
    else:
        return redirect('login')

def profile_view(request):
    return render(request, "home/user_profile.html", {'status_str':User.ROLE_CHOICES} )



def custom_page_not_found_view(request, exception):
    return render(request, "error_pages/page-404.html", {})
def custom_error_view(request, exception=None):
    return render(request, "error_pages/page-500.html", {})
def custom_permission_denied_view(request, exception=None):
    return render(request, "error_pages/page-403.html", {})


def login_view(request):
    msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.role in [User.ADMIN_STAFF,User.SUPER_ADMIN] :
                login(request, user)
                return redirect('home')  # Redirect to home page after login
        else:
            msg = 'Invalid credentials'
    return render(request, 'login_page/login.html', {'msg':msg})

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))  # Redirect to login page after logout

@login_required
def dashboard(request):
    cards={}
    cards["No. of Organizations"]= str(Organization.objects.count())
    cards["No. of Agencies"]= str(AgencyDetail.objects.count())
    cards["No. of Agents"]= str(AgentDetail.objects.count())
    cards["No. of Staff Members"]= str(StaffDetail.objects.count())
    return render(request,'home/dashboard.html', {'cards':cards} )

@login_required
def staff_detail(request):
    staff= StaffDetail.objects.all()
    # print(staff[0].agency)
    return render(request, 'home/staff_details.html', {'staff_details':staff} )

def staff_search(request): #agency_search
    if request.htmx:
      search = request.GET.get('search_q')
      page_num = request.GET.get('page', 1)
      if search:
          q_logs = StaffDetail.objects.filter(user__name__icontains=search)
      else:
          q_logs = StaffDetail.objects.all()
      page = Paginator(object_list=q_logs, per_page=5).get_page(page_num)
      return render( request, 'home/staff_search_results.html', {'staff_q_page':page})



@login_required
def agent_logs(request):
    logs=AgentStatusLogs.objects.all()
    return render(request, 'home/agent_logs.html', {  'agent_logs':logs, 'status_str':AgentDetail.STATUS_CHOICES} )

def partial_search_logs(request): #agentlogs_search
    if request.htmx:
      search = request.GET.get('search_q')
      page_num = request.GET.get('page', 1)
      if search:
          q_logs = AgentStatusLogs.objects.filter(agent__user__name__icontains=search)
      else:
          q_logs = AgentStatusLogs.objects.all()
      page = Paginator(object_list=q_logs, per_page=5).get_page(page_num)
      return render( request, 'home/agent_log_partial_results.html', {'agent_q_logs_page':page, 'status_str':AgentDetail.STATUS_CHOICES})


@login_required
def agency_detail(request):
    agency_details= AgencyDetail.objects.all()
    return render(request, 'home/agency_details.html', {'agency_detail':agency_details} )

def agency_search(request): #agency_search
    if request.htmx:
      search = request.GET.get('search_q')
      page_num = request.GET.get('page', 1)
      if search:
          q_logs = AgencyDetail.objects.filter(agency_name__icontains=search)
      else:
          q_logs = AgencyDetail.objects.all()
      page = Paginator(object_list=q_logs, per_page=5).get_page(page_num)
      return render( request, 'home/agency_partial_results.html', {'agency_q_page':page})


@login_required
def org_detail(request):
    orgs= Organization.objects.all()
    return render(request, 'home/org_details.html', {'org_details':orgs} )


@login_required
def agent_detail(request):
    orgs= AgentDetail.objects.all()
    return render(request, 'home/agent_details.html', {'agent_details':orgs, 'status_str':AgentDetail.STATUS_CHOICES} )

def agent_search(request): #agency_search
    if request.htmx:
      search = request.GET.get('search_q')
      page_num = request.GET.get('page', 1)
      if search:
          q_logs = AgentDetail.objects.filter(user__name__icontains=search)
      else:
          q_logs = AgentDetail.objects.all()
      page = Paginator(object_list=q_logs, per_page=5).get_page(page_num)
      return render( request, 'home/agent_search_results.html', {'agent_q_page':page, 'status_str':AgentDetail.STATUS_CHOICES})



# @login_required
# def update_or_create_org(request, pk=None):
#     org_instance= None
#     if pk:  #editing existing
#         org_instance = Organization.objects.get(pk=pk)
#     else:  # creating new
#         org_instance = None

#     form = forms.Org_Form(request.POST or None, instance=org_instance)
#     if form.is_valid():
#         form.save()
#         return redirect('org_detail')  # Redirect to success page or URL

#     return render(request, 'home/forms.html', {'form': form})


@login_required
def update_or_create_org(request, pk=None):
    if request.method == 'POST':
        data = {
                'domain':  request.POST.get('domain'),
                'orgranization_name':  request.POST.get('orgranization_name'),
                'country' :  request.POST.get('country'),
                'status' : True if request.POST.get('status')=='on' else False,
                'city' :  request.POST.get('city'),
                'local_gov_area' :   request.POST.get('local_gov_area'),
                'address' :   request.POST.get('address'),
                'zipcode' :  request.POST.get('zipcode'),
                'website' :   request.POST.get('website'),
                'logo' :  request.POST.get('logo'),
                'cpysource' :  request.POST.get('cpysource'),
                'affid' :  request.POST.get('affid'),
                'domainurl' :  request.POST.get('domainurl'),
                'notifcatione_mail' :  request.POST.get('notifcatione_mail'),
                'payment_notification_email' :  request.POST.get('payment_notification_email')
                }

        if pk:
            record = Organization.objects.filter(pk=pk)
            record.update(**data)
        else:
            record = Organization.objects.create(**data)
            record.save()
        return redirect('org_detail')
        
    else:
        if pk:
            record = Organization.objects.get(pk=pk)
            context = {'record': record}
        else:
            context = {}

        return render(request, 'home/org_form.html', context)
    

