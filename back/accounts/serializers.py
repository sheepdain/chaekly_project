from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': '이메일을 입력해 주세요.',
            'invalid': '유효한 이메일 주소를 입력해 주세요.'
        }
    )
    nickname = serializers.CharField(
        required=True,
        max_length=15,
        error_messages={
            'required': '닉네임을 입력해 주세요.',
            'max_length': '닉네임은 최대 15자까지 가능합니다.'
        }
    )
    gender = serializers.ChoiceField(
        choices=[('M', '남성'), ('F', '여성')],
        required=True,
        error_messages={
            'required': '성별을 선택해 주세요.',
            'invalid_choice': '유효한 성별을 선택해 주세요.'
        }
    )
    age = serializers.IntegerField(
        required=True,
        min_value=0,
        error_messages={
            'required': '나이를 입력해 주세요.',
            'min_value': '나이는 0 이상의 숫자여야 합니다.',
            'invalid': '숫자를 입력해 주세요.'
        }
    )
    profile_image = serializers.ImageField(
        required=False,
        error_messages={
            'invalid_image': '이미지 파일만 업로드할 수 있습니다.'
        }
    )
    introduction = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
        error_messages={
            'max_length': '소개글은 500자 이내로 작성해 주세요.'
        }
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['email'] = self.validated_data.get('email')
        data['nickname'] = self.validated_data.get('nickname')
        data['gender'] = self.validated_data.get('gender')
        data['age'] = self.validated_data.get('age')
        data['profile_image'] = self.validated_data.get('profile_image')
        data['introduction'] = self.validated_data.get('introduction', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.email = self.validated_data.get('email')
        user.nickname = self.validated_data.get('nickname')
        user.gender = self.validated_data.get('gender')
        user.age = self.validated_data.get('age')
        user.profile_image = self.validated_data.get('profile_image')
        user.introduction = self.validated_data.get('introduction', '')
        user.save()
        return user
        

    def validate_nickname(self, value):
        stripped = value.strip()
        # 자음 또는 모음만으로 이루어진 닉네임 필터링
        if all('\u3131' <= char <= '\u314E' or '\u314F' <= char <= '\u3163' for char in stripped):
            raise serializers.ValidationError('사용할 수 없는 닉네임입니다.')
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError('이미 사용 중인 닉네임입니다.')
        return value

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('아이디를 입력해 주세요.')

        # 영문자, 숫자, 언더스코어만 허용 (4~20자 등 제한은 자유롭게 조절)
        if not re.fullmatch(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError('아이디는 영문자, 숫자, 언더스코어만 사용할 수 있습니다.')
        
        if not 4 <= len(value) <= 20:
            raise serializers.ValidationError('아이디는 4자 이상 20자 이하로 입력해 주세요.')


        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('이미 사용 중인 아이디입니다.')

        return value

    def validate_password1(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('비밀번호는 최소 8자 이상이어야 합니다.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('이미 사용 중인 이메일입니다.')
        return value

    def validate(self, data):
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError({'password2': '비밀번호가 일치하지 않습니다.'})
        return data
    
