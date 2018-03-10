import datetime
import pytz

from django.shortcuts import render

from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import activate

from books.models import Review, Category
# from .models import Votation

# from celery.schedules import crontab
# from celery.task import periodic_task


# @periodic_task(run_every=crontab(hour=13, minute=27, day_of_week="sun"))
# def every_monday_morning():
#     print("This is run every Monday morning at 7:30")

class HomeView(View):
	def get(self, request, *args, **kwargs):
		context = {}

		# context['vstart'] = vstart
		# context['timezone_now'] = user_now_aware

		# d, h, m, s, started = get_time_left(request.user)

		# context['days_left'] = d
		# context['hours_left'] = h
		# context['minutes_left'] = m
		# context['seconds_left'] = s
		# context['started'] = started
		context['category'] = Category.objects.get(title__iexact='Habilidades sociales')


		return render(request, 'home_view.html', context)
