from django.shortcuts import render
from core.forms import SubmissaoForm, PreSubmissaoForm
from core.models import SubmissaoModel


def index(request):
    return render(request, 'index.html')


def pre_lancamento(request):
    url = 'pre_lancamento.html'
    if request.method == 'GET':
        form = PreSubmissaoForm()
    if PreSubmissaoForm(request.POST).is_valid():
        form = SubmissaoForm(request.POST)
        url = 'lancamento.html'
        qs = _buscar_submissoes_lancadas(form)
        context = {'form': form, 'qs': qs}
    else:
        form = PreSubmissaoForm(request.POST)
        context = {'form': form}
    return render(request, url, context)


def _buscar_submissoes_lancadas(form):
    prob_selec = form.data.get('problema', '')
    equipe_selec = form.data.get('equipe', '')
    query_set = SubmissaoModel.objects.filter(
        problema=prob_selec).filter(equipe=equipe_selec)
    return query_set


def lancamento(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    form = SubmissaoForm(request.POST)
    if form.is_valid():
        form.save()
        context = {'form': PreSubmissaoForm()}
        return render(request, 'pre_lancamento.html', context)
    else:
        context = {'form': form}
        return render(request, 'lancamento.html', context)


def editar_lancamento(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    id_lancamento = request.POST.get('id_lancamento', '')
    vitima = SubmissaoModel.objects.get(pk=id_lancamento)
    if SubmissaoForm(request.POST).is_valid():
        form = SubmissaoForm(request.POST, instance=vitima)
        form.save()
        context = {'form': PreSubmissaoForm()}
        return render(request, 'pre_lancamento.html', context)
    else:
        form = SubmissaoForm(instance=vitima)
        context = {'form': form, 'id_lancamento': id_lancamento}
        return render(request, 'editar_lancamento.html', context)


def remover_lancamento(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    try:
        id_lancamento = request.POST.get('id_lancamento', '')
        vitima = SubmissaoModel.objects.get(pk=id_lancamento)
        vitima.delete()
        context = {'form': PreSubmissaoForm()}
    except SubmissaoModel.DoesNotExist:
        context = {'form': PreSubmissaoForm(), 'id_lancamento': id_lancamento}
    return render(request, 'pre_lancamento.html', context)


def placar_estatico(request):
    return render(request, 'placar_estatico.html')
