from django.db import models
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Max
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Create your models here.

class Superadmin(models.Model):
    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    password = models.CharField(max_length=255)
    profile = models.CharField(default='superadmin') 
    @property
    def is_authenticated(self):
        return True 
    class Meta:
        db_table = 'superadmin'   

    def __str__(self):
        return self.username

    
class Enquiry(models.Model):
    enquiry_id = models.CharField(primary_key=True, max_length=20,unique=True,null=False)
    name = models.CharField(null=True, max_length=30)
    process_name = models.CharField(null=True, max_length=30)
    disease = models.CharField(null=True, max_length=30)
    created_at = models.DateTimeField(default=now, null=True)  # Temporarily allow null and use default
    source = models.CharField(max_length=500, null=False)  
    patient_id = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=255, null=True)
    phone_number = models.CharField(null=True,max_length=20)
    address = models.TextField(null=True)
    sub_disease = models.CharField(max_length=20,null=True, blank=True)
    organ = models.CharField(max_length=255)
    dme_message = models.TextField(null=True)
    date = models.CharField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    time = models.TimeField(null=True)
    country = models.CharField(null=True)
    working = models.BooleanField(default=True)
    dme = models.CharField(null=True) #user_id of the dme assigned. 
    calling_agent = models.CharField(null=True)
    landing_page = models.URLField(max_length=255, null=True)
    utm_source = models.CharField(max_length=255, null=True)
    utm_campaign = models.CharField(max_length=255, null=True)
    utm_ad = models.CharField(max_length=255, null=True)
    utm_keywords = models.CharField(max_length=255, null=True)
    utm_browser = models.CharField(max_length=255, null=True)
    utm_device = models.CharField(max_length=255, null=True)
    utm_ip_address = models.GenericIPAddressField(null=True)
    interactions = models.JSONField(null=True)
    utm_others = models.TextField(null=True)
    status = models.CharField(max_length=50,default="chat")
    conversion_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    products = models.JSONField(null=True)
    type = models.CharField(default="Aquisition",max_length=100, choices=[("Aquisition", "Aquisition"), ("Retention", "Retention")])  # Country of the enquiry
    failed_deals = models.JSONField(null=True)
    demographics = models.JSONField(null=True)
    app = models.JSONField(null=True)
    duplicate = models.BooleanField(default=False)
    retention = models.JSONField(null=True)
    visit_history = models.JSONField(null=True)
    agent = models.JSONField(null=True)
    counter = models.PositiveIntegerField(default=0, editable=False)  # Auto-incrementing counter

    def save(self, *args, **kwargs):
        # Generate enquiry_id if not already set
        if not self.enquiry_id:

            ten_days_ago = now() - timedelta(days=10)             # Check if an enquiry with the same criteria exists within the last 10 days
            recent_enquiry = Enquiry.objects.filter(
                name=self.name,
                phone_number=self.phone_number,
                disease= self.disease,
                created_at__gte=ten_days_ago
            ).exists()

            if recent_enquiry:
                self.duplicate = True


            # Get today's date in DDMM format
            today_date = now().strftime("%d%m")
            if not ( self.name and self.phone_number and self.type):
                raise ValueError("Invalid: Either name, type, or phone_number doens't exists.")
            # Fetch existing enquiries with the same disease code
            # Sort the query set by the numeric part of enquiry_id
            max_counter = Enquiry.objects.aggregate(Max('counter'))['counter__max'] or 0
            self.counter = max_counter + 1

            # we are getting process_name from DMEs and Calling agents already, this if is only for Meta, where we'll get process name from source name. 
            if not self.process_name: 
                self.source
                source = Source.objects.get(pk=self.source)
                process_name = source.process_name
                #storing process name in the enquiry.
                self.process_name = process_name
            

            self.enquiry_id = f"EQ{today_date}{self.process_name[:3]}000{self.counter}"



            calling_agent = (
            CallingAgent.objects.filter(process_name__contains=self.process_name)
            .order_by('updated_at')
            .first())

            if calling_agent:
                self.callingagent = calling_agent.user_id
                print(calling_agent.user_id) 
                channel_layer = get_channel_layer()
                group_name = f"callingagent_{calling_agent.user_id}"


                
                data_to_ws = {
                            "address": getattr(self, "address", "N/A"),
                            "date": getattr(self, "date", "N/A"),
                            "disease": getattr(self, "disease", "N/A"),
                            "dme_message": getattr(self, "dme_message", "N/A"),
                            "duplicate": getattr(self, "duplicate", False),
                            "enquiry_id": getattr(self, "enquiry_id", "N/A"),
                            "name": getattr(self, "name", "N/A"),
                            "status": getattr(self, "status", "Pending"),
                            "phone_number": getattr(self, "phone_number", "Unknown"),
                            "sub_disease": getattr(self, "sub_disease", []),  # Default to an empty list
                            "working": getattr(self, "working", False),
                        }


                async_to_sync(channel_layer.group_send)(
                            group_name,
                            {
                                "type": "send_notification",
                                "message": data_to_ws,
                            }
                        )
                

                # Add the user_id to the enquiry field (assuming it's a list).
                enquiry_field = calling_agent.enquiry or []  # Ensure it's a list.
                enquiry_field.append(self.enquiry_id)  # Add user_id to the list.
                calling_agent.enquiry = enquiry_field

                # Update the updated_at field to the current time.
                calling_agent.updated_at = now()

                # Save the changes.
                calling_agent.save()
                team_leader_id = calling_agent.team_leader
                process_head_id = calling_agent.process_head

                # Assuming team_leader and process_head are instances of models that have an `enquiry` field.
                team_leader = teamleader.objects.get(pk=team_leader_id)
                if team_leader:
                    # Ensure the enquiry field is a list and append the enquiry_id.

                    team_leader_enquiry_field = team_leader.enquiry or []
                    team_leader_enquiry_field.append(self.enquiry_id)
                    team_leader.enquiry = team_leader_enquiry_field
                    team_leader.save()

                process_head = Processhead.objects.get(pk=process_head_id)
                if process_head:
                    # Ensure the enquiry field is a list and append the enquiry_id.
                    process_head_enquiry_field = process_head.enquiry or []
                    process_head_enquiry_field.append(self.enquiry_id)
                    process_head.enquiry = process_head_enquiry_field
                    process_head.save()


            else:
                raise ValueError("No calling agent found for the given process name")






        else:
            print('else working')


        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return self.enquiry_id

    class Meta:
        db_table = 'enquiry'

    



class Processhead(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)  # Unique ID for the agent
    name = models.CharField(max_length=255)  # Name of the process head
    enquiry = models.JSONField(null=True, default=dict, blank=True) # list of enquiries agent got. 
    password = models.CharField(max_length=255)
    kras = models.JSONField(null=True, default=dict, blank=True)  # Permissions assigned by super admin

    process_name = models.JSONField(null=True) #name of the process headed by the process-head. 
    is_enabled = models.BooleanField(default=True)  # Enable or disable login for the agent
    login_times = models.JSONField(null=True)  # History of all login and logout times
    permissions = models.JSONField(null=True)  # Permissions assigned by super admin
    department = models.CharField(editable=False, default="Calling")  # Department name
    targets = models.JSONField(null=True)  # Targets assigned to the agent and achieved percentage
    conversion_rate = models.JSONField(null=True)  # Monthly conversion rate data, including current month
    failed_deals = models.JSONField(null=True) #list of all enquiries that couldn't convert. 
    profile = models.CharField(editable=False,default='processhead') #
    counter = models.PositiveIntegerField(default=0, editable=False)  # Auto-incrementing counter

    class Meta:
        db_table = 'processhead'

    @property
    def is_authenticated(self):
        return self.is_enabled  # Assuming 'is_enabled' determines if the user is authenticated or not





class teamleader(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True,unique=True)  # Unique ID for the TL
    name = models.CharField(max_length=255)  # Name of the TL
    password = models.CharField(max_length=255)
    process_name = models.JSONField(null=True) #name of the process headed by the process-head. 
    enquiry = models.JSONField(null=True, default=dict, blank=True) # list of enquiries agent got. 
    kras = models.JSONField(null=True, default=dict, blank=True)  # Permissions assigned by super admin

    is_enabled = models.BooleanField(default=True)  # Enable or disable login for the TL
    login_times = models.JSONField(null=True)  # History of all login and logout times
    permissions = models.JSONField(null=True)  # Permissions assigned by super admin
    department = models.CharField(max_length=50, default="Calling")  # Department name
    process_head = models.CharField(max_length=50, null=True)
    targets = models.JSONField(null=True)  # Targets assigned to the agent and achieved percentage
    conversion_rate = models.JSONField(null=True)  # Monthly conversion rate data, including current month
    failed_deals = models.JSONField(null=True) #list of all enquiries that couldn't convert. 
    profile = models.CharField(default='teamleader') #
    counter = models.PositiveIntegerField(default=0, editable=False)  # Auto-incrementing counter

    class Meta:
        db_table = 'teamleader'
    
    @property
    def is_authenticated(self):
        return self.is_enabled  # Assuming 'is_enabled' determines if the user is authenticated or not



class CallingAgent(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True,unique=True)  # Unique ID for the agent
    password = models.CharField(max_length=255,default='krmcrm123')
    name = models.CharField(max_length=30 , null=True)
    is_enabled = models.BooleanField(default=True)  # Enable or disable login for the agent
    process_name = models.JSONField(null=True) #list of name  of the process headed by the process-head. 
    enquiry = models.JSONField(null=True, default=dict, blank=True) # list of enquiries agent got. 
    color = models.CharField(max_length=100,blank=True,null=True, choices=[("red", "red"), ("yellow", "yellow"), ("green", "green")])
    login_times = models.JSONField(null=True, default=dict, blank=True)  # History of all login and logout times
    permissions = models.JSONField(null=True, default=dict, blank=True)  # Permissions assigned by super admin
    kras = models.JSONField(null=True, default=dict, blank=True)  # Permissions assigned by super admin
    updated_at = models.DateTimeField(default=now, null=True)
    department = models.CharField(max_length=50, default="Calling")  # Department name
    team_leader = models.CharField(null=True, blank=True)  # ID and name of the team leader
    process_head = models.CharField(null=True, blank=True)  # ID and name of the process head
    targets = models.JSONField(null=True, default=dict, blank=True)  # Targets assigned to the agent and achieved percentage
    interactions = models.JSONField(null=True, default=dict, blank=True)  # Data of enquiry that interacted with the agent
    conversion_rate = models.JSONField(null=True, default=dict, blank=True)  # Monthly conversion rate data, including current month
    failed_deals = models.JSONField(null=True, default=dict, blank=True)  # list of all enquiries that the agent didn't convert
    orders = models.JSONField(null=True, default=dict, blank=True) #list of all the orders placed by the calling agent. 
    attendance = models.JSONField(null=True, default=dict, blank=True)  # Data of all present and absent days for this and previous months
    profile = models.CharField(default='callingagent') #
    counter = models.PositiveIntegerField(default=0, editable=False)  # Auto-incrementing counter

    @property
    def is_authenticated(self):
        return self.is_enabled

    class Meta:
        db_table = 'callingagent'





class DispatchAgent(models.Model):
    user_id = models.CharField(max_length=20,primary_key=True)  # Unique ID for the delivery agent
    name = models.CharField(max_length=30 , null=True)
    password = models.CharField(max_length=255)
    kras = models.JSONField(null=True, default=dict, blank=True)  # Permissions assigned by super admin
    is_enabled = models.BooleanField(default=True)  # Enable or disable login for the agent
    deliveries = models.JSONField(null=True)  # Details of parcels delivered
    products = models.JSONField(null=True)  # Products delivered during the delivery
    orders = models.JSONField(null=True)  # List of orders the agent is working on.
    profile = models.CharField(max_length=30, default='dispatchagent') #department of the agent. 
    counter = models.PositiveIntegerField(default=0, editable=False)  # Auto-incrementing counter

    @property
    def is_authenticated(self):
        return self.is_enabled

    def __str__(self):
        return self.delivery_id
    
    class Meta:
        db_table = 'dispatchagent'



class Source(models.Model):
    name = models.CharField(max_length=100, primary_key=True)  # Admin-created name for specific types of enquiry
    process_name = models.CharField(max_length=50, null=True)
    platform = models.CharField(max_length=100, choices=[('website', 'Website'),('youtube', 'YouTube'),('instagram', 'Instagram'),('google', 'Google'),('facebook', 'Facebook'),('call', 'Call'),])  # Platform where enquiry initiated contact
    platform_link = models.CharField(max_length=200)  # Link or action point of the platform
    medium = models.CharField(max_length=100, choices=[('chat', 'Chat'),('phone', 'Phone'),('webform', 'Webform')])  
    enquiry_type = models.CharField(max_length=10, choices=[("Organic", "Organic"), ("Inorganic", "Inorganic")])  # Organic or inorganic enquiry
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Budget for inorganic enquiry
    spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Budget for inorganic enquiry
    dmes = models.JSONField(default=dict, null=True, blank=True)
    

    def __str__(self):
        return f"{self.name} - {self.platform}"

    def save(self, *args, **kwargs):
        # Ensure budget is only entered for Inorganic enquiry
        if self.enquiry_type == "Organic":
            self.budget = None
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'source'

class dme(models.Model):
    user_id = models.CharField(primary_key=True,max_length=20, unique=True,blank=False,null=False)  # Unique ID for the agent
    password = models.CharField(max_length=255, default='krmcrm123')
    name = models.CharField(max_length=30, null=True)
    kras = models.JSONField(null=True, default=dict, blank=True)  # Permissions assigned by super admin

    is_enabled = models.BooleanField(default=True)  # Enable or disable login for the agent
    enquiry = models.JSONField(null=True, default=dict, blank=True)  # List of enquiries agent got
    color = models.CharField(
        max_length=100, blank=True, null=True,
        choices=[("red", "red"), ("yellow", "yellow"), ("green", "green")]
    )
    login_times = models.JSONField(null=True, default=dict, blank=True)  # History of all login and logout times
    permissions = models.JSONField(null=True, default=dict, blank=True)  # Permissions assigned by super admin
    department = models.CharField(max_length=50, default="Digital")  # Department name
    attendance = models.JSONField(null=True, default=dict, blank=True)  # Attendance data
    profile = models.CharField(max_length=50, default='dme')
    counter = models.PositiveIntegerField(default=0, editable=False)  # Auto-incrementing counter

    # def save(self, *args, **kwargs):
    #     if not self.user_id:  # Only generate user_id if it's not already set
    #         last_user = dme.objects.order_by('-user_id').first()
    #         if last_user and last_user.user_id.startswith("CLAQKD"):
    #             last_number = int(last_user.user_id[6:])
    #             new_number = str(last_number + 1).zfill(3)
    #         else:
    #             new_number = "001"
    #         self.user_id = f"CLAQKD{new_number}"
    #     super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        return self.is_enabled  # Assuming 'is_enabled' determines if the user is authenticated or not

    

    class Meta:
        db_table = 'dme'



class process(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    country = models.CharField(max_length=100, choices=[("India", "India"), ("USA", "USA"), ("UK", "UK"), ("Other", "Other")])  # Country of the enquiry
    disease = models.CharField(null=True)
    type = models.CharField(max_length=100, choices=[("Aquisition", "Aquisition"), ("Retention", "Retention")])  # Country of the enquiry
    created_at = models.DateTimeField(default=now, null=True)
    counter = models.PositiveIntegerField(default=0, editable=False)  # Auto-incrementing counter

    class Meta:
        db_table = 'process'  

    
class disease(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    sub_disease = models.JSONField(null=True) #List of all the sub-disease inside the disease
    medicines = models.JSONField(null=True) #
    class Meta:
        db_table = 'disease'  

# medicines = [{"medicine_code":"CSJ1221","strength":"major"},{"medicine_code":"CSSDFF1221","strength":"minor"}]



class jdlead(models.Model):
    leadid = models.CharField(max_length=255, unique=True)
    leadtype = models.CharField(max_length=255)
    prefix = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=255,blank=True, null=True)
    area = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=255,blank=True, null=True)
    brancharea = models.CharField(max_length=255,blank=True, null=True)
    dncmobile = models.IntegerField(blank=True, null=True)
    dncphone = models.IntegerField(blank=True, null=True)
    company = models.CharField(max_length=255,blank=True, null=True)
    pincode = models.CharField(max_length=10,blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    branchpin = models.CharField(max_length=6,blank=True, null=True)
    parentid = models.CharField(max_length=255,blank=True, null=True)
    contacted = models.BooleanField(default=False,blank=True, null=True)  # True if lead was contacted, False otherwise
    contacted_on = models.CharField(blank=True,null=True) #date time when the agent tick the "contacted" box. 
    interested = models.CharField(max_length=100, blank=True, null=True, choices=[("interested", "interested"), ("not-interested", "not-interested")])


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'jdlead'


class Medicine(models.Model):
    
    name = models.CharField(max_length=255)  # Medicine name
    medicine_code = models.CharField(max_length=100, unique=True,primary_key=True)  # Unique code for medicine
    organs = models.JSONField()  # List of organs the medicine is effective on
    countries = models.JSONField()  # List of countries where medicine is available
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the medicine
    margin = models.DecimalField(max_digits=5, decimal_places=2)  # Margin on the medicine
    out_of_stock = models.BooleanField(default=False)  # Whether the medicine is out of stock

    def __str__(self):
        return f"{self.name} ({self.code})"
    class Meta:
        db_table = 'medicine'



class Hospital(models.Model):
    hospital_id = models.CharField(max_length=20, primary_key=True)  # Unique ID for each hospital
    receptionist_id = models.CharField(max_length=20)  # Unique ID for each receptionist
    location = models.CharField(max_length=255)  # Location of the hospital
    doctor = models.JSONField(null=True , blank=True)  # Stores doctor details (e.g., names, specialties)
    enquiry = models.JSONField(null=True, blank=True)  # Stores list of all enquiry entered by the hospital
    patients = models.JSONField(null=True, blank=True)  # List of patient IDs who underwent treatment
    medicines = models.JSONField(null=True, blank=True)  # Medicines sold by the hospital
    employees = models.JSONField(null=True, blank=True)  # List of employees working in the hospital
    expected_patients = models.JSONField(null=True, blank=True)  # Details of enquiry expected to arrive for the day
    revenue = models.JSONField(null=True, blank=True)  # Revenue data (e.g., by date, month, amount.
    ward_numbers = models.JSONField(null=True, blank=True)  # List of ward numbers in the hospital
    beds = models.JSONField(null=True, blank=True)  # List of beds in the hospital
    
    def __str__(self):
        return self.hospital_id
    class Meta:
        db_table = 'hospitals'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True, unique=True)
    products = models.JSONField()  # Store product details as a dictionary
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateField(auto_now_add=True)
    creation_time = models.TimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)  # Remarks by the delivery agent
    address = models.JSONField()  # Store address as a dictionary
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=100)  # Adjust type if needed
    enquiry_id = models.CharField(max_length=100)  # Adjust type if needed
    payment_mode = models.CharField(max_length=50)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cod = models.BooleanField(default=False)
    status = models.CharField(max_length=50)
    payment_source = models.CharField(max_length=100)
    time_to_deliver = models.DurationField()
    dispatch_agent_id = models.CharField(max_length=100)
    calling_agent_id = models.CharField(max_length=100)
    team_leader_id = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=100)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)
    delivery_company = models.CharField(max_length=100, null=True, blank=True)
    accounts_approval = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_id} - Status: {self.status}"
    
    class Meta:
        db_table = 'order'


class notification(models.Model):
    notification_id = models.AutoField(primary_key=True, unique=True)
    notification_name = models.CharField(null=True)
    level = models.CharField(choices=[("General", "General"), ("Important", "Important"),('Critical','Critical')])
    department = models.CharField(null=True)
    users = models.JSONField()
    text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unreadby = models.JSONField(null=True)
    class Meta:
        db_table = 'notification'


class knowledgebank(models.Model):
    knowledge_id = models.AutoField(primary_key=True,unique=True)
    question = models.TextField()
    topic = models.CharField(null=True)
    user_id = models.CharField()
    profile = models.CharField()
    answer = models.TextField()
    hashtags = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'knowledgebank'



class kra(models.Model):
    kras = models.JSONField()
    profile = models.CharField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'kra'

class hr(models.Model):
    user_id = models.CharField(primary_key=True)
    name = models.CharField(null=True)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField()

    class Meta:
        db_table = 'hr'
    
    @property
    def is_authenticated(self):
        return self.is_enabled  # Assuming 'is_enabled' determines if the user is authenticated or not
    


class timetable(models.Model):
    id = models.CharField(primary_key=True)
    profile = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    timetable = models.JSONField(null=False,default=dict)

    class Meta:
        db_table = 'timetable'


class disposition(models.Model):
    id = models.CharField(primary_key=True,unique=True, default = "id")
    dispositions = models.JSONField(null=True,default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'disposition'


