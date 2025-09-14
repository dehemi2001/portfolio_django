from django.shortcuts import render ,redirect
from django.contrib import messages
from .models import Contact, User, Skill, Project

def home(request):
    # Handle Contact Form Submission on POST request
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        content = request.POST.get('content')

        # Basic validation
        if not (1 < len(name) < 30):
            messages.error(request, 'Length of name should be between 2 and 30 characters.')
        elif not (1 < len(email) < 30): # A proper email validator would be better
            messages.error(request, 'Invalid email, please try again.')
        elif not (9 < len(number) < 13):
            messages.error(request, 'Invalid number, please try again.')
        else:
            # If validation passes, save the contact and show a success message
            ins = Contact(name=name, email=email, content=content, number=number)
            ins.save()
            messages.success(request, 'Thank you for contacting me! Your message has been saved.')
            return redirect('home') # Redirect to the same page to prevent form resubmission
        
    # Fetch portfolio data for GET request or after form processing
    # We use .first() assuming you will only have one user entry for your portfolio.
    user_profile = User.objects.first()
    skills = Skill.objects.all() # These are already ordered by the 'order' field
    projects = Project.objects.all() # Also ordered by 'order'

    context = {
        'user': user_profile,
        'skills': skills,
        'projects': projects,
    }
    return render(request, 'home.html', context)
