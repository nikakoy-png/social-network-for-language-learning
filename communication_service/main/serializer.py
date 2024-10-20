from rest_framework import serializers

from main.models import Dialog, Feedback, Complaint, Message, UserDialog, User, Language, UserLanguages, \
    LevelLanguageENUM


class DialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = '__all__'


class UserDialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDialog
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    feedback = FeedbackSerializer(many=False)

    class Meta:
        model = Message
        fields = ('dialog',
                  'sender_id',
                  'id',
                  'text',
                  'send_date',
                  'is_read',
                  'is_deleted',
                  'feedback',)


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class UserLanguagesSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(many=False)
    proficiency_level = serializers.ChoiceField(choices=LevelLanguageENUM.choices)
    is_learning = serializers.BooleanField()

    class Meta:
        model = UserLanguages
        fields = ['id', 'language', 'proficiency_level', 'is_learning']


class UserSerializer(serializers.ModelSerializer):
    languages = UserLanguagesSerializer(source='userlanguages_set', many=True)
    photo = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'gender',
                  'first_name',
                  'last_name',
                  'status',
                  'last_active_date',
                  'registration_date',
                  'photo',
                  'phone',
                  'birth_date',
                  'languages',
                  )


class ResolutionSerializer(serializers.Serializer):
    resolution = serializers.CharField(max_length=1000)