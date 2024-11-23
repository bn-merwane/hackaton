
from django.contrib import admin
from django.urls import path,include
from apps.analytics.views import Analysis

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("apps.accounts.urls") ),
    path('ticket/',include("apps.tickets.urls")),
    path('posts/', include("apps.posts.urls")),
    path('analysis/',Analysis.as_view())

]
