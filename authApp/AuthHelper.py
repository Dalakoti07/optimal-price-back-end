import requests
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from .customJWTUtils import jwt_payload_handler
from rest_framework_jwt.settings import api_settings
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from .serializers import UserSerializer
from .models import User

def askForOTPFromMsg91(userPhoneNumber):
    # get request 
    results =requests.get("https://api.msg91.com/api/v5/otp?authkey=342362ApTFZMcg5hW5f68b46aP1&mobile=91{}".format(userPhoneNumber))
    return results

def validateTheOTPFromMsg91(userPhoneNumber,otpByUser):
    # get request 
    results= requests.get("https://api.msg91.com/api/v5/otp/verify?mobile=91{}&otp={}&authkey=342362ApTFZMcg5hW5f68b46aP1".format(userPhoneNumber,otpByUser))
    return results

# after otp validation u get access token
@api_view(['POST','GET'])
@permission_classes([])
def OTPView(request):
    if request.method=='POST':
        userPhoneNumber=request.data['number']
        print("validating otp for :",userPhoneNumber)
        otp=request.data['otp']
        results=validateTheOTPFromMsg91(userPhoneNumber,otp)
        jsonResponse=results.json()
        if (not (results.status_code ==200)) or (jsonResponse['type']=='error'):
            return Response({'message':"Invalid OTP or OTP Expired"},400)
        else:
            # get the user details and send token
            # phone number should be unique

            user=User.objects.all().filter(mobile=userPhoneNumber)
            user=user[0]
            payload = jwt_payload_handler(user)

            return Response({
                'token': jwt_encode_handler(payload),
                'user': UserSerializer(user).data
            },200)
            return Response({'message':"Success"},200)
    
    if request.method=='GET':
        userPhoneNumber=request.GET['number']
        print("getting otp for ",userPhoneNumber)
        results=askForOTPFromMsg91(userPhoneNumber)
        if results.status_code ==200:
            return Response({'message':"OTP successfully generated "})
        else:
            return Response({'message':"Could not generate OTP"},400)


# used when user is trying to log in, do custom login 
@api_view(['POST'])
@permission_classes([])
def loginUser(request):
    username=request.data['email']
    password=request.data['password']
    credentials = {
            'email': username,
            'password': password
        }
    user = authenticate(**credentials)

    if user:
        if not user.is_active:
            msg = _('User account is disabled.')
            return Response({'message':msg},400)

        return Response({
            'user': UserSerializer(user).data
        },200)
    else:
        msg = 'Unable to log in with provided credentials.'
        return Response({"message":msg},400)
