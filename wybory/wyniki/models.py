from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Create your models here.

commune_types = (
    ('city', 'miasto'),
    ('village', 'wies'),
    ('abroad', 'zagranica'),
    ('ship', 'statek')
)

people_ranges = (
    (0, 5000, "do 5000"),
    (5001, 10000, "od 5 001 do 10 000"),
    (10001, 20000, "od 10 001 do 20 000"),
    (20001, 50000, "od 20 001 do 50 000"),
    (50001, 100000, "od 50 001 do 100 000"),
    (100001, 200000, "od 100 001 do 200 000"),
    (200001, 500000, "od 200 001 do 500 000"),
    (500000, 1000000000, "pow. 500 000")
)


def cand(number):
    obj = Candidate.objects.all()[number]
    if obj:
        return obj.first_name + " " + obj.last_name


def candpk(number):
    object = Candidate.objects.select_for_update().all()[number]
    if object:
        return object.pk


class Province(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nazwa')
    identifier = models.CharField(max_length=5, verbose_name='Identyfikator', primary_key=True)

    @staticmethod
    def get_names():
        objs = Province.objects.all();
        names = []
        for obj in objs:
            names += (obj.pk, obj.name)
        return names

    def __str__(self):
        return self.name;

    @staticmethod
    def results():
        results = []
        for obj in Province.objects.all().order_by('name'):
            province = []
            province.append(obj.__str__())
            for i in range (0, 4):
                province.append(0)
            province[3] = '50%'
            for commune in Commune.objects.filter(province=obj.pk):
                province[1] += commune.correctly_filled_forms
                province[2] += commune.candidate1_votes
                province[4] += commune.candidate2_votes
            if province[1] != 0:
                province[3] = str(round(province[2]/province[1]*100)) + '%'
            results.append(province)
        for i in (10, 10, 4):
            province = results.pop(results.__len__()-1)
            results.insert(i, province)
        return results

    class Meta:
        verbose_name = "Województwo"
        verbose_name_plural = "Województwa"


class Candidate(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Imie')
    last_name = models.CharField(max_length=30, verbose_name='Nazwisko')

    def clean(self):
        if Candidate.objects.select_for_update().all().count() == 2:
            raise ValidationError(_("Kandydaci zostali dodani!"))

    def __str__(self):
        return self.first_name + " " + self.last_name

    @staticmethod
    def overall():
        candidates = []
        for cand in Candidate.objects.all():
            candidates.append([cand.__str__()])
        cand1 = 0
        cand2 = 0
        for com in Commune.objects.all():
            cand1 += com.candidate1_votes
            cand2 += com.candidate2_votes
        if Candidate.objects.count() == 2:
            candidates[0].append(cand1)
            candidates[0].append(str(round(cand1/(cand1+cand2)*100))+"%")
            candidates[0].append("black")
            candidates[1].append(cand2)
            candidates[1].append(str(round(cand2/(cand1+cand2)*100))+"%")
            candidates[1].append("red")
        return candidates


    class Meta:
        verbose_name = "Kandydata"
        verbose_name_plural = "Kandydaci"


class Commune(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nazwa gminy')
    type = models.CharField(max_length=7, choices=commune_types, verbose_name='Typ')
    province = models.ForeignKey(Province, verbose_name='Województwo')
    habitancy = models.IntegerField(verbose_name='Liczba mieszkancow')
    privileged = models.IntegerField(verbose_name='Liczba uprawnionych')
    given_forms = models.IntegerField(verbose_name='Liczba wydanych kart')
    filled_forms = models.IntegerField(verbose_name='Liczba wypelnionych kart')
    correctly_filled_forms = models.IntegerField(verbose_name='Liczba poprawnie wypelnionych kart')
    candidate1 = models.ForeignKey(Candidate, default=candpk(0), related_name='candidate1')
    candidate1_votes = models.IntegerField(verbose_name=cand(0))
    candidate2 = models.ForeignKey(Candidate, default=candpk(1), related_name='candidate2')
    candidate2_votes = models.IntegerField(verbose_name=cand(1))

    @staticmethod
    def size_results():
        results = []
        result = ['statki i zagranicza']
        types = ['abroad', 'ship']
        for i in range(0,4):
            result.append(0)
        result[3] = '50%'
        for obj in Commune.objects.filter(type__in=types):
            result[1] += obj.correctly_filled_forms
            result[2] += obj.candidate1_votes
            result[4] += obj.candidate2_votes
        if result[1] != 0:
            result[3] = str(round(result[2]/result[1]*100)) + "%"
        results.append(result)
        for size in people_ranges:
            result = [size[2]]
            for i in range(0,4):
                result.append(0)
            result[3] = '50%'
            for obj in Commune.objects.exclude(type__in=types).filter(habitancy__gte=size[0], habitancy__lt=size[1]):
                result[1] += obj.correctly_filled_forms
                result[2] += obj.candidate1_votes
                result[4] += obj.candidate2_votes
            if result[1] != 0:
                result[3] = str(round(result[2]/result[1]*100)) + "%"
            results.append(result)
        return results


    @staticmethod
    def types_results():
        results = []
        for type in commune_types:
            result = []
            result.append(type[1])
            for i in range(0,4):
                result.append(0)
            result[3] = '50%'
            for obj in Commune.objects.filter(type=type[0]):
                result[1] += obj.correctly_filled_forms
                result[2] += obj.candidate1_votes
                result[4] += obj.candidate2_votes
            if result[1] != 0:
                result[3] = str(round(result[2]/result[1]*100)) + '%'
            results.append(result)
        return results

    class Meta:
        verbose_name = "gmina"
        verbose_name_plural = "gminy"

    def get_numbers(self):
        values = []
        values.append(self.habitancy)
        values.append(self.privileged)
        values.append(self.given_forms)
        values.append(self.filled_forms)
        values.append(self.correctly_filled_forms)
        values.append(self.candidate1_votes)
        values.append(self.candidate2_votes)
        return values

    def clean(self):
        values = self.get_numbers()
        for i in range(0, 3):
            if values[i] < values[i+1]:
                raise ValidationError(_("Wartość wiersza " + str(i+3) + " jest mniejsza od " + str(i+4)))
            if values[-1] + values[-2] != values[-3]:
                raise ValidationError(_("Wyniki głosów na kandydatów nie sumują się do liczby poprawnie wypelnionych kart"))

    def __str__(self):
        return self.name + " (" + str(self.province) + ")"


