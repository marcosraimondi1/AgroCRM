from .forms import landForm, billingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
import json

from .models import User, Land, TenantProfile, Billing, Message

import environ  # for making environmental variables

env = environ.Env()
environ.Env.read_env()
API_KEY = env('API_KEY')

# MAIN VIEWS _____________________________________________________________________


def index(request):

    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)

        lands = []

        # get lands to display
        if user.is_landlord:
            lands = user.lands.all().order_by('id')
        else:
            profile = user.profile
            lands = profile.lands.all().order_by('id')

        # create paginator for viewing lands (max 9 lands per page)
        paginator = Paginator(lands, 9)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "crm/index.html", {
            "user": user,
            "lands": page_obj,
            "API_KEY": API_KEY
        })

    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def billing_view(request):
    """
    Display list of all user's bills ordered by their deadline.
    """
    # first get user's lands to get to their billings
    user = User.objects.get(pk=request.user.id)

    if user.is_landlord:
        lands = user.lands.all()
    else:
        profile = user.profile
        lands = profile.lands.all()

    bills = []
    for land in lands:
        bills.append(land.billing)

    # sort by expiration date, first the ones that expire first
    def myKey(b):
        return b.daysleft()

    bills.sort(key=myKey)

    return(render(request, 'crm/bills.html', {
        "user": user,
        "bills": bills,
    }))


@login_required
@ensure_csrf_cookie
def newLand(request):

    landlord = User.objects.get(pk=request.user.id)

    # make sure the user is allowed to create new lands
    if landlord.is_landlord:
        if request.method == 'GET':
            # create new Land instance to populate the form
            land = Land(landlord=landlord)

            # create new forms to display
            land_form = landForm(instance=land)
            billing_form = billingForm()
            return(render(request, 'crm/newLand.html', {
                "land_form": land_form,
                "billing_form": billing_form
            }))
        elif request.method == 'POST':
            if request.POST.get("editing"):

                # update existing land and billing
                land = Land.objects.get(pk=request.POST["land_id"])
                billing = Billing.objects.get(pk=request.POST["billing_id"])

                # get forms to update instances
                land_form = landForm(
                    request.POST, request.FILES, instance=land)

                billing_form = billingForm(request.POST, instance=billing)

                # validate and save
                if land_form.is_valid() and billing_form.is_valid():
                    land_form.save()
                    billing_form.save()
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return(render(request, 'crm/newLand.html', {
                        "land_form": land_form,
                        "billing_form": billing_form,
                        "land": land,
                        "billing": billing,
                        "editing": True
                    }))

            else:
                # get form for new land
                land_form = landForm(request.POST, request.FILES)
                billing_form = billingForm(request.POST)

                # validate and save
                if land_form.is_valid() and billing_form.is_valid():
                    # validate forms and save new objects
                    land = land_form.save(commit=False)
                    land.landlord = landlord
                    land.save()

                    billing = billing_form.save(commit=False)
                    billing.land = land
                    billing.save()

                    return HttpResponseRedirect(reverse("index"))
                else:
                    return(render(request, 'crm/newLand.html', {
                        "land_form": land_form,
                        "billing_form": billing_form
                    }))
        else:
            return(HttpResponse("error: Bad request.", status=400))
    else:
        return(HttpResponse("error: Invalid credentials.", status=401))


@login_required
def editLand(request, land_id):

    # get respective data
    landlord = User.objects.get(pk=request.user.id)
    land = landlord.lands.filter(pk=land_id).first()
    billing = land.billing

    # make sure the user is allowed to edit this land
    if landlord.is_landlord and land:
        if request.method == 'GET':

            # create forms from existing model objects
            land_form = landForm(instance=land)
            billing_form = billingForm(instance=billing)

            return(render(request, 'crm/newLand.html', {
                "land_form": land_form,
                "billing_form": billing_form,
                "land": land,
                "billing": billing,
                "editing": True
            }))
        else:
            return(HttpResponse("error: Bad request.", status=400))
    else:
        return(HttpResponse("error: Invalid credentials.", status=401))


@login_required
@ensure_csrf_cookie
def profile(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'GET':
        partners = []
        if user.is_landlord:
            partners = user.tenants.all()
        else:
            partners = user.profile.landlords.all()

        messages = user.received_messages.filter(
            is_request=False).all().order_by('-timestamp')

        requests = user.received_messages.filter(
            is_request=True).all().order_by('-timestamp')

        return(render(request, 'crm/profile.html', {
            "user": user,
            "partners": partners,
            "messages": messages,
            "requests": requests
        }))

    elif request.method == 'PUT':
        # accepting request -> create relation
        data = json.loads(request.body)
        message = Message.objects.get(pk=data["message_id"])

        if data.get("deleting"):
            # if deleting request -> delete
            message.delete()
            return JsonResponse({"message": "deleted successfully."}, status=200)

        # receiver == current user
        receiver = message.receiver

        if receiver.id != request.user.id:
            return(JsonResponse({"error": "Invalid credentials."}, status=401))

        # sender == other user
        sender = message.sender

        try:
            if receiver.is_landlord:
                sender.profile.landlords.add(receiver)
            else:
                receiver.profile.landlords.add(sender)

        except Exception as ex:
            print(ex)
            return(JsonResponse({"error": "Invalid credentials."}, status=401))

        # delete request
        message.delete()
        return JsonResponse({"message": "relation created!"}, status=200)
    else:
        return(HttpResponse("error: Bad request.", status=400))

# API ROUTES ______________________________________________________________


@login_required
def land(request, land_id):
    if request.method == 'GET':
        try:
            # get land object
            land = Land.objects.get(pk=land_id)
        except Exception as ex:
            print(ex)
            return JsonResponse({"error": f"Land with id {land_id} not found"}, status=404)
        # get land data
        data = land.serialize()
        return JsonResponse(data)

    elif request.method == 'PUT':
        # receive information
        data = json.loads(request.body)

        # check user is allowed to edit this land
        user = User.objects.get(pk=request.user.id)
        land = Land.objects.get(pk=data["land_id"])

        if user.is_landlord and land in user.lands.all():
            try:
                data["deleting"]
                land.delete()
                return JsonResponse({"message": "deleted successfully"}, status=204)
            except Exception as ex:
                print(ex)
                return JsonResponse({"message": "error"}, status=500)
        else:
            return(JsonResponse({"error": "Invalid credentials."}, status=401))
    else:
        return render(request, "crm/login.html")


@login_required
def messages(request):
    """
    Post new messages
    """

    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)

        # get post data
        content = request.POST["message"]
        receiver_id = request.POST["receiver"]

        is_request = False
        if request.POST.get("adduser"):
            is_request = True

        try:
            # check that receiver is an already associated user if it is not a request
            # if it is a request the receiver shouldn't be already associated
            # only messages btwn landlords and tenants

            receiver = User.objects.get(pk=receiver_id)

            if user.is_landlord:
                if is_request:
                    if receiver.profile in user.tenants.all() or receiver.is_landlord:
                        raise Exception
                else:
                    if receiver.profile not in user.tenants.all() or receiver.is_landlord:
                        raise Exception

            else:
                if is_request:
                    if receiver in user.profile.landlords.all() or not receiver.is_landlord:
                        raise Exception
                else:
                    if receiver not in user.profile.landlords.all() or not receiver.is_landlord:
                        raise Exception

        except:
            return(JsonResponse({"error": "Receiver user not found or invalid credentials."}, status=401))

        # create new message
        message = Message(message=content, receiver=receiver,
                          sender=user, is_request=is_request)
        message.save()

        return HttpResponseRedirect(reverse('profile'))

    else:
        return(JsonResponse({"error": "Bad request."}, status=401))


# LOGIN VIEWS _____________________________________________________________________

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "crm/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "crm/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        print(request.POST)
        try:
            request.POST["islandlord"]
            is_landlord = True
        except:
            is_landlord = False

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "crm/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, is_landlord=is_landlord)
            user.save()

            if not user.is_landlord:
                # create tenant profile
                # note: for landlord attr, tenant should be supplied with a token or
                # a key that links him to a specific landlord
                profile = TenantProfile(tenant=user)
                profile.save()

        except IntegrityError as e:
            print(e)
            return render(request, "crm/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "crm/register.html")
