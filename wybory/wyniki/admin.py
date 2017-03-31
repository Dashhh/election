from django.contrib import admin
from .models import Candidate, Commune, Province

# Register your models here.


class CommuneAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'candidate1_votes', 'candidate2_votes']
    exclude = ('candidate1', 'candidate2')

    def has_add_permission(self, request):
        if Candidate.objects.select_for_update().all().count() == 2:
            return True
        else:
            return False


class CandidateAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() == 2:
            return False
        else:
            return True


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Commune, CommuneAdmin)
