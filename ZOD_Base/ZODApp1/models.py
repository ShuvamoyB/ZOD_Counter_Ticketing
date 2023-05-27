# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone
from datetime import datetime

# T1
class Xamp100Constants(models.Model):
    constant_id_x100 = models.AutoField(primary_key=True)
    constant_name_x100 = models.CharField(max_length=100)
    constant_value_x100 = models.CharField(max_length=100)
    active_yn_x100 = models.CharField(max_length=20)
    ourtag_x100 = models.CharField(max_length=100)
    tagvar_x100 = models.CharField(max_length=255)
    tagtext_t100 = models.TextField()
    ipadr_x100 = models.CharField(max_length=100)
    source_x100 = models.CharField(max_length=100)
    last_modified_user_id_x100 = models.IntegerField(default=0)
    last_modified_dt_x100 = models.DateTimeField(null=True, blank=True)
    created_by_user_id_x100 = models.IntegerField(null=True, blank=True)
    created_on_x100 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'xamp_100_constants'

# T2
class Xamp200LoadsheddingInfo(models.Model):
    log_id_200 = models.AutoField(primary_key=True)
    created_log_dt_ymd_200 = models.CharField(max_length=100)
    created_log_time_hhmm_200 = models.CharField(max_length=100)
    last_executed_ymd_200 = models.CharField(max_length=100)
    last_executed_hhmm_200 = models.CharField(max_length=100)
    error_log_200 = models.TextField()
    succesful_yn_200 = models.CharField(max_length=100)
    successful_dt_ymd_200 = models.CharField(max_length=100)

    class Meta:
        db_table = 'xamp_200_loadshedding_info'

# T3
class Xamp220DailySummary(models.Model):
    id_x220 = models.AutoField(primary_key=True)
    generated_dt_ymd_x220 = models.CharField(max_length=100)
    generated_time_hhmm_x220 = models.CharField(max_length=100)
    activation_dt_ymd_x220 = models.CharField(max_length=100)
    activation_code_x220 = models.CharField(max_length=100)
    zoo_id_x220 = models.IntegerField()
    counter_id_x220 = models.IntegerField()
    event_id_x220 = models.IntegerField()
    total_adult_x220 = models.IntegerField()
    total_child_x220 = models.IntegerField()
    total_perticket_x220 = models.IntegerField()
    adult_rate_x220 = models.IntegerField()
    child_rate_x220 = models.IntegerField()
    perticket_rate_x220 = models.IntegerField()
    active_yn_x220 = models.CharField(max_length=200)
    ourtag_x220 = models.CharField(max_length=100)
    tagvar_x220 = models.CharField(max_length=255)
    tagtext_x220 = models.TextField()
    ipadr_x220 = models.CharField(max_length=100)
    source_x220 = models.CharField(max_length=100)

    last_modified_user_id_x220 = models.IntegerField(default=0)
    last_modified_dt_x220 = models.DateTimeField(null=True, blank=True)
    created_by_user_id_x220 = models.IntegerField(null=True, blank=True)
    created_on_x220 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'xamp_220_daily_summary'

# Table-4
class Xamp300Log(models.Model):
    log_id_x300 = models.AutoField(primary_key=True)
    welcome_ymd_x300 = models.CharField(max_length=200, null =True, blank=True)
    welcome_activated_hhmm_x300 = models.CharField(max_length=40, null =True, blank=True)
    internet_connectivity_ok_failed_x300 = models.CharField(max_length=200, null =True, blank=True)
    no_of_tries_cloud_app_x300 = models.CharField(max_length=200, null =True, blank=True)
    connected_ticket_cloud_api_yesno_x300 = models.CharField(max_length=100, null =True, blank=True)
    otp_for_sms_x300 = models.CharField(max_length=60, null =True, blank=True)
    mobileno_received_byapi_forotp_sending_x300 = models.CharField(max_length=200, null =True, blank=True)
    otp_entered_text_x300 = models.CharField(max_length=60, null =True, blank=True)
    connected_ticket_cloud_api_sent_json_x300 = models.TextField()
    jsondata_sent_to_t520_from_cc_x300 = models.TextField()
    cloud_tkt_520id_x300 = models.IntegerField(null =True, blank=True)
    zoo_id_430_x300 = models.IntegerField(null =True, blank=True)
    zoo_name_430_x300 = models.CharField(max_length=400, null =True, blank=True)
    zoo_code_abbr_430_x300 = models.CharField(max_length=200, null =True, blank=True)
    zoo_opentime_430_x300 = models.CharField(max_length=100, null =True, blank=True)
    zoo_closetime_430_x300 = models.CharField(max_length=100, null =True, blank=True)
    unique_ticket_zoo_2char_code_430_x300 = models.CharField(max_length=40, null =True, blank=True)
    enclave_code_t370_x300 = models.CharField(max_length=100, null =True, blank=True)
    counter_unique_code_wrt_zoo_t390_x300 = models.CharField(max_length=40, null =True, blank=True)
    zoo_counters_id_t390_x300 = models.IntegerField(null =True, blank=True)
    zoo_counters_username_t160_x300 = models.CharField(max_length=255, null =True, blank=True)
    activation_code_entered_x300 = models.CharField(max_length=50, null =True, blank=True)
    activate_code_verified_yn_x300 = models.CharField(max_length=200, null =True, blank=True)
    ticket_start_hhmm_t500_x300 = models.CharField(max_length=40, null =True, blank=True)
    ticket_end_hhmm_t500_x300 = models.CharField(max_length=40, null =True, blank=True)
    ticket_counter_activated_from_hhmm_x300 = models.CharField(max_length=40, null =True, blank=True)
    todays_code_t520_x300 = models.CharField(max_length=40, null =True, blank=True)
    security_code_x300 = models.CharField(max_length=100, null =True, blank=True)
    saletype_x300 = models.CharField(max_length=100, null =True, blank=True)
    ticket_prefix_x300 = models.CharField(max_length=100, null =True, blank=True)
    total_ticket_sold_x300 = models.CharField(max_length=100, null =True, blank=True)
    total_ticket_reprint_x300 = models.CharField(max_length=200, null =True, blank=True)

    total_per_ticket_x300 = models.CharField(max_length=100, null =True, blank=True)
    total_adult_x300 = models.CharField(max_length=100, null =True, blank=True)
    total_child_x300 = models.CharField(max_length=100, null =True, blank=True)

    total_revenue_x300 = models.CharField(max_length=200, null =True, blank=True)
    total_cash_x300 = models.CharField(max_length=200, null =True, blank=True)
    total_card_x300 = models.CharField(max_length=200, null =True, blank=True)
    total_upi_x300 = models.CharField(max_length=200, null =True, blank=True)
    counter_closed_at_hhmm_x300 = models.CharField(max_length=40, null =True, blank=True)
    uploaded_json_file_created_path_x300 = models.CharField(max_length=500, null =True, blank=True)
    uploaded_json_file_created_name_x300 = models.CharField(max_length=100, null =True, blank=True)
    uploaded_file_created_path_x300 = models.CharField(max_length=500, null =True, blank=True)
    uploaded_file_created_name_x300 = models.CharField(max_length=100, null =True, blank=True)
    file_uploaded_on_ymd_x300 = models.CharField(max_length=200, null =True, blank=True)
    file_uploaded_on_hhmm_x300 = models.CharField(max_length=200, null =True, blank=True)
    active_yn_x300 = models.CharField(max_length=200, null =True, blank=True)
    ourtag_x300 = models.CharField(max_length=100, null =True, blank=True)
    tagvar_x300 = models.CharField(max_length=255, null =True, blank=True)
    tagtext_x300 = models.TextField()
    ipadr_x300 = models.CharField(max_length=100, null =True, blank=True)
    source_x300 = models.CharField(max_length=100, null =True, blank=True)

    last_modified_user_id_x300 = models.IntegerField(default=0)
    last_modified_dt_x100 = models.DateTimeField(null=True, blank=True)
    created_by_user_id_x300 = models.IntegerField(null=True, blank=True)
    created_on_x300 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'xamp_300_log'


# JSON Data from Cloud (DOWNLOAD)
# # TABLE-5A________________________________________________________
# class Xamp320EventwiseJsondataReceived(models.Model):
#     eventwise_jsondata_received_id_x320 = models.AutoField(primary_key=True)
#     eventname = models.CharField(max_length=255)
#     eventnameupper = models.CharField(max_length=255)
#     eventid = models.IntegerField(null =True, blank=True)
#     eventcode = models.CharField(max_length=100)
#     ticketprefix = models.CharField(max_length=200)
#     faretype = models.CharField(max_length=100)
#     adult = models.CharField(max_length=100)
#     child = models.CharField(max_length=100)
#     perunit = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'xamp_320_eventwise_jsondata_received'


# TABLE-5________________________________________________________
class Xamp320EventwiseJsondataReceived(models.Model):
    # Data to received from Cloud as JSON
    eventwise_jsondata_received_id_x320 = models.AutoField(primary_key=True)
    event_name_t130_t530_x320 = models.CharField(max_length=255, null =True, blank=True)
    event_id_from_t520_x320 = models.IntegerField(null =True, blank=True)
    event_code_from_t520_x320 = models.CharField(max_length=100, null =True, blank=True)
    ticket_prefix_x320 = models.CharField(max_length=200, null =True, blank=True)
    faretype_x320 = models.CharField(max_length=200)
    adult_rt_x320 = models.CharField(max_length=100, null =True, blank=True)
    child_rt_x320 = models.CharField(max_length=100, null =True, blank=True)
    perticket_rt_x320 = models.CharField(max_length=100, null =True, blank=True)
    # Data to send to Cloud as JSON
    zoo_calendar_daily_ticket_pointer_setting_id_t520_x320 = models.IntegerField(null =True, blank=True)
    log_id_x300_x320 = models.IntegerField(null =True, blank=True)
    ticketlast_serial_no_x320 = models.CharField(max_length=10, null =True, blank=True)
    total_adult_x320 = models.CharField(max_length=100, null =True, blank=True)
    total_child_x320 = models.CharField(max_length=100, null =True, blank=True)
    total_perunit_x320 = models.CharField(max_length=100, null =True, blank=True)
    total_ticket_sold_x320 = models.CharField(max_length=100, null =True, blank=True)
    total_cash_collected_x320 = models.CharField(max_length=100, null =True, blank=True)
    total_card_collected_x320 = models.CharField(max_length=100, null =True, blank=True)
    total_upi_collected_x320 = models.CharField(max_length=100, null =True, blank=True)
    total_revenue_collected_x320 = models.CharField(max_length=100, null =True, blank=True)
    active_yn_x320 = models.CharField(max_length=200, null =True, blank=True)
    ourtag_x320 = models.CharField(max_length=100, null =True, blank=True)
    tagvar_x320 = models.CharField(max_length=255, null =True, blank=True)
    tagtext_t320 = models.TextField()
    ipadr_x320 = models.CharField(max_length=100, null =True, blank=True)
    source_x320 = models.CharField(max_length=100, null =True, blank=True)
    last_modified_user_id_x320 = models.IntegerField(null =True, blank=True)
    last_modified_dt_x320 = models.DateTimeField(null=True, blank=True)
    created_by_user_id_x320 = models.IntegerField(null =True, blank=True)
    created_on_x320 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'xamp_320_eventwise_jsondata_received'



# T6
class Xamp330TicketGrpGist(models.Model):
    ticket_grp_gist_id_x330 = models.AutoField(primary_key=True)
    log_id_x300_x330 = models.IntegerField(null =True, blank=True)
    dt_ymd_x330 = models.CharField(max_length=160)
    active_yn_x330 = models.CharField(max_length=200)
    ourtag_x330 = models.CharField(max_length=100)
    tagvar_x330 = models.CharField(max_length=255)
    tagtext_x330 = models.TextField()
    ipadr_x330 = models.CharField(max_length=100)
    source_x330 = models.CharField(max_length=100)

    last_modified_user_id_x330 = models.IntegerField(default=0)
    last_modified_dt_x330 = models.DateTimeField(null=True, blank=True)
    created_by_user_id_x330 = models.IntegerField(null=True, blank=True)
    created_on_x330 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'xamp_330_ticket_grp_gist'

# T7
class Xamp340TicketSoldDetails(models.Model):
    ticket_sold_details_id_x340 = models.AutoField(primary_key=True)
    log_id_x300_x340 = models.IntegerField(null=True, blank=True)
    ticket_grp_gist_id_x330_x340 = models.IntegerField(null =True, blank=True)
    zoo_calendar_daily_ticket_pointer_setting_id_t520_x340 = models.IntegerField(null =True, blank=True)
    event_name_t130_t530_x340 = models.CharField(max_length=255, null =True, blank=True)
    event_id_from_t520_x340 = models.IntegerField(null =True, blank=True)
    event_code_from_t520_x340 = models.CharField(max_length=100, null =True, blank=True)
    ticket_prefix_x340 = models.CharField(max_length=100, null =True, blank=True)
    ticket_no_x340 = models.CharField(max_length=200, null =True, blank=True)
    ticketlast_serial_no_x340 = models.CharField(max_length=10, null =True, blank=True)

    total_adult_x340 = models.CharField(max_length=100, null =True, default=0)
    total_child_x340 = models.CharField(max_length=100, null =True, default=0)
    total_perunit_x340 = models.CharField(max_length=10, null =True, default=0)

    total_ticket_sold_x340 = models.CharField(max_length=100, null =True, default=0)
    total_reprint_x340 = models.CharField(max_length=110, null =True, default=0)

    total_cash_collected_x340 = models.CharField(max_length=100, null =True, default=0)
    total_card_collected_x340 = models.CharField(max_length=100, null =True, default=0)
    total_upi_collected_x340 = models.CharField(max_length=100, null =True, default=0)

    total_revenue_collected_x340 = models.CharField(max_length=100, null =True, default=0)
    
    adult_rt_x340 = models.CharField(max_length=100, null =True, blank=True)
    child_rt_x340 = models.CharField(max_length=100, null =True, blank=True)
    perticket_rt_x340 = models.CharField(max_length=100, null =True, blank=True)
    qrcode_file_path_x340 = models.CharField(max_length=255, null =True, blank=True)
    qrcode_file_name_x340 = models.CharField(max_length=100, null =True, blank=True)
    active_yn_x340 = models.CharField(max_length=200, null =True, blank=True)
    ourtag_x340 = models.CharField(max_length=100, null =True, blank=True)
    tagvar_x340 = models.CharField(max_length=255, null =True, blank=True)
    tagtext_t340 = models.TextField(null =True, blank=True)
    ipadr_x340 = models.CharField(max_length=100, null =True, blank=True)
    source_x340 = models.CharField(max_length=100, null =True, blank=True)

    last_modified_user_id_x340 = models.IntegerField(default=0)
    last_modified_dt_x340 = models.DateTimeField(null=True, blank=True)
    created_by_user_id_x340 = models.IntegerField(null=True, blank=True)
    created_on_x340 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'xamp_340_ticket_sold_details'


class Xamp350SetellementDetailed(models.Model):
    constant_id_x100 = models.AutoField(primary_key=True)
    constant_name_x100 = models.CharField(max_length=100)
    constant_value_x100 = models.CharField(max_length=100)
    active_yn_x100 = models.CharField(max_length=20)
    ourtag_x100 = models.CharField(max_length=100)
    tagvar_x100 = models.CharField(max_length=255)
    tagtext_t100 = models.TextField()
    ipadr_x100 = models.CharField(max_length=100)
    source_x100 = models.CharField(max_length=100)

    last_modified_user_id_x100 = models.IntegerField(default=0)
    last_modified_dt_x100 = models.DateTimeField(null=True, blank=True)
    created_by_user_id_x100 = models.IntegerField(null=True, blank=True)
    created_on_x100 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'xamp_350_setellement_detailed'
