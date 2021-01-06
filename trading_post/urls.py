from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('transaction_list/', views.TransactionListView.as_view(), name='transaction_list'),
    path('deck/', views.show_deck, name='show_deck'),
    path('transaction/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction_view'),
    path('', views.CardListView.as_view(), name='card_list'),
    path('card/<int:pk>/', views.CardDetailView.as_view(), name='card_view'),
    path('start/card/<int:card_id>', views.create_transaction, name="create_transaction"),
    path('start/offer/<int:transaction_id>', views.create_offer, name="create_offer"),
    path('eval/offer/<int:offer_id>/<int:accepted>', views.eval_offer, name="eval_offer"),

]
