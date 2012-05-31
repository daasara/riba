# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.models import formset_factory, inlineformset_factory
from question.models import *
from question.forms import *
from random import randint
from django.utils.html import escape

def view_all_questions(request):
    q = request.GET.get('q')
    if q:
        questions = QuestionTree.objects.select_related('question', 'parent_question').filter(question__question__icontains=q).order_by('-id')
    else:
        questions = QuestionTree.objects.select_related('question', 'parent_question').filter(parent_question=None, parent_value=None).order_by('-id')
    ques = {}
    for qs in questions:
        qt = QuestionTree.objects.filter(lft__gt=qs.lft, rgt__lt=qs.rgt).order_by('lft')
        ques[qs] = qt
    ques_dict = {    
        'ques':ques,
        'q':q,
        }
    return render_to_response('question/view_questions.html', ques_dict, context_instance=RequestContext(request))


def delete_question(request, question_id):
    try:
        question = Question.objects.get(id = question_id)
    except Question.DoesNotExist:
        raise Http404
    qch = question.get_all_children()
    html = 'question/question_delete_confirm.html'
    if request.method == "POST":
        del_confirm = request.POST.get('del_confirm', 'No')
        if del_confirm == "Yes":
            question.delete()
            for q in qch:
                if q.question:
                    q.question.delete()
                q.delete()
        return HttpResponseRedirect('/question/view/')
        
    del_question_dict = {
        'question':question,
        'question_id': question_id,
        'dependent_questions': qch
        }    
    return render_to_response(html, del_question_dict, context_instance=RequestContext(request))

def add_question(request, id=None):
    form = QuestionForm()
    field_inline_formset = inlineformset_factory(Question, Field, form = FieldForm, extra=1, can_delete=True)
    field_formset = field_inline_formset(instance=None)
    option_inline_formset = inlineformset_factory(Question, Option, form = OptionForm, extra=1, fk_name="question", can_delete=True)
    option_formset = option_inline_formset(instance=None)
    is_popup = 0
    errors = []
    if request.method == "POST":
        if 'save' in request.POST:
            is_popup = int(request.POST.get('is_popup', 0))
            form = QuestionForm(request.POST, request.FILES)
            field_formset = field_inline_formset(request.POST, request.FILES, instance=None)
            option_formset = option_inline_formset(request.POST, request.FILES, instance=None)
            if form.is_valid():
                q = form.save()
                # Assumption: Every question added in popup will be dependent question
                if is_popup != 1:
                    try:
                        qt = QuestionTree.objects.get(question=q, parent_question=None, parent_value=None)
                    except QuestionTree.DoesNotExist:
                        qt = QuestionTree(question=q)
                        qt.save()
                    
            else:
                for er in form.errors:
                    errors.append(form.errors[er])
            if not errors:
                for fld in field_formset:
                    if fld.is_valid() and fld.cleaned_data.get('field_label'):
                        f = Field()
                        f.question = q
                        f.field_label = fld.cleaned_data.get('field_label')
                        f.field_type = fld.cleaned_data.get('field_type')
                        f.field_option = fld.cleaned_data.get('field_option')
                        f.save()
                for op in option_formset:
                    if op.is_valid() and op.cleaned_data.get('option_value'):
                        o = Option()
                        o.question = q
                        o.option_value = op.cleaned_data.get('option_value')
                        o.dependent_question = op.cleaned_data.get('dependent_question')
                        o.save()
                        try:
                            qt = QuestionTree.objects.get(question=o.dependent_question, parent_question=q, parent_value=o.option_value)
                        except QuestionTree.DoesNotExist:
                            qt = QuestionTree(question=o.dependent_question, parent_question=q, parent_value=o.option_value)
                            qt.save()
                if is_popup == 1:
                    return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(q._get_pk_val()), escape(q)))
                else:
                    q.rebuild_nsm()
                    return HttpResponseRedirect('/question/%s' %q.id)
    else:
        is_popup = int(request.GET.get('_popup', 0))
    ctxt = {
        'form': form,
        'option_formset': option_formset,
        'field_formset': field_formset,
        'random_count': randint(1,999), # included for multiple popups of dependent question 
        'is_popup': is_popup,
        'errors': errors,
    }
    return render_to_response('question/add_question.html', ctxt, context_instance=RequestContext(request))


def view_question(request, id):
    q = Question.objects.get(pk=id)
    q_fields = q.field_set.all().order_by('id')
    q_options = q.option_set.all().order_by('id')
    ctxt = {
        'q': q,
        'fields': q_fields,
        'options': q_options,
    }
    return render_to_response('question/question.html', ctxt, context_instance=RequestContext(request))


def preview_question(request, id):
    preview_complete = False
    if request.method == "POST":
        qid = request.POST.get('current_question_id', id)
        qval = request.POST.get('current_question_val')
        q = Question.objects.get(pk=qid)
        try:
            q_tree = QuestionTree.objects.select_related('question').get(parent_question__id=qid, parent_value=qval)
            q = q_tree.question or q_tree.parent_question 
        except QuestionTree.DoesNotExist:
            preview_complete = True
    else:
        q = Question.objects.get(pk=id)
    q_fields = q.field_set.all().order_by('id')
    q_options = q.option_set.all().order_by('id')
    q_hierarchy = q.get_question_hierarchy()
    ctxt = {
        'q': q,
        'fields': q_fields,
        'options': q_options,
        'hierarchy': q_hierarchy,
        'preview_complete': preview_complete,
    }
    return render_to_response('question/preview_question.html', ctxt, context_instance=RequestContext(request))


def edit_question(request, id):
    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        raise Http404
    form = QuestionForm(instance = question)
    fieldinlineformset = inlineformset_factory(Question, Field, form = FieldForm, extra=1, can_delete=True)
    optioninlineformset = inlineformset_factory(Question, Option, form = OptionForm, extra=1, fk_name="question", can_delete=True)

    field_formset = fieldinlineformset(instance = question)
    option_formset = optioninlineformset(instance = question)

    is_popup, errors = 0, []
    if request.method == "POST":
        is_popup = int(request.POST.get('is_popup', 0))
        form = QuestionForm(request.POST, request.FILES, instance = question)
        field_formset = fieldinlineformset(request.POST, request.FILES, instance = question)
        option_formset = optioninlineformset(request.POST, request.FILES, instance = question)

        if form.is_valid():
            qch = question.get_all_children()
            for qs in qch:
                qs.delete()
            q = form.save()
        else:
            for er in form.errors:
                errors.append(form.errors[er])
        if not errors:
            Option.objects.filter(question=question).delete()
            Field.objects.filter(question=question).delete()
            for fld in field_formset:
                if fld.is_valid() and fld.cleaned_data.get('field_label'):
                    f = Field()
                    f.question = q
                    f.field_label = fld.cleaned_data.get('field_label')
                    f.field_type = fld.cleaned_data.get('field_type')
                    f.field_option = fld.cleaned_data.get('field_option')
                    f.save()
            for op in option_formset:
                if op.is_valid() and op.cleaned_data.get('option_value'):
                    o = Option()
                    o.question = q
                    o.option_value = op.cleaned_data.get('option_value')
                    o.dependent_question = op.cleaned_data.get('dependent_question')
                    o.save()
                    try:
                        qt = QuestionTree.objects.get(question=o.dependent_question, parent_question=q, parent_value=o.option_value)
                    except QuestionTree.DoesNotExist:
                        qt = QuestionTree(question=o.dependent_question, parent_question=q, parent_value=o.option_value)
                        qt.save()
            if is_popup == 1:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(q._get_pk_val()), escape(q)))
            else:
                if question.is_root_question():
                    root_question = question
                else:
                    root_question = question.get_root_question()
                root_question.rebuild_nsm()
                return HttpResponseRedirect('/question/%s' %q.id)

    is_popup = int(request.GET.get('_popup', 0))
    ctxt = {
        'question': question,
        'form': form,
        'field_formset': field_formset,
        'option_formset': option_formset,
        'random_count': randint(1,999), # included for multiple popups of dependent question 
        'is_popup': is_popup,
        'errors': errors
    }
    return render_to_response('question/edit_question.html', ctxt, context_instance=RequestContext(request))
