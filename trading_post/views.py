from django.shortcuts import render, redirect
from django.views import generic
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.


class TransactionListView(generic.ListView):
    model = Transaction

    def get_queryset(self):
        return super(TransactionListView, self).get_queryset().filter(status='O')


class TransactionDetailView(generic.DetailView):
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super(TransactionDetailView, self).get_context_data(**kwargs)
        form = OfferForm()
        form.fields['card'].queryset = self.request.user.profile.deck.all()
        context['form'] = form
        return context


class CardListView(generic.ListView):
    model = Card


class CardDetailView(generic.DetailView):
    model = Card

@login_required
def create_transaction(request, card_id):
    card = Card.objects.get(pk=card_id)
    if card not in request.user.profile.deck.all():
        # TODO: add error message that you dont own card 
        return redirect('card_list')
    transaction, created = Transaction.objects.get_or_create(card=card, seller=request.user.profile)
    # TODO: success/failure message if unique or not

    return redirect('transaction_list')


@login_required
def create_offer(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    form = OfferForm(request.POST)
    offer = form.save(commit=False)
    if offer.card in request.user.profile.deck.all():
        offer.transaction = transaction
        offer.buyer = request.user.profile
        offer.save()
    # if card in request.user.profile.deck.all():
    #     # TODO: add error message that you dont own card
    #     offer, created = Offer.objects.get_or_create(card=card, buyer=request.user.profile, transaction=transaction)
    # # TODO: success/failure message if unique or not

    return redirect('transaction_view', pk=transaction_id)


@login_required
def eval_offer(request, offer_id, accepted):
    offer = Offer.objects.get(pk=offer_id)
    transaction = offer.transaction
    if transaction in request.user.profile.transaction_set.all():
        if accepted:
            offer.status = 'A'
            transaction.status = 'C'
            transaction.save()
            offer.save()
            offer.buyer.deck.remove(offer.card)
            offer.buyer.deck.add(transaction.card)
            transaction.seller.deck.add(offer.card)
            transaction.seller.deck.remove(transaction.card)
            return redirect('transaction_list')
        else:
            offer.status = 'R'
            offer.save()
              
    else:
        # TODO: add error message that this offer isnt to a transaction of yours
        pass
    return redirect('transaction_view', pk=transaction.id)


@login_required
def show_deck(request):
    return render(request, 'trading_post/my_deck.html')
