from django.shortcuts import render
from core.forms import SubmissaoForm, PreSubmissaoForm


def index(request):
    return render(request, 'index.html')


def pre_lancamento(request):
    url = 'pre_lancamento.html'
    if request.method == 'GET':
        form = PreSubmissaoForm()
    if PreSubmissaoForm(request.POST).is_valid():
        form = SubmissaoForm(request.POST)
        url = 'lancamento.html'
    else:
        form = PreSubmissaoForm(request.POST)
    context = {'form': form}
    return render(request, url, context)


def lancamento(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    form = SubmissaoForm(request.POST)
    if form.is_valid():
        form.save()
        return render(request, 'index.html')
    else:
        context = {'form': form}
        return render(request, 'lancamento.html', context)


def placar_estatico(request):
    return render(request, 'placar_estatico.html')
