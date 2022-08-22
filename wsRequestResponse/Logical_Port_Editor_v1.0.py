from requests import Session
from zeep import Client, Settings
from zeep.transports import Transport
import urllib3
import time
import sys
import getpass

#disable certificate warnings from beginning because webservice gives a warning.
urllib3.disable_warnings()

###########################################################################

#built a main function that gets called at the end.
def main():
    
    print("Welcome to the logical port editor.")
    user = User()
    ses = session_setup()
    client = client_setup(ses)
    login(user) 
    cv_login(client, user)
    loggedIn = cv_isloggedin(client)
    
    while(not(loggedIn)):
        print("Incorrect username or password, please try again.")
        login(user)
        cv_login(client, user)
        loggedIn = cv_isloggedin(client)    

    print("Successfully logged in.")

    logical = Logical()

    loop = True

    while(loop):
        choice = input("Would you like to add or delete positions('add' or 'delete')? ").upper().strip()
        while(choice != 'ADD' and choice != 'DELETE'):
            choice = input("Invalid entry, would you like to add or delete positions('add' or 'delete')? ").upper().strip()
                 
        if(choice == 'ADD'):
            cv_location(client, logical)
            cv_floor(client, logical)
            cv_frame(client, logical)
            shelfId(logical)
            cv_equipmentType(client, logical)
            cv_workorder(client, logical)
            position_range(logical)
            
            cv_shelf_save(client, logical)
            print("Logical port additions completed.")

        else:
            cv_location(client, logical)
            cv_floor(client, logical)
            cv_frame(client, logical)
            shelfId(logical)
            
            cv_shelf_delete(client, logical)
        
        completeQuestion = input("Would you like to perform another operation or would you like to exit('yes' or 'exit')?: ").upper().strip()
        while(completeQuestion != 'YES' and completeQuestion != 'EXIT'):
            completeQuestion = input("Invalid input, would you like to perform another operation or would you like to exit('yes' or 'exit')?: ").upper().strip()
        
        if(completeQuestion == 'EXIT'):
            loop = False
        
    client.service.disconnect()
    ses.close()

###########################################################################

#User class for creating user objects.
class User:
    username = ''
    password = ''

#Logical class for creating logical objects.
class Logical:
    location = ''
    floor = ''
    frame = ''
    shelf = ''
    equipmentType = ''
    workorder = ''
    positionFrom = ''
    PositionTo = ''

#Login function for getting user credentials and passing to the user object.
def login(user):
    user.username = input("Please enter your username: ").upper().strip()
    user.password = getpass.getpass("Please enter your password: ").strip()
    
#Create a session.    
def session_setup():
    ses = Session()
    ses.verify = False
    return ses

#Connect to the CV client.
def client_setup(ses):
    transport = Transport(session=ses)
    settings = Settings(strict=False)
    #Development webservices link
    wsdl = 'https://btln001137.corp.ads:9043/cvnetDV/services/CvCommon?wsdl'
    #Production webservices link
    #wsdl = 'https://btlp000229.corp.ads:9043/cvnetPR/services/CvCommon?wsdl'
    try:
        client = Client(wsdl=wsdl, transport=transport, settings=settings)
        return client
    except:
        print("Failed to connect to CV, exiting...")
        time.sleep(3)
        sys.exit()

#Login to the CV client with the user object.
def cv_login(client, user):
    client.service.login(user=user.username, password=user.password)

#Confirms the user is logged into the CV client.
def cv_isloggedin(client):
    response = client.service.isLoggedIn()
    return response

#Gets a location from the user and validates that the location exists.
def cv_location(client, logical):
    logical.location = input("Please enter a location: ").upper().strip()
    location_response = client.service.location_get(logical.location)
    while(location_response.location is None):
        logical.location = input("Invalid location, please enter again: ").upper().strip()
        location_response = client.service.location_get(logical.location)

#Gets a floor from the user and validates that the floor exists at given location.
def cv_floor(client, logical):
    logical.floor = input("Please enter a floor: ").strip()
    floor_response = client.service.locationFloor_getByLocation(logical.location)
    floorExist = False
    while(not floorExist):
        for x in floor_response:
            if(x.floor == logical.floor):
                floorExist = True
                break
        if(not floorExist):
            logical.floor = input("That floor does not exist at " + logical.location + " please enter again: ").strip()
            floor_response = client.service.locationFloor_getByLocation(logical.location)

#Gets a frame from the user and validates that the frame exists in that given floor at the given location.
def cv_frame(client, logical):
    logical.frame = input("Please enter a frame/bay: ").upper().strip()
    frame_response = client.service.frameInfo_get(logical.location, logical.floor, logical.frame)
    while(frame_response.frame is None):
        logical.frame = input("That frame does not exist, please enter again: ").upper().strip()
        frame_response = client.service.frameInfo_get(logical.location, logical.floor, logical.frame)

#Gets a shelfID from the user.
def shelfId(logical):
    logical.shelf = input("Please enter the shelf ID(Max 20 characters): ").upper().strip()
    while(len(logical.shelf) > 20):
        logical.shelf = input("Too many characters, Please enter the shelf ID(Max 20 characters): ").upper().strip()    

#Gets the equipment type from the user and validates that it exists in CV.
def cv_equipmentType(client, logical):
    logical.equipmentType = input("Please enter in the equipment type: ").upper().strip()
    equipmentType_response = client.service.equipping_getEquipmentDescription(logical.equipmentType)
    while(equipmentType_response is None):
        logical.equipmentType = input("That equipment type does not exist in CV, please enter again: ").upper().strip()
        equipmentType_response = client.service.equipping_getEquipmentDescription(logical.equipmentType)

#Gets the workorder from the user and validates that it exists and isn't completed.
def cv_workorder(client, logical):
    logical.workorder = input("Please enter your workorder: ").upper().strip()
    workorder_response = client.service.workorder_getById(logical.workorder)
    while(workorder_response.workorder is None):
        logical.workorder = input("That workorder does not exist, please enter again: ").upper().strip()
        workorder_response = client.service.workorder_getById(logical.workorder)
    while(workorder_response.completionDate is not None):
        logical.workorder = input("That workorder has been completed, please enter a new one: ").upper().strip()
        workorder_response = client.service.workorder_getById(logical.workorder)

#Gets the range of positions from the user that they want to add.
def position_range(logical):
    pRange = input("Please enter the range you would like to use(1 = 1-1993, 2 = 1-4009, 3 = 2017-4009): ").strip()
    while(pRange != '1' and pRange != '2' and pRange != '3'):
        pRange = input("Incorrect entry, Please enter the range you would like to use(1 = 1-1993, 2 = 1-4009, 3 = 2017-4009): ").strip()
    if(pRange == '1'):
        logical.positionFrom = '1'
        logical.positionTo = '1993'
    elif(pRange == '2'):
        logical.positionFrom = '1'
        logical.positionTo = '4009'
    else:
        logical.positionFrom = '2017'
        logical.positionTo = '4009'

#Adds the new shelf and each of the positons.
def cv_shelf_save(client, logical):
    print("Adding...")
    for x in range(int(logical.positionFrom), int(logical.positionTo) + 1, 24):
        try:
            response = client.service.shelfPositions_save(equipmentGroup={
                'equipmentType': logical.equipmentType,
                'floor': logical.floor,
                'forAssembly': 'Yes',
                'frame': logical.frame,
                'location': logical.location,
                'owner': 'TCC',
                'positionFrom': x,
                'positionTo': x,
                'shelf': logical.shelf,
                'workorder': logical.workorder
                })
        except:
            print("Failed to add shelf with position: " + str(x))

#Deletes the shelf and all of its positions.
def cv_shelf_delete(client, logical):
    try:
        shelfList = []
        shelfList_response = client.service.shelfPositions_getList(logical.location, logical.floor, logical.frame, logical.shelf, '', '', '', '0', '1000')
        for x in shelfList_response:
            if(x.shelf == logical.shelf):
                shelfList.append(x.eqSysid)
        if(len(shelfList) > 0):            
            print("Deleting...")
            for x in shelfList:
                response = client.service.shelfPositions_delete(x)
            print("Logical port deletions completed.")
        else:
            print("Failed to delete, that shelf does not exist.")
    except:
        if(len(shelfList) > 0):
            positionResponse = client.service.shelfPositions_getSelection(x)
            failedPositionFrom = positionResponse.positionFrom
            failedPositionTo = positionResponse.positionTo
            print("Failed to delete that shelf at position(s) " + failedPositionFrom + " - " + failedPositionTo + ", please check CV and try again.")
        else:
            print("Failed to delete, that shelf does not exist.")

#Calls the main functions after reading everything else.
if __name__ == "__main__":
    main()
