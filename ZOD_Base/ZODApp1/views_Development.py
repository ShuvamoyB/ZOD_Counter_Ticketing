from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .serializers import Xamp320EventwiseJsondataReceivedSerializer
from datetime import datetime
import time
from daterangefilter.filters import PastDateRangeFilter, FutureDateRangeFilter
import requests
import re
import json
import ast
import os
import base64
import pyqrcode
# from dotenv import load_dotenv
# load_dotenv()


## Global declarations______________
StartDate = datetime.now().date()
StTime = datetime.now().time()
print(StTime)
StartTime = StTime
# n=random.randint(39896, 93654)

## Cloud API Headers & URL
Headerkey = 'keys'
ZOO_API_KEYS_Val = 'innova@2021'

Headers = {Headerkey : ZOO_API_KEYS_Val}
ZOO_API_URL = "https://php151.innovaindia.in/zoonewton/work/"

InternetStatus = False
TicketCloudStatus = False
ActvCode = 0
ActivationCode_Verified = False
OTPCode = 0



## Starting Index Page__________________________________________________________
def index(request):
    StartDate1 = datetime.now().date().strftime("%d-%B-%Y")
    StartTime1 = datetime.now().time().strftime("%H:%M %p")

    strStartTime = str(StartTime)    
    if strStartTime <= '11:59':
        starttimestr = "Good Morning"
    elif strStartTime >= '12:00' and strStartTime <= '16:59':
        starttimestr = "Good Afternoon"
    else:
        starttimestr = "Good Evening"
    
    context = {
        'startdt':StartDate, 
        'starttime':StartTime1, 
        'starttimestr':starttimestr
    }
        
    return render(request, 'index.html', context)



# Code Verification for Activation_____________________________________
def login(request):
    global InternetStatus, TicketCloudStatus, ActivationKey, ActvCode, ActivationCode_Verified

    # Check Internet Link
    def internet_on():
        return (lambda a: True if 0 == a.system('ping 8.8.8.8 -n 1 > clear') else False)(__import__('os'))
    InternetStatus = internet_on()
    print("InternetStatus: ",InternetStatus)

    print("\n",str(ZOO_API_URL))
    print(Headers,"\n")   

    # Check the Link with Ticket Cloud:
    if InternetStatus == True:
        API_ConnectionCheck = "api/tapi/connection_check_api"
        api_url_linking = str(ZOO_API_URL+API_ConnectionCheck)            
        response = requests.post(api_url_linking, headers=Headers)            
        print("\nConnection Status Code: ", response.status_code)
        print("\nConnection Response: ", response.text)
        if response.status_code == 200:  
            TicketCloudStatus = True      

            ## Activation Code Verification
            # Get Activation Code from login.html page
            if request.method == "POST":
                ActvCode = request.POST.get('activationcode')
                print("\nActivation Code: ", ActvCode)
                ActivationKey = 'activation_code'
                ActvCodeData = {ActivationKey:ActvCode}

                API_CodeVerification = 'api/tapi/activation_code_verification_api'
                api_url_activation = str(ZOO_API_URL+API_CodeVerification)
                response1 = requests.post(api_url_activation, data=ActvCodeData, headers=Headers)
                ActivationStatusCode = response1.status_code
                print("\nStatus Code after activation code: ", ActivationStatusCode)

                if ActivationStatusCode != 404:
                    print("\nActivation Code Valid.")
                    ActivationCode_Verified = 'yes'
                else:
                    print("\nInvalid Activation Code.")
                    ActivationCode_Verified = 'no'

                return redirect('otp')
                
                # if ActivationStatusCode != 404:
                #     print("\nActivation Code Valid.", )
                #     return redirect('otp')
                # else:
                #     print("\nInvalid Activation Code.", )
                #     messages.warning(request, "Invalid Activation Code")
        else:
            print("\nNo Internet")
            TicketCloudStatus = False

    print("\nInternet Status: ", InternetStatus)
    print("Cloud connection status: ", TicketCloudStatus)

    return render(request, 'login.html', {'internet':InternetStatus, 'ticketcloud':TicketCloudStatus})



# OTP Validation_______________________________________________
def otp(request):
    global OTPCode

    # Get OTP from otp.html page    
    if request.method == "POST":
        OTPCode = request.POST.get('otpcode')
        print("\nOTP Code: ", OTPCode)

        # print("\nActivation Key: ",ActivationKey)
        
        OTPKey = 'otp_code'
        # OTPActivationCodeData = {ActivationKey:ActvCode, OTPKey:OTPCode}
        # print("\nOTP Activation Code: ",OTPActivationCodeData)
        
        API_OTPVerification = 'api/tapi/otp_verification_api'
        api_url_otp = str(ZOO_API_URL+API_OTPVerification)
        
        # response3 = requests.post(api_url_otp, data=OTPActivationCodeData, headers=Headers)
        # ValidationStatusCode = response3.status_code
        # print("Validation Status: ", ValidationStatusCode)
        
        # if ValidationStatusCode != 404:
        #     # Download JSON data from cloud________________
        #     JsonDataFrmCloud = response3.text           
        #     # Dump JSON data to a JSON file
        #     with open("CloudResponse.json", "w") as outfile:
        #         json.dump(JsonDataFrmCloud, outfile)
        #         print("\n JSON data dumped to the JSON file: CloudResponse.json")
        #         messages.success(request, "OTP Validate")
        #         return redirect('activation')
        return redirect('activation')
        # else:
        #     messages.warning(request, "Invalid OTP")
        #     return render(request, 'otp.html')

    return render(request, 'otp.html')



# Activation Page___________________________________________________________________ACTIVATION____________

# Fatching data from Json file
def activation(request):

    # Load JSON and convert to Dictionary
    with open('CloudResponse.json') as json_file:
        Dict1 = json.load(json_file)
        # print("\nDict Data: \n",Dict1)
        
        Dict2 =  Dict1['data']['jsondata_sent_t520']
        # print("\n",Dict2)

        Dict3 = json.loads(Dict2)
        print("\nDict3: ",Dict3)


    # InternetStatus1 = InternetStatus
    # TicketCloudStatus1 = TicketCloudStatus
    
    # try:
    #     ActvCode1 = ActvCode
    #     if InternetStatus1 == True:
    #         InternetStatus1 = 'ok'
    #     else:
    #         InternetStatus1 = 'failed'
        
    #     if TicketCloudStatus1 == True:
    #         TicketCloudStatus1 = 'yes'
    #     else:
    #         TicketCloudStatus1 = 'no'
    # except:
    #     InternetStatus1 = 'ok'
    #     TicketCloudStatus1 = 'yes'
    #     ActvCode = 'AZD123456'


    # Upload JSON Data to Database Tables_______________
    # Enter Data to Table-4 (300):
    modelTable4 = Xamp300Log()
    modelTable4.internet_connectivity_ok_failed_x300 = InternetStatus
    modelTable4.connected_ticket_cloud_api_yesno_x300 = TicketCloudStatus
    modelTable4.activation_code_entered_x300 = ActvCode
    modelTable4.activate_code_verified_yn_x300 = ActivationCode_Verified
    modelTable4.otp_entered_text_x300 = OTPCode

    modelTable4.cloud_tkt_520id_x300 = Dict3['tkt520id']
    modelTable4.ticket_start_hhmm_t500_x300 = Dict3['tktstarthhmm']
    modelTable4.ticket_counter_activated_from_hhmm_x300 = Dict3['tktactivatedhhmm']
    modelTable4.todays_code_t520_x300 = Dict3['todayscode']
    modelTable4.security_code_x300 = Dict3['securitycode']
    modelTable4.zoo_id_430_x300 = Dict3['zoo_id']
    modelTable4.zoo_name_430_x300 = Dict3['zoonm']
    modelTable4.zoo_code_abbr_430_x300 = Dict3['zoocodeabbr']
    modelTable4.zoo_opentime_430_x300 = Dict3['zoopentime']
    modelTable4.zoo_closetime_430_x300 = Dict3['zooclosetime']
    modelTable4.zoo_counters_id_t390_x300 = Dict3['counterid']
    modelTable4.counter_unique_code_wrt_zoo_t390_x300 = Dict3['countercode']
    modelTable4.enclave_code_t370_x300 = Dict3['enclavecode']
    modelTable4.zoo_counters_username_t160_x300 = Dict3['counterusername']
    modelTable4.saletype_x300 = Dict3['saletype']
    modelTable4.ticket_prefix_x300 = Dict3['ticketprefix5']
    # modelTable4.activation_code_entered_x300 = Dict3['activationcode']
    modelTable4.otp_for_sms_x300 = Dict3['otp']
    modelTable4.ticket_end_hhmm_t500_x300 = Dict3['tktclosinghhmm']    
    modelTable4.save()
   
    TodaysCode = Dict3['todayscode']

    tm1 = Dict3['tktclosinghhmm']
    timeVal1 = tm1[0:2]
    timeVal2 = tm1[2:4]
    CloseTime = timeVal1+":"+timeVal2
    tm2 = datetime.strptime(CloseTime, "%H:%M")
    CounterClosingTime = datetime.time(tm2)
    print("\nCounter Closing Time: ",CounterClosingTime)


    # Enter a single value to the Dictionary RateListDict

    RateListDict = Dict3['currentrate']        
    print("\nRateListDict: ", RateListDict, "\n")
    print("Total No of Events: ",len(RateListDict),"\n")

    for key in RateListDict:
        key.pop('eventnameupper')
        key['event_name_t130_t530_x320'] = key.pop('eventname')
        key['event_id_from_t520_x320'] = key.pop('eventid')
        key['event_code_from_t520_x320'] = key.pop('eventcode')
        key['ticket_prefix_x320'] = key.pop('ticketprefix')
        key['faretype_x320'] = key.pop('faretype')
        key['adult_rt_x320'] = key.pop('adult')
        key['child_rt_x320'] = key.pop('child')
        key['perticket_rt_x320'] = key.pop('perunit')
    

    print("\nNew RateListDict: ",RateListDict)


    # SERIALIZER - Load Data from JSON to Table-5A(320):
    for i in range(len(RateListDict)):
        myDict = RateListDict[i]
        print("\nmyDict by serializer: ",myDict,"\n")
        serializer = Xamp320EventwiseJsondataReceivedSerializer(data=myDict)
        if serializer.is_valid():
            serializer.save()


    Log_ID_x300 = Xamp300Log.objects.only('log_id_x300').latest('log_id_x300').log_id_x300
    print("\nLog_ID_x300: ", Log_ID_x300)

    modelTable6 = Xamp330TicketGrpGist()
    modelTable6.log_id_x300_x330 = Log_ID_x300
    modelTable6.dt_ymd_x330 = datetime.now().date()
    modelTable6.active_yn_x330 = 'yes'
    modelTable6.save()


    LastId_320 = (Xamp320EventwiseJsondataReceived.objects.last()).eventwise_jsondata_received_id_x320
    print("\nLast ID of Table x320: ", LastId_320)
    LastEventID320 = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=LastId_320).event_id_from_t520_x320
    print("\nLast Event ID: ", LastEventID320)

    # for i in range(LastId_320):
    #     modelTable5 = Xamp320EventwiseJsondataReceived()
    #     modelTable5.log_id_x300_x320 = Log_ID_x300
    #     modelTable5.save()


    j=0
    eventList = []
    adultRtList = []
    childRtList = []
    perunitRtList = []
    for j in range(1, (LastEventID320+1)):
        EventID = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).event_id_from_t520_x320
        print("Event ID: ",EventID)
        EventCode = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).event_code_from_t520_x320
        print("Event Code: ",EventCode)
        TicketPrefix = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).ticket_prefix_x320
        print("Event Code: ",TicketPrefix)
        EventName = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).event_name_t130_t530_x320
        print("Event Name: ",EventName)
        AdultRate = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).adult_rt_x320
        print("Adult Rate: ",AdultRate)
        ChildRate = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).child_rt_x320
        print("Child Rate: ",ChildRate)
        VideoPerUnitRate = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).perticket_rt_x320
        print("Video Per Unit Rate: ",VideoPerUnitRate)
        ZooCalendarSettingIDx340 = Xamp300Log.objects.only('cloud_tkt_520id_x300').latest('cloud_tkt_520id_x300').cloud_tkt_520id_x300
        print("Zoo Calendar Setting ID x340: ",ZooCalendarSettingIDx340)
        eventList.append(EventName)
        adultRtList.append(AdultRate)
        childRtList.append(ChildRate)
        perunitRtList.append(VideoPerUnitRate)

    print("\nEvent List: ",eventList)
    print("Adult Rate List: ",adultRtList)
    print("Child Rate List: ",childRtList)
    print("Video Per Unit Rate List (Activation Page): ",perunitRtList,"\n")
        
        
    # Display Data at Activation Page______________________
    # Entry:
    EventName1 = eventList[0]
    AdultRate1 = adultRtList[0]
    ChildRate1 = childRtList[0]
    PerUnitRate1 = perunitRtList[0]
    print("\nEvent Name-1: ",EventName1)
    print("Adult Rate-1: ",AdultRate1)
    print("Child Rate-1: ",ChildRate1)
    print("PerUnit Rate-1: ",PerUnitRate1,"\n")
    # Video Photography:
    EventName2 = eventList[1]
    AdultRate2 = adultRtList[1]
    ChildRate2 = childRtList[1]
    PerUnitRate2 = perunitRtList[1]
    print("\nEvent Name-2: ",EventName2)
    print("Adult Rate-2: ",AdultRate2)
    print("Child Rate-2: ",ChildRate2)
    print("Per Unit Rate-2: ",PerUnitRate2)
    # Aquarium:
    EventName3 = eventList[2]
    AdultRate3 = adultRtList[2]
    ChildRate3 = childRtList[2]
    PerUnitRate3 = perunitRtList[2]
    print("\nEvent Name-3: ",EventName3)
    print("Adult Rate-3: ",AdultRate3)
    print("Child Rate-3: ",ChildRate3)
    print("Per Unit Rate-3: ",PerUnitRate3) # NA


    StartDate1 = datetime.now().date().strftime("%d-%B-%Y")
    StartTime1 = datetime.now().time().strftime("%H:%M %p")

    print("\nStart Date: ",StartDate1)
    print("Start Time: ",StartTime1,"\n")

    # Save data to Environment Variables:
    DictEnvVar = {
        "LAST_ID_X300":Log_ID_x300, 
        "LAST_ID_X320":LastId_320, 
        "LAST_EVENT_ID_X320":LastEventID320,
        "Event_Code":EventCode,
        "AdultEntryRate":AdultRate1,
        "ChildEntryRate":ChildRate1,
        "PerUnitVideoRate":PerUnitRate2,
        "AdultAqRate":AdultRate3,
        "ChildAqRate":ChildRate3
    }

    with open(".env", "w") as fw:
        fw.write(str(DictEnvVar)+'\n')
    fw.close()

    
    context= {
        'startdt': StartDate1,
        'starttime': StartTime1,
        'closedt': StartDate1,
        'closetime' : CounterClosingTime,
        'todayscode': TodaysCode,
        'eventname1': EventName1,
        'adultrate1': AdultRate1,
        'childrate1': ChildRate1,
        'eventname2': EventName2,
        'perunitrate2': PerUnitRate2,
        'eventname3': EventName3,
        'adultrate3': AdultRate3,
        'childrate3': ChildRate3,
        }

    return render(request, 'activation.html', context)





#___Ticket Generation by PC________________________________________________________TICKET GENERATION_________

def generate_ticket_pc(request):
    
    TktCounterCode = (Xamp300Log.objects.last()).zoo_code_abbr_430_x300
    CounterUserName = (Xamp300Log.objects.last()).zoo_counters_username_t160_x300

    EntryTotalNoOfAdults=0
    EntryTotalNoOfChild=0
    AquariumTotalNoOfAdults=0
    AquariumTotalNoOfChild=0
    TotalVideoPerUnit=0

    AdultEntryRate=0
    ChildEntryRate=0
    PerUnitVideoRate=0
    AdultAquariumRate=0
    ChildAquariumRate=0

    TotalEntryCost=0
    TotalPerUnitVideoCost=0
    TotalAquariumCost=0

    # Get Environment Variables____________________    
    with open(".env", "r") as fr:
        readString = fr.read()
    fr.close()

    Env_Dict = ast.literal_eval(readString)  # Converting String to Dictionary
    print('\nEnv_Dict: ',Env_Dict)
    LastEventID320 = Env_Dict['LAST_EVENT_ID_X320']
    EventCode = Env_Dict['Event_Code']
    AdultEntryRate = Env_Dict['AdultEntryRate']
    ChildEntryRate = Env_Dict['ChildEntryRate']
    PerUnitVideoRate = Env_Dict['PerUnitVideoRate']
    AdultAquariumRate = Env_Dict['AdultAqRate']
    ChildAquariumRate = Env_Dict['ChildAqRate']


    # TID Ticket No Generation:
    ZooID=str(Xamp300Log.objects.only('zoo_id_430_x300').latest('zoo_id_430_x300').zoo_id_430_x300)
    print("\nZooCode: ",ZooID)  
    CounterCode=str(Xamp300Log.objects.only('counter_unique_code_wrt_zoo_t390_x300').latest('counter_unique_code_wrt_zoo_t390_x300').counter_unique_code_wrt_zoo_t390_x300)
    print("CounterCode: ",CounterCode)
    EnclaveCode=str(Xamp300Log.objects.only('enclave_code_t370_x300').latest('enclave_code_t370_x300').enclave_code_t370_x300)
    print("EnclaveCode: ",EnclaveCode)
    TicketDate1=datetime.now().date().strftime('%d%m%Y')
    TicketDate=str(TicketDate1)
    print("TicketDate: ",TicketDate)
    TypeForCounter='C'
    TicketSrNo=1
    print("TicketSrNo: ",TicketSrNo)
    print("EventCode: ",EventCode)
    
    TodaysCode = (Xamp300Log.objects.last()).todays_code_t520_x300
    TIDNo = int(TodaysCode[-1])
    TID_No = str(TIDNo+1)
    # TID_No = int(re.search(r'\d+', TodaysCode).group())
    # TID_No = TID_No+1
    print("\nTID Number: ", TID_No)

    # TIDCode = ZooCode+CounterCode+EnclaveCode+TicketDate+TypeForCounter+TicketSrNo+EventCode+'/'+TID_No
    TID_Ticket_No = ZooID+CounterCode+EnclaveCode+TicketDate+TypeForCounter+EventCode+'/'+TID_No


    TotalAdultList = []
    TotalChildList = []
    TotalPerUnitList = []
    TotalCostList = []
    TotalCostListDB=[]
    TotalTicketList = []

    if request.method == "POST":
        ## Number of Adult & Child as per Events____________________________
        # Adult List___________________________
        EntryTotalNoOfAdults = int(request.POST.get('total_adult_1'))
        TotalAdultList.insert(0, EntryTotalNoOfAdults)
        TotalAdultList.insert(1, 0)
        AquariumTotalNoOfAdults = int(request.POST.get('total_adult_3'))
        TotalAdultList.insert(2, AquariumTotalNoOfAdults)

        # Child List___________________________
        EntryTotalNoOfChild = int(request.POST.get('total_child_1'))
        TotalChildList.insert(0, EntryTotalNoOfChild)
        TotalChildList.insert(1, 0)
        AquariumTotalNoOfChild = int(request.POST.get('total_child_3'))
        TotalChildList.insert(2, AquariumTotalNoOfChild)

        # Video PerUnit List_________________________
        TotalVideoPerUnit = int(request.POST.get('total_perunit_2'))
        TotalPerUnitList.insert(0, 0)
        TotalPerUnitList.insert(1, TotalVideoPerUnit)
        TotalPerUnitList.insert(2, 0)
    
        print("\n________Total Adult List: ", TotalAdultList)
        print("__________TotalPerUnitList: ", TotalPerUnitList)
        print("__________Total Child List: ", TotalChildList)


        # Save Ticket Data to Xamp340 (Table-7):
        # Event wise Cost Calculations________________________
        # Total Adult Entry Cost:
        AdultTotalEntryCost = EntryTotalNoOfAdults * int(AdultEntryRate)
        # Total Child Entry Cost:
        ChildTotalEntryCost = EntryTotalNoOfChild * int(ChildEntryRate)
        # Entry - Total Cost:
        TotalEntryCost = AdultTotalEntryCost + ChildTotalEntryCost
        print("Total Entry Cost (Adults+Child): ", TotalEntryCost)
        TotalCostList.insert(0, TotalEntryCost)
        TotalEntry = EntryTotalNoOfAdults + EntryTotalNoOfChild
        print("\nTotal No. of Entry Tickets: ", TotalEntry)
        TotalTicketList.append(TotalEntry)

        # Total Per Unit Video Cost:
        TotalPerUnitVideoCost = TotalVideoPerUnit * int(PerUnitVideoRate)
        print("\nTotal Video Cost: ", TotalPerUnitVideoCost)
        TotalCostList.insert(1, TotalPerUnitVideoCost)
        TotalVideo = TotalVideoPerUnit
        print("\nTotal No. of Video Tickets: ", TotalVideo)
        TotalTicketList.append(TotalVideo)

        # Total Adults to Aquarium:
        AquariumTotalAdultCost = AquariumTotalNoOfAdults * int(AdultAquariumRate)
        # Total Child to Aquarium:
        AquariumTotalChildCost = AquariumTotalNoOfChild * int(ChildAquariumRate)
        # Aquarium - Total Cost:
        TotalAquariumCost = AquariumTotalAdultCost + AquariumTotalChildCost
        print("Total Aquarium Cost (Adults+Child): ", TotalAquariumCost,"\n")
        TotalCostList.insert(2, TotalAquariumCost)
        TotalAquarium = AquariumTotalNoOfAdults + AquariumTotalNoOfChild
        print("\nTotal No. of Aquarium Tickets: ", TotalAquarium)
        TotalTicketList.append(TotalAquarium)

        print("\nTotal Cost List: ", TotalCostList)
        print("\nTotal Ticket List: ", TotalTicketList)

        # Calculated value wrt event
        Total_Revenue_Collected = TotalEntryCost + TotalPerUnitVideoCost + TotalAquariumCost
        print("\nTotal_Revenue_Collected_x340: ",Total_Revenue_Collected)

        PaymentMode = request.POST.get('payment_mode_type')
        print("\nPayment Mode : ", PaymentMode)

        TotalNoOfTickets = request.POST.get('total_tickets')
        print("\nTotal No of Tickets from Frontend : ", TotalNoOfTickets)
        
        j=0
        for j in range(1, (LastEventID320+1)):
            modelTable7 = Xamp340TicketSoldDetails()
            EventID = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).event_id_from_t520_x320
            modelTable7.event_id_from_t520_x340 = EventID
            EventCode = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).event_code_from_t520_x320
            modelTable7.event_code_from_t520_x340 = EventCode
            TicketPrefix = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).ticket_prefix_x320
            modelTable7.ticket_prefix_x340 = TicketPrefix
            EventName = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).event_name_t130_t530_x320
            modelTable7.event_name_t130_t530_x340 = EventName
            AdultRate = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).adult_rt_x320
            modelTable7.adult_rt_x340 = AdultRate
            ChildRate = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).child_rt_x320
            modelTable7.child_rt_x340 = ChildRate
            VideoPerUnitRate = Xamp320EventwiseJsondataReceived.objects.only('event_id_from_t520_x320').get(pk=j).perticket_rt_x320
            modelTable7.perticket_rt_x340 = VideoPerUnitRate
            # modelTable7.ticketlast_serial_no_x340 = no of the ticket
            modelTable7.total_adult_x340 = TotalAdultList[j-1]
            modelTable7.total_perunit_x340 = TotalPerUnitList[j-1]
            modelTable7.total_child_x340 = TotalChildList[j-1]            
            modelTable7.total_ticket_sold_x340 =  TotalTicketList[j-1]
            if PaymentMode == 'cash':
                modelTable7.total_cash_collected_x340 = TotalCostList[j-1]
            if PaymentMode == 'card':
                modelTable7.total_card_collected_x340 = TotalCostList[j-1]
            if PaymentMode == 'upi':
                modelTable7.total_upi_collected_x340 = TotalCostList[j-1]
            modelTable7.total_revenue_collected_x340 = TotalCostList[j-1]
            ZooCalendarSettingIDx340 = (Xamp300Log.objects.last()).cloud_tkt_520id_x300
            modelTable7.zoo_calendar_daily_ticket_pointer_setting_id_t520_x340 = ZooCalendarSettingIDx340
            modelTable7.log_id_x300_x340 = (Xamp300Log.objects.last()).log_id_x300
            modelTable7.ticket_grp_gist_id_x330_x340 = (Xamp330TicketGrpGist.objects.last()).ticket_grp_gist_id_x330
            # modelTable7.created_on_x340 = datetime.now().strftime("%d-%m-%y %H:%M:%S")
            modelTable7.created_on_x340 = datetime.now()
            modelTable7.ticket_no_x340 = TID_Ticket_No
            # modelTable7.last_modified_user_id_x340 = 
            # modelTable7.last_modified_dt_x340 =
            # modelTable7.created_by_user_id_x340 = 
            # modelTable7.tagvar_x340 = 
            # modelTable7.tagtext_t340 =
            modelTable7.save()

        return redirect('print_ticket')
    

    try:
        id_340 = (Xamp340TicketSoldDetails.objects.last()).ticket_sold_details_id_x340    
        LastEventIDx340 = (Xamp340TicketSoldDetails.objects.last()).event_id_from_t520_x340
        LastEventIDx340e = LastEventIDx340+1
        i=0
        index=0
        for i in range(1,LastEventIDx340e):
            index = id_340 - (LastEventIDx340-i)
            TotalCost = Xamp340TicketSoldDetails.objects.only('ticket_sold_details_id_x340').get(pk=index).total_revenue_collected_x340
            print("\ni = ", index)
            TotalCostListDB.append(TotalCost)
    except:
        for j in range(LastEventID320):
            TotalCost = 0
            TotalCostListDB.append(TotalCost)

    print("\nTotalCostListDB: ", TotalCostListDB)
    print("\nTotalCostList_Entry: ", TotalCostListDB[0])
    print("\nTotalCostList_VideoPU: ", TotalCostListDB[1])
    print("\nTotalCostList_Aq: ", TotalCostListDB[2])

    context = {
        'countercode': TktCounterCode,
        'counterusername': CounterUserName,
        'adultrate1': AdultEntryRate,
        'childrate1': ChildEntryRate,
        'perunitrate2': PerUnitVideoRate,
        'adultrate3': AdultAquariumRate,
        'childrate3': ChildAquariumRate,
        'totalentrycost': TotalCostListDB[0],
        'totalvideorate': TotalCostListDB[1],
        'totalaquariumcost': TotalCostListDB[2],
        }

    return render(request, 'generate_ticket_pc.html', context)





#_____Ticket Generation by Touch Screen_____________________________________________________________________
def generate_ticket_ts(request):

    return render(request, 'generate_ticket_touchscreen.html')




#_____Print Ticket_________________________________________________________________PRINT TICKET____________
def print_ticket(request):

    # Required Ticket Data from DB Table-7(340)

    print("\nPrint Ticket___________________________________")

    Valid_for_Dt = datetime.now().date()
    PresentTime = datetime.now().time()
    ZooName = Xamp300Log.objects.only('zoo_name_430_x300').latest('zoo_name_430_x300').zoo_name_430_x300
    ZooOpenTime = Xamp300Log.objects.only('zoo_opentime_430_x300').latest('zoo_opentime_430_x300').zoo_opentime_430_x300
    ZooCloseTime = Xamp300Log.objects.only('zoo_closetime_430_x300').latest('zoo_closetime_430_x300').zoo_closetime_430_x300

    OpenTimeVal1 = ZooOpenTime[0:2]
    OpenTimeVal2 = ZooOpenTime[2:4]
    CounterOpenTime = OpenTimeVal1+":"+OpenTimeVal2
    OpenTimeVal3 = datetime.strptime(CounterOpenTime, "%H:%M")
    ZooCounterOpenTime = datetime.time(OpenTimeVal3)
    print("\nCounter Open Time: ",ZooCounterOpenTime)

    CloseTimeVal1 = ZooCloseTime[0:2]
    CloseTimeVal2 = ZooCloseTime[2:4]
    CounterCloseTime = CloseTimeVal1+":"+CloseTimeVal2
    CloseTimeVal3 = datetime.strptime(CounterCloseTime, "%H:%M")
    ZooCounterCloseTime = datetime.time(CloseTimeVal3)
    print("\nCounter Open Time: ",ZooCounterCloseTime)

    TodaysCode = (Xamp300Log.objects.last()).todays_code_t520_x300
    CounterUniqCode = (Xamp300Log.objects.last()).counter_unique_code_wrt_zoo_t390_x300

    # TIDCode = ZooCode+CounterCode+EnclaveCode+TicketDate+TypeForCounter+TicketSrNo+EventCode+'/'+TID_No
    TIDCode = (Xamp340TicketSoldDetails.objects.last()).ticket_no_x340

    EnclaveCode=str(Xamp300Log.objects.only('enclave_code_t370_x300').latest('enclave_code_t370_x300').enclave_code_t370_x300)

    id_340 = (Xamp340TicketSoldDetails.objects.last()).ticket_sold_details_id_x340    
    LastEventIDx340 = (Xamp340TicketSoldDetails.objects.last()).event_id_from_t520_x340
    LastEventIDx340e = LastEventIDx340+1
    
    i=0
    index=0
    EventListToPrint = []
    TotalAdultListToPrint = []
    TotalPerUnitVideoList = []
    TotalChildListToPrint = []
    TotalCostListToPrint = []
    for i in range(1,LastEventIDx340e):
        index = id_340 - (LastEventIDx340-i)
        Events = Xamp340TicketSoldDetails.objects.only('ticket_sold_details_id_x340').get(pk=index).event_name_t130_t530_x340
        EventListToPrint.append(Events)

        TotalAdult = Xamp340TicketSoldDetails.objects.only('ticket_sold_details_id_x340').get(pk=index).total_adult_x340
        TotalAdultListToPrint.append(TotalAdult)

        TotalChild = Xamp340TicketSoldDetails.objects.only('ticket_sold_details_id_x340').get(pk=index).total_child_x340
        TotalChildListToPrint.append(TotalChild)

        TotalPerUnit = Xamp340TicketSoldDetails.objects.only('ticket_sold_details_id_x340').get(pk=index).total_perunit_x340
        TotalPerUnitVideoList.append(TotalPerUnit)

        TotalCost = Xamp340TicketSoldDetails.objects.only('ticket_sold_details_id_x340').get(pk=index).total_revenue_collected_x340
        TotalCostListToPrint.append(TotalCost)

    print("\nEventListToPrint: ", EventListToPrint)
    print("TotalAdultListToPrint: ", TotalAdultListToPrint)
    print("TotalChildListToPrint: ", TotalChildListToPrint)
    print("TotalPerUnitVideoList: ", TotalPerUnitVideoList)
    print("TotalCostListToPrint: ", TotalCostListToPrint)

    TotalAdultENTRYtoPrint = TotalAdultListToPrint[0]
    TotalChildENTRYtoPrint = TotalChildListToPrint[0]
    TotalPerUnitToPrint = TotalPerUnitVideoList[1]
    TotalAdultAQUARIUMtoPrint = TotalAdultListToPrint[2]
    TotalChildAQUARIUMtoPrint = TotalChildListToPrint[2]

    

    NoOfSelectedEvents = 2

    for i in range(NoOfSelectedEvents):
        # Entry:
        if (TotalAdultENTRYtoPrint>'0' and TotalChildENTRYtoPrint>'0' and TotalPerUnitToPrint=='0' and  TotalAdultAQUARIUMtoPrint=='0' and TotalChildAQUARIUMtoPrint=='0'):
            EntryDataPrint = {
                'eventname1': EventListToPrint[0],
                'entrytotaladultx340': TotalAdultListToPrint[0],
                'entrytotalchildx340': TotalChildListToPrint[0],
                'totalentrycost': TotalCostListToPrint[0],

                'zooname' : ZooName,
                'zooopentime': ZooCounterOpenTime,
                'zooclosetime': ZooCounterCloseTime,
                'valid_for_dt': Valid_for_Dt,
                'presenttime':PresentTime,
                'countercode': CounterUniqCode,
                'enclavecode': EnclaveCode,
                'todayscode': TodaysCode,
                'tid': TIDCode
            }
            return render(request, 'print_ticket.html', context = EntryDataPrint)
    
    
        # Video Per Unit
        elif (TotalPerUnitToPrint>'0' and TotalAdultENTRYtoPrint=='0' and TotalChildENTRYtoPrint=='0' and  TotalAdultAQUARIUMtoPrint=='0' and TotalChildAQUARIUMtoPrint=='0'):
            PerUnitDataPrint = {
                'eventname2': EventListToPrint[1],
                'videototalperunitx340': TotalPerUnitVideoList[1],
                'totalvideocost': TotalCostListToPrint[1],

                'zooname' : ZooName,
                'zooopentime': ZooCounterOpenTime,
                'zooclosetime': ZooCounterCloseTime,
                'valid_for_dt': Valid_for_Dt,
                'presenttime':PresentTime,
                'countercode': CounterUniqCode,
                'enclavecode': EnclaveCode,
                'todayscode': TodaysCode,
                'tid': TIDCode
            }
            return render(request, 'print_ticket.html', context = PerUnitDataPrint)

        # Aquarium:
        elif (TotalAdultAQUARIUMtoPrint>'0' and TotalChildAQUARIUMtoPrint>'0' and TotalAdultENTRYtoPrint=='0' and TotalChildENTRYtoPrint=='0' and TotalPerUnitToPrint=='0'):
            AquariumDataPrint = {
                'eventname3': EventListToPrint[2],
                'aquariumtotaladultx340': TotalAdultListToPrint[2],
                'aquariumtotalchildx340': TotalChildListToPrint[2],
                'totalaquriumcost': TotalCostListToPrint[2],

                'zooname' : ZooName,
                'zooopentime': ZooCounterOpenTime,
                'zooclosetime': ZooCounterCloseTime,
                'valid_for_dt': Valid_for_Dt,
                'presenttime':PresentTime,
                'countercode': CounterUniqCode,
                'enclavecode': EnclaveCode,
                'todayscode': TodaysCode,
                'tid': TIDCode
            }
            return render(request, 'print_ticket.html', context = AquariumDataPrint)
        

        # Entry & Video Per Unit
        elif (TotalAdultENTRYtoPrint>'0' and TotalChildENTRYtoPrint>'0' and TotalPerUnitToPrint>'0' and TotalAdultAQUARIUMtoPrint=='0' and TotalChildAQUARIUMtoPrint=='0'):
            EntryVideoDataPrint = {
                'eventname1': EventListToPrint[0],
                'entrytotaladultx340': TotalAdultListToPrint[0],
                'entrytotalchildx340': TotalChildListToPrint[0],

                'eventname2': EventListToPrint[1],
                'videototalperunitx340': TotalPerUnitVideoList[1],

                'zooname' : ZooName,
                'zooopentime': ZooCounterOpenTime,
                'zooclosetime': ZooCounterCloseTime,
                'valid_for_dt': Valid_for_Dt,
                'presenttime':PresentTime,
                'countercode': CounterUniqCode,
                'enclavecode': EnclaveCode,
                'todayscode': TodaysCode,
                'tid': TIDCode
            }
            return render(request, 'print_ticket.html', context = EntryVideoDataPrint)


        # Aquarium & Video Per Unit
        elif (TotalAdultAQUARIUMtoPrint>'0' and TotalChildAQUARIUMtoPrint>'0' and TotalPerUnitToPrint>'0' and TotalAdultENTRYtoPrint=='0' and TotalChildENTRYtoPrint=='0'):
            AquariumVideoDataPrint = {
                'eventname2': EventListToPrint[1],
                'videototalperunitx340': TotalPerUnitVideoList[1],

                'eventname3': EventListToPrint[2],
                'aquariumtotaladultx340': TotalAdultListToPrint[2],
                'aquariumtotalchildx340': TotalChildListToPrint[2],

                'totalvideocost': TotalCostListToPrint[1],
                'totalaquriumcost': TotalCostListToPrint[2],

                'zooname' : ZooName,
                'zooopentime': ZooCounterOpenTime,
                'zooclosetime': ZooCounterCloseTime,
                'valid_for_dt': Valid_for_Dt,
                'presenttime':PresentTime,
                'countercode': CounterUniqCode,
                'enclavecode': EnclaveCode,
                'todayscode': TodaysCode,
                'tid': TIDCode
            }
            return render(request, 'print_ticket.html', context = AquariumVideoDataPrint)


        # Entry & VideoPerUnit & Aquarium
        # elif (TotalAdultENTRYtoPrint>'0' and TotalChildENTRYtoPrint>'0' and TotalPerUnitToPrint>'0' and TotalAdultAQUARIUMtoPrint>'0' and TotalChildAQUARIUMtoPrint>'0'):
        else:
            EntryVideoAquariumDataPrint = {
                'eventname1': EventListToPrint[0],
                'entrytotaladultx340': TotalAdultListToPrint[0],
                'entrytotalchildx340': TotalChildListToPrint[0],

                'eventname2': EventListToPrint[1],
                'videototalperunitx340': TotalPerUnitVideoList[1],

                'eventname3': EventListToPrint[2],
                'aquariumtotaladultx340': TotalAdultListToPrint[2],
                'aquariumtotalchildx340': TotalChildListToPrint[2],

                'totalentrycost': TotalCostListToPrint[0],
                'totalvideocost': TotalCostListToPrint[1],
                'totalaquriumcost': TotalCostListToPrint[2],

                'zooname' : ZooName,
                'zooopentime': ZooCounterOpenTime,
                'zooclosetime': ZooCounterCloseTime,
                'valid_for_dt': Valid_for_Dt,
                'presenttime':PresentTime,
                'countercode': CounterUniqCode,
                'enclavecode': EnclaveCode,
                'todayscode': TodaysCode,
                'tid': TIDCode
            }
            return render(request, 'print_ticket.html', context = EntryVideoAquariumDataPrint)




# Salse Report_________________________________________________________________SALSE REPORT__________
def statement(request):
    DateRange=0

    ReportGenDt = datetime.now().date().strftime("%d-%B-%Y")
    ReportGenTime = datetime.now().time().strftime("%H:%M %p")
    print("Report Dt & Time: ",ReportGenDt, " | ",  ReportGenTime)

    LastEnclaveCode_x300 = (Xamp300Log.objects.last()).enclave_code_t370_x300
    LastCounterCode_x300 = (Xamp300Log.objects.last()).counter_unique_code_wrt_zoo_t390_x300
    CounterNo = LastEnclaveCode_x300+LastCounterCode_x300

    UserName = (Xamp300Log.objects.last()).zoo_counters_username_t160_x300
    ZooName = (Xamp300Log.objects.last()).zoo_name_430_x300

    # ZooOpenTime = Xamp300Log.objects.only('zoo_opentime_430_x300').latest('zoo_opentime_430_x300').zoo_opentime_430_x300
    # ZooCloseTime = Xamp300Log.objects.only('zoo_closetime_430_x300').latest('zoo_closetime_430_x300').zoo_closetime_430_x300

    # ZooOpenTime = ZooOpenTime.replace('00',':00:00')
    # ZooCloseTime = ZooCloseTime.replace('00',':00:00')

    OpenTime = '00:00:00'
    CloseTime = '23:59:59'

    if request.method == "POST":
        DateRange = request.POST.get('date_range')
        print("\nDate Range: ", DateRange)

        DateRangeList = DateRange.split("-")
        FrmYY = (DateRangeList[2]).replace(' ', '')
        FrmMM = DateRangeList[1]
        FrmDD = DateRangeList[0]
        SelectedDateFrm = FrmYY+'-'+FrmMM+'-'+FrmDD

        DDTo = (DateRangeList[3]).replace(' ', '')
        MMTo = DateRangeList[4]
        YYTo = DateRangeList[5]

        SelectedDateTo = YYTo+'-'+MMTo+'-'+DDTo

        print(DateRangeList)
        print(SelectedDateFrm)
        print(SelectedDateTo)
              
        DateFrm = SelectedDateFrm+' '+OpenTime
        DateTo = SelectedDateTo+' '+CloseTime

        print("\nDate From: ",DateFrm)
        print("Date To: ",DateTo,'\n')

        SelectedData_x340 = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values()
        # RangeDate_x340 = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('created_on_x340')

        TotalNoTickets = (Xamp340TicketSoldDetails.objects.last()).ticket_sold_details_id_x340

        TicketNumber = (Xamp340TicketSoldDetails.objects.last()).ticket_no_x340


        # Total Adult______
        TotalAdultQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_adult_x340')
        # print("\nTotalRevenue: ", TotalAdultQSet)
        # # Getting Values of QuerySet
        TotalAdult = 0
        for adultval in TotalAdultQSet:
            AdultValues = int(adultval['total_adult_x340'])
            # print(AdultValues)
            TotalAdult = TotalAdult + AdultValues
        print("\nTotalAdult: ",TotalAdult)


        # Total Child______
        TotalChildQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_child_x340')
        TotalChild = 0
        for childval in TotalChildQSet:
            ChildValues = int(childval['total_child_x340'])
            TotalChild = TotalChild + ChildValues
        print("\nTotalChild: ",TotalChild)


        # Total Per Unit______
        TotalPerUnitQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_perunit_x340')
        TotalPerUnit = 0
        for perunitval in TotalPerUnitQSet:
            PerUnitValues = int(perunitval['total_perunit_x340'])
            TotalPerUnit = TotalPerUnit + PerUnitValues
        print("\nTotalPerUnit: ",TotalPerUnit)

        # Total Cash______
        TotalCashQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_cash_collected_x340')
        TotalCash = 0
        for cashval in TotalCashQSet:
            TotalCashValues = int(cashval['total_cash_collected_x340'])
            TotalCash = TotalCash + TotalCashValues
        print("\nTotalCash: ",TotalCash)

        # Total Card______
        TotalCardQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_card_collected_x340')
        TotalCard = 0
        for cardval in TotalCardQSet:
            TotalCardValues = int(cardval['total_card_collected_x340'])
            TotalCard = TotalCard + TotalCardValues
        print("\nTotalCard: ",TotalCard)

        # Total UPI______
        TotalUpiQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_upi_collected_x340')
        TotalUpi = 0
        for upival in TotalUpiQSet:
            TotalUpiValues = int(upival['total_upi_collected_x340'])
            TotalUpi = TotalUpi + TotalUpiValues
        print("\nTotalCard: ",TotalUpi)

        # Total Revenue Collected______
        RevenueValuesQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_revenue_collected_x340')
        # print("\nTotalRevenue: ",RevenueValuesQSet)
        # # Getting Values of QuerySet
        TotalRevenueValue = 0
        for revenue in RevenueValuesQSet:
            RevenueValues = int(revenue['total_revenue_collected_x340'])
            # print(RevenueValues)
            TotalRevenueValue = TotalRevenueValue + RevenueValues
        print("\nTotalRevenueValue: ",TotalRevenueValue)


        context = {
            'report_generated_date':ReportGenDt,
            'report_generated_time':ReportGenTime,
            'counter_no':CounterNo,
            'user_name':UserName,
            'zoo_name':ZooName,
            'ticketnumber':TicketNumber,
            'totaltickets':TotalNoTickets,
            'daterange':DateRange,
            'selecteddata_x340':SelectedData_x340,
            'totaladult':TotalAdult,
            'totalchild':TotalChild,
            'totalperunit':TotalPerUnit,
            'totalcash':TotalCash,
            'totalcard':TotalCard,
            'totalupi':TotalUpi,
            'totalrevenue':TotalRevenueValue
        }

        return render(request, 'statement.html', context)

    
    # context = {'daterange':DateRange,'data_x300':DataFrm_x300, 'data_x340':DataFrm_x340}
    return render(request, 'statement.html')





def summary(request):
    DateRange=0

    ReportGenDt = datetime.now().date().strftime("%d-%B-%Y")
    ReportGenTime = datetime.now().time().strftime("%H:%M %p")
    print("Report Dt & Time: ",ReportGenDt, " | ",  ReportGenTime)

    OpenTime = '00:00:00'
    CloseTime = '23:59:59'

    if request.method == "POST":
        DateRange = request.POST.get('date_range')
        print("\nDate Range: ", DateRange)

        DateRangeList = DateRange.split("-")
        FrmYY = (DateRangeList[2]).replace(' ', '')
        FrmMM = DateRangeList[1]
        FrmDD = DateRangeList[0]
        SelectedDateFrm = FrmYY+'-'+FrmMM+'-'+FrmDD

        DDTo = (DateRangeList[3]).replace(' ', '')
        MMTo = DateRangeList[4]
        YYTo = DateRangeList[5]

        SelectedDateTo = YYTo+'-'+MMTo+'-'+DDTo

        print(DateRangeList)
        print(SelectedDateFrm)
        print(SelectedDateTo)
              
        DateFrm = SelectedDateFrm+' '+OpenTime
        DateTo = SelectedDateTo+' '+CloseTime

        print("\nDate From: ",DateFrm)
        print("Date To: ",DateTo,'\n')

        SelectedData_x340 = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values()


        TotalNoTickets = (Xamp340TicketSoldDetails.objects.last()).ticket_sold_details_id_x340

        TicketNumber = (Xamp340TicketSoldDetails.objects.last()).ticket_no_x340


        # Total Adult______
        TotalAdultQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_adult_x340')
        # print("\nTotalRevenue: ", TotalAdultQSet)
        # # Getting Values of QuerySet
        TotalAdult = 0
        for adultval in TotalAdultQSet:
            AdultValues = int(adultval['total_adult_x340'])
            # print(AdultValues)
            TotalAdult = TotalAdult + AdultValues
        print("\nTotalAdult: ",TotalAdult)


        # Total Child______
        TotalChildQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_child_x340')
        TotalChild = 0
        for childval in TotalChildQSet:
            ChildValues = int(childval['total_child_x340'])
            TotalChild = TotalChild + ChildValues
        print("\nTotalChild: ",TotalChild)


        # Total Per Unit______
        TotalPerUnitQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_perunit_x340')
        TotalPerUnit = 0
        for perunitval in TotalPerUnitQSet:
            PerUnitValues = int(perunitval['total_perunit_x340'])
            TotalPerUnit = TotalPerUnit + PerUnitValues
        print("\nTotalPerUnit: ",TotalPerUnit)

        # Total Cash______
        TotalCashQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_cash_collected_x340')
        TotalCash = 0
        for cashval in TotalCashQSet:
            TotalCashValues = int(cashval['total_cash_collected_x340'])
            TotalCash = TotalCash + TotalCashValues
        print("\nTotalCash: ",TotalCash)

        # Total Card______
        TotalCardQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_card_collected_x340')
        TotalCard = 0
        for cardval in TotalCardQSet:
            TotalCardValues = int(cardval['total_card_collected_x340'])
            TotalCard = TotalCard + TotalCardValues
        print("\nTotalCard: ",TotalCard)

        # Total UPI______
        TotalUpiQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_upi_collected_x340')
        TotalUpi = 0
        for upival in TotalUpiQSet:
            TotalUpiValues = int(upival['total_upi_collected_x340'])
            TotalUpi = TotalUpi + TotalUpiValues
        print("\nTotalCard: ",TotalUpi)

        # Total Revenue Collected______
        RevenueValuesQSet = Xamp340TicketSoldDetails.objects.filter(created_on_x340__range=(DateFrm, DateTo)).values('total_revenue_collected_x340')
        # print("\nTotalRevenue: ",RevenueValuesQSet)
        # # Getting Values of QuerySet
        TotalRevenueValue = 0
        for revenue in RevenueValuesQSet:
            RevenueValues = int(revenue['total_revenue_collected_x340'])
            # print(RevenueValues)
            TotalRevenueValue = TotalRevenueValue + RevenueValues
        print("\nTotalRevenueValue: ",TotalRevenueValue)



    # i=0
    # for i in range(LastEvntID):
    #     No_of_Tickets =''
    #     Event_Name = Xamp340TicketSoldDetails.objects.only('event_id_from_t520_x340').get(pk=i).event_name_t130_t530_x340
    #     Total_Adult = ''
    #     Total_Child = ''
    #     Total_Cash = ''
    #     Total_Card = ''
    #     Total_Upi = ''
    #     Total_Rev = ''

    #     # TICKET REPRINT DETAILS
    #     TicketNo_EventName =''
    #     RePrinted_Count = ''
    #     Value = ''


    context = {
        'report_generated_time':ReportGenTime,
        'report_generated_dt':ReportGenDt,
        'daterange':DateRange,
        # 'selecteddata_x340':SelectedData_x340,
    }

    return render(request, 'summary.html', context)





def counter_close(request):
    # Check Internet Link
    def internet_on():
        return (lambda a: True if 0 == a.system('ping 8.8.8.8 -n 1 > clear') else False)(__import__('os'))
    InternetStatus = internet_on()

    if InternetStatus == True:
        Internet = 'OK'
        API_ConnectionCheck = "api/tapi/connection_check_api"
        api_url_linking = str(ZOO_API_URL+API_ConnectionCheck)            
        response = requests.post(api_url_linking, headers=Headers)            
        print("\nConnection Status Code: ", response.status_code)
        print("\nConnection Response: ", response.text)
        if response.status_code == 200:  
            TicketCloudStatus = 'OK'

    strStartTime = str(StartTime)    
    if strStartTime <= '11:59':
        starttimestr = "Good Morning"
    elif strStartTime >= '12:00' and strStartTime <= '16:59':
        starttimestr = "Good Afternoon"
    else:
        starttimestr = "Good Evening"

    context = {
        'internet':Internet, 
        'ticketcloud':TicketCloudStatus,
        'startdt':StartDate,
        'starttime':StartTime,
        'starttimestr':starttimestr
    }
    return render(request, 'counter_close.html', context)


def preview_closing(request):
    return render(request, 'preview_closing.html')


def collection(request):
    return render(request, 'collection.html')
