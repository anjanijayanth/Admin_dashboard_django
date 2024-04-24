from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.



class Organization(models.Model):
    domain = models.CharField(max_length=100, unique=True, primary_key=True)
    orgranization_name = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    status = models.BooleanField(default=True)
    city = models.CharField(max_length=50, null=False, blank=False)
    local_gov_area = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    zipcode = models.CharField(max_length=150, null=False, blank=False)
    website = models.CharField(max_length=100, blank=True)
    logo = models.CharField(max_length=1000,  blank=True)
    cpysource = models.CharField(max_length=1000, null=False, blank=False)
    affid = models.CharField(max_length=1000, blank=True)
    domainurl = models.CharField(max_length=1000, null=False, blank=False)
    notifcatione_mail = models.EmailField(null=True)
    payment_notification_email = models.EmailField(null=True)


    class Meta:
        db_table = "orgranization"
    def __str__(self):
        return self.orgranization_name


class AgencyDetail(models.Model):
    agency_name = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    status = models.BooleanField(default=True)
    city = models.CharField(max_length=50, null=False, blank=False)
    local_gov_area = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=False)
    zipcode = models.CharField(max_length=10, null=True)
    website = models.CharField(max_length=100, null=True)
    logo = models.CharField(max_length=1000, null=True)
    cpysource = models.CharField(max_length=1000, null=True)
    affid = models.CharField(max_length=1000, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    is_country_editable = models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default='TS_NG')


    class Meta:
        db_table = "agency_detail"


class User(AbstractUser):
    
    ORGANIZATION_ADMIN = 1
    ORGANIZATION_STAFF = 2
    AGENT = 3
    SUB_AGENT = 4
    STAFF = 5
    SUPER_ADMIN = 6
    ADMIN_STAFF = 7

    

    ROLE_CHOICES = [(SUPER_ADMIN, "super-admin"),
                    (ADMIN_STAFF, "ts-employee"),
                    (ORGANIZATION_ADMIN, "org-admin"),
                    (ORGANIZATION_STAFF, "org-staff"),
                    (AGENT, "agent"),
                    (SUB_AGENT, "sub-agent"),
                    (STAFF, "staff")]

    email = models.EmailField()
    name = models.CharField(max_length=25)
    # username = models.CharField(blank=True, null=True)
    country_code = models.CharField(max_length=5, null=True, default=None, help_text="do not add + extension")
    mobile_number = models.CharField(max_length=15, null=True, default=None, help_text="do not add country code")
    phone_number = models.CharField(max_length=15, null=True, default=None, help_text="landline number")
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=6)
    is_user_activated = models.BooleanField(default=False)
    is_mail_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, default=None)
    otp_created_time = models.DateTimeField(null=True, default=None)
    is_company = models.BooleanField(default=True)
    agency = models.ForeignKey(AgencyDetail, on_delete=models.CASCADE, null=True, default=None)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default='TS_NG',null=True)

    class Meta:
        db_table = "user"
        unique_together = ('email', 'organization')
    def __str__(self):
        return self.name


class AgentDetail(models.Model):

    INACTIVE = 0
    ACTIVE = 1
    UNDER_VERIFICTION = 2 
    APPROVED = 3
    REJECTED = 4

    STATUS_CHOICES = [
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (UNDER_VERIFICTION, 'Under Verification'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_user', blank=False, null=False)
    agency = models.ForeignKey(AgencyDetail, on_delete=models.CASCADE, related_name='agent_agency', blank=False, null=False)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name='agent_to_parent')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=2)
    # verified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name='agent_verified_by')

    class Meta:
        db_table = "agent_detail"


class AgentStatusLogs(models.Model):
    agent = models.ForeignKey(AgentDetail, on_delete=models.CASCADE, related_name='agent_status', blank=False, null=False)
    status = models.PositiveSmallIntegerField(choices=AgentDetail.STATUS_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_updated_by', blank=False, null=False)
    note = models.TextField(null=True)

    class Meta:
        db_table = "agent_status_log"


class StaffDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_details')
    parent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name='staff_to_parent')
    agency = models.ForeignKey(AgencyDetail, on_delete=models.CASCADE, related_name='staff_agency')
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    zipcode = models.CharField(max_length=10)

    class Meta:
        db_table = "staff_detail"


class Product(models.Model):
    name = models.CharField(max_length=50, default="Flight")
    desc = models.TextField(null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'product'


class Module(models.Model):
    module_name = models.CharField(max_length=200, blank=False, null=False)
    module_description = models.TextField(blank=True, null=True, default=None)
    status = models.BooleanField(default=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_updated_by', unique=False, null=True, default=None)
    last_modified = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "module"


class PermissionRule(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module_permission')
    permission_name = models.CharField(max_length=200, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_permission', null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    status = models.BooleanField(default=True)
    for_agent = models.BooleanField(default=False)  
    for_tsemployee = models.BooleanField(default=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rules_updated_by', unique=False, null=True, default=None)
    last_modified = models.DateTimeField(default=timezone.now)



    class Meta:
        db_table = "permission_rule"


class UserPermission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, unique=False)
    permission = models.ForeignKey(PermissionRule, on_delete=models.CASCADE, unique=False)
    read_permission = models.BooleanField(default=False, null=False, blank=False)
    write_permission = models.BooleanField(default=False, null=False, blank=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_permission_updated_by')


    class Meta:
        db_table = "user_permission"
