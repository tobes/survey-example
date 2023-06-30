import uuid

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import FormView

from pulse_survey.survey.forms import FeedbackForm
from pulse_survey.survey.models import Result, Feedback

# I like this order
WELLBEING_RESPONSES = [
    "Strongly agree",
    "Agree",
    "Neither agree nor disagree",
    "Disagree",
    "Strongly disagree",
]


def index(request):
    session_id = uuid.uuid4()
    start = request.GET.get("start")
    if start:
        return redirect(reverse("team", args=(session_id,)))
    return render(request=request, template_name="index.html", context={"session_id": session_id})


def team_view(request, session_id):
    errors = {}
    page_number = 1
    result, _ = Result.objects.get_or_create(session_id=session_id, page_number=page_number)
    # I opted to sort the teams when sent to the template rather than just
    # changing this set to a list.
    teams = {"Team A", "Team B", "Team C"}
    chosen_team = None
    if result.data:
        chosen_team = result.data.get("team")
    if request.method == "POST":
        result.data = request.POST
        result.save()
        return redirect(reverse("location", args=(session_id,)))
    return render(request, "team_question.html", {"errors": errors, "teams": sorted(teams), "chosen_team": chosen_team})


def location_view(request, session_id):
    errors = {}
    page_number = 2
    result, _ = Result.objects.get_or_create(session_id=session_id, page_number=page_number)
    # so here is the other option
    locations = ["London", "Manchester", "Glasgow", "York", "Bristol"]
    chosen_location = None
    if result.data:
        chosen_location = result.data.get("location")
    if request.method == "POST":
        result.data = request.POST
        result.save()
        return redirect(reverse("wellbeing-q1", args=(session_id,)))
    return render(request, "location_question.html", {"errors": errors, "locations": locations, "chosen_location": chosen_location})



def wellbeing_q1_view(request, session_id):
    errors = {}
    page_number = 3
    result, _ = Result.objects.get_or_create(session_id=session_id, page_number=page_number)
    answers = WELLBEING_RESPONSES
    chosen_answer = None
    if result.data:
        chosen_answer = result.data.get("q1")
    if request.method == "POST":
        result.data = request.POST
        result.save()
        return redirect(reverse("wellbeing-q2", args=(session_id,)))
    return render(request, "wellbeing_q1.html", {"errors": errors, "answers": answers, "chosen_answer": chosen_answer})


def wellbeing_q2_view(request, session_id):
    errors = {}
    page_number = 4
    result, _ = Result.objects.get_or_create(session_id=session_id, page_number=page_number)
    answers = WELLBEING_RESPONSES
    chosen_answer = None
    if result.data:
        chosen_answer = result.data.get("q2")
    if request.method == "POST":
        result.data = request.POST
        result.save()
        return redirect(reverse("feedback"))
    return render(request, "wellbeing_q2.html", {"errors": errors, "answers": answers, "chosen_answer": chosen_answer})


class FeedbackView(FormView):
    template_name = "feedback.html"
    form_class = FeedbackForm
    success_url = "survey/end/"

    def form_valid(self, form):
        Feedback(email=form.data["email"], content=form.data["content"]).save()
        return redirect("end")
    

def end_view(request):
    return render(request, "end.html")

