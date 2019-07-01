from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid


class HowYouHeard(models.Model):
    MEDIUM_TYPE = (
        ('default', 'Default'),
        ('other', 'Other')
    )
    medium = models.TextField(unique=True)
    type = models.CharField(
        help_text='Type of medium heard', choices=MEDIUM_TYPE, max_length=100)

    def __unicode__(self):
        return str(self.medium)

    class Meta:
        db_table = "how_you_heard"


class PotluckSurvey(models.Model):
    ETHNIC_TYPE = (
        ('black or african american', 'Black or African American'),
        ('white', 'White'),
        ('prefer not to say', 'Prefer not to say')
    )
    AVAILABILITY_TYPE = (
        ('tuesday', 'Tuesday'),
        ('thursday', 'Thursday'),
        ('tuesday and thursday', 'Tuesday and Thursday')
    )
    HOST_TYPE = (
        ('home', 'Home'),
        ('church', 'Church')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(help_text='Survey Username', max_length=200)
    email = models.EmailField(max_length=254, help_text='example@gmail.com')
    phone = models.CharField(help_text='Mobile Number', max_length=20)
    zipcode = models.IntegerField(help_text='Valid US Zip code')
    ethnic_persuasion = models.CharField(
        help_text='Ethnic type', choices=ETHNIC_TYPE, max_length=100)
    involved = models.CharField(
        help_text='No of individuals involved', max_length=100)
    church_affiliation = models.TextField(
        blank=True, help_text='Association with church')
    availability = models.CharField(
        help_text='Ethnic type', choices=AVAILABILITY_TYPE, max_length=100)
    hosting_at = models.CharField(
        help_text='Ethnic type', choices=HOST_TYPE, max_length=100)
    dietary_restrictions_or_allergies = models.TextField(
        blank=True, help_text='Any restrictions or any allergies for food')
    heard_from = models.ManyToManyField(
        HowYouHeard, blank=True, help_text='From where did you heard?')
    comments_and_queries = models.TextField(
        blank=True, help_text='Any comments or queries')
    is_agreed = models.BooleanField(
        default=False, help_text='is agreed to terms and conditions')
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    survey_meta_data = JSONField(blank=True, null=True)

    def __unicode__(self):
        return str(self.email)

    class Meta:
        db_table = "potluck_survey"


class PotluckFood(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FOOD_TYPE = (
        ('veg', 'Veg'),
        ('non veg', 'Non Veg'),
        ('both', 'Both')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(help_text='potluck food name', unique=True)
    type = models.CharField(help_text='food type',
                            choices=FOOD_TYPE, max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    meta_data = JSONField(blank=True, null=True)

    class Meta:
        db_table = "potluck_food"


class PotluckGroup(models.Model):
    STATUS_TYPE = (
        ('locked', 'Locked'),
        ('published', 'Published'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(help_text='potluck group name', unique=True)
    attendees = models.ManyToManyField(PotluckSurvey)
    foods = models.ManyToManyField(PotluckFood)
    group_meta_data = JSONField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(help_text='status type', choices=STATUS_TYPE, default=STATUS_TYPE[0][0],
                              max_length=100)
    hosting_on = models.DateTimeField(blank=True, null=True)
    manager = models.ForeignKey(
        PotluckSurvey, on_delete=models.SET_NULL, blank=True, null=True, related_name='group_manager', help_text='Manager of the group')

    class Meta:
        db_table = "potluck_group"


class PotluckFoodGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_id = models.ForeignKey(
        PotluckGroup, on_delete=models.SET_NULL, blank=True, null=True, related_name='food_group_group_id', help_text='group of a survey user')
    guest_id = models.ForeignKey(
        PotluckSurvey, on_delete=models.SET_NULL, blank=True, null=True, related_name='food_group_guest_id', help_text='survey user')
    food_id = models.ForeignKey(
        PotluckFood, on_delete=models.SET_NULL, blank=True, null=True, related_name='food_group_food_id', help_text='food assigned to survey user of a group')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['group_id', 'food_id']]
        db_table = "potluck_food_group"


class GlobalMeta(models.Model):
    potluck_csv_meta = JSONField(blank=True)

    class Meta:
        db_table = "global_meta"
