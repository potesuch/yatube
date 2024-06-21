from django.utils.timezone import now
from rest_framework import serializers
import webcolors
from .models import Cat, User, Achievement, AchievementCat, CHOICES


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет названия')
        return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('achievement_name',)


class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True, required=False)
    age = serializers.SerializerMethodField()
    #color = Hex2NameColor()
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements',
                  'age')
        read_only_fields = ('owner', )

    def create(self, validated_data):
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        achievements = validated_data.pop('achievements')
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat)
        return cat

    def update(self, instance, validated_data):
        if 'achievements' not in self.initial_data:
            super().update(instance, validated_data)
            return instance
        achievements = validated_data.pop('achievements')
        instance_achievements = AchievementCat.objects.filter(cat=instance)
        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            if current_achievement not in instance_achievements:
                AchievementCat.objects.create(
                    achievement=current_achievement, cat=instance)
        for achievement in instance_achievements:
            if achievement not in achievements:
                achievement.delete()
        super().update(instance, validated_data)
        return instance

    def validate_birth_year(self, value):
        year = now().year
        if not (year - 40 < value <= year):
            raise serializers.ValidationError('Проверьте год рождения!')
        return value

    def get_age(self, obj):
        return now().year - obj.birth_year


class UserSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'cats')
