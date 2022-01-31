from django.http import HttpResponse
from django.shortcuts import render
from .one_variable_stats import OneVariableStatsQuestion, OneVariableStatsQuestionType
from .probabilities import ProbabilitiesQuestion, ProbabilitiesQuestionType

# Create your views here.
def index(request):
    return HttpResponse('<a href="/probabilities">Probabilities questions...</a> <br/> <a href="/one_variable_stats">One variable stats questions...</a>')

probabilities_context = {
        'question1': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question2': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question3': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question4': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question5': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question6': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
    }

def probabilities(request):
    global probabilities_context
    if request.method == 'POST':
        answers = {
            'answer1': 0 if not request.POST['answer1'] else round(float(request.POST['answer1']), 6),
            'answer2': 0 if not request.POST['answer2'] else round(float(request.POST['answer2']), 6),
            'answer3': 0 if not request.POST['answer3'] else round(float(request.POST['answer3']), 6),
            'answer4': 0 if not request.POST['answer4'] else round(float(request.POST['answer4']), 6),
            'answer5': 0 if not request.POST['answer5'] else round(float(request.POST['answer5']), 6),
            'answer6': 0 if not request.POST['answer6'] else round(float(request.POST['answer6']), 6),
        }
        for i in range(1, len(probabilities_context) + 1):
            answers[f'solution{i}'] = round(float(probabilities_context[f'question{i}'].answer[0]), 6)
        context = {
            'results1': 'Good job!' if answers['answer1'] == answers['solution1'] else 'Better luck next time!',
            'results2': 'Good job!' if answers['answer2'] == answers['solution2'] else 'Better luck next time!',
            'results3': 'Good job!' if answers['answer3'] == answers['solution3'] else 'Better luck next time!',
            'results4': 'Good job!' if answers['answer4'] == answers['solution4'] else 'Better luck next time!',
            'results5': 'Good job!' if answers['answer5'] == answers['solution5'] else 'Better luck next time!',
            'results6': 'Good job!' if answers['answer6'] == answers['solution6'] else 'Better luck next time!',
        }
        context.update(answers)
        context.update(probabilities_context)
        return render(request, 'probabilities_answers.html', context)
    probabilities_context = {
        'question1': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question2': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question3': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question4': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question5': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
        'question6': ProbabilitiesQuestion(ProbabilitiesQuestionType.random_type()),
    }
    return render(request, 'probabilities.html', probabilities_context)

one_variable_stats_context = {
        'question1': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question2': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question3': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question4': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question5': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question6': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
    }

def one_variable_stats(request):
    global one_variable_stats_context
    if request.method == 'POST':
        answers = {
            'answer1': 0 if not request.POST['answer1'] else round(float(request.POST['answer1']), 1),
            'answer2': 0 if not request.POST['answer2'] else round(float(request.POST['answer2']), 1),
            'answer3': 0 if not request.POST['answer3'] else round(float(request.POST['answer3']), 1),
            'answer4': 0 if not request.POST['answer4'] else round(float(request.POST['answer4']), 1),
            'answer5': 0 if not request.POST['answer5'] else round(float(request.POST['answer5']), 1),
            'answer6': 0 if not request.POST['answer6'] else round(float(request.POST['answer6']), 1),
        }
        for i in range(1, len(one_variable_stats_context) + 1):
            answers[f'solution{i}'] = round(float(one_variable_stats_context[f'question{i}'].answer[0]), 1)
        context = {
            'results1': 'Good job!' if answers['answer1'] == answers['solution1'] else 'Better luck next time!',
            'results2': 'Good job!' if answers['answer2'] == answers['solution2'] else 'Better luck next time!',
            'results3': 'Good job!' if answers['answer3'] == answers['solution3'] else 'Better luck next time!',
            'results4': 'Good job!' if answers['answer4'] == answers['solution4'] else 'Better luck next time!',
            'results5': 'Good job!' if answers['answer5'] == answers['solution5'] else 'Better luck next time!',
            'results6': 'Good job!' if answers['answer6'] == answers['solution6'] else 'Better luck next time!',
        }
        context.update(answers)
        context.update(one_variable_stats_context)
        return render(request, 'one_variable_stats_answers.html', context)
    one_variable_stats_context = {
        'question1': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question2': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question3': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question4': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question5': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
        'question6': OneVariableStatsQuestion(OneVariableStatsQuestionType.random_type()),
    }
    return render(request, 'one_variable_stats.html', one_variable_stats_context)