
from django.db import IntegrityError
from .models import Vote
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
# from django.http import HttpResponse
import random
from .models import Member,Secretary, Categoryname,Issue,Solutions


def calculate_approval_percent(solution):
    total_votes = solution.approve_count + solution.reject_count
    if total_votes > 0:
        percent = (solution.approve_count / total_votes) * 100
        return min(int(percent), 100)  # Cap at 100% to prevent any overflow
    return 0


# -------------------------
# MEMBER SIGNUP
# -------------------------
def MemberSignup(request):
    if request.method == 'POST':
        memberName = request.POST.get('membername', '').strip()
        memberContact = request.POST.get('membercontact', '').strip()
        memberEmail = request.POST.get('memberemail', '').strip()
        memberPassword = request.POST.get('memberpass', '')
        memberCpassword = request.POST.get('membercpass', '')
        memberAddress = request.POST.get('flatnumber', '').strip()
        memberType = request.POST.get('residentType', '').strip()

        if not all([memberName, memberContact, memberEmail, memberPassword, memberCpassword, memberAddress, memberType]):
            return render(request, 'membersignup.html', {'err1': 'All fields are required'})

        if memberPassword != memberCpassword:
            return render(request, 'membersignup.html', {'err2': 'Passwords do not match'})

        if Member.objects.filter(memberMail=memberEmail).exists():
            return render(request, 'membersignup.html', {'err3': 'Email already registered'})

        if len(memberContact) != 10:
            return render(request, 'membersignup.html', {'err5': 'Phone number must be exactly 10 digits'})

        if Member.objects.filter(memberContact=memberContact).exists():
            return render(request, 'membersignup.html', {'err4': 'Number already exists'})
       
        

     


        otp = str(random.randint(1000, 9999))

        request.session['signup_data'] = {
            'name': memberName,
            'email': memberEmail,
            'password': make_password(memberPassword),
            'contact': memberContact,
            'address': memberAddress,
            'membertype': memberType,
        }

        request.session['otp'] = otp
        request.session.set_expiry(300)  # OTP valid for 5 minutes

        send_mail(
            subject='Your OTP Verification',
            message=f'Your OTP is: {otp}',
            from_email='rahulsinghrawat1667@gmail.com',
            recipient_list=[memberEmail],
            fail_silently=False
        )

        return redirect('verifymember')

    return render(request, 'membersignup.html')


# -------------------------
# OTP VERIFICATION
# -------------------------
def verifymember(request):
    if request.method == 'POST':
        user_otp = request.POST.get('motp', '').strip()
        actual_otp = request.session.get('otp')
        data = request.session.get('signup_data')

        if not data or not actual_otp:
            return render(request, 'verifymember.html', {'err': 'Session expired. Please sign up again.'})

        if user_otp != actual_otp:
            return render(request, 'verifymember.html', {'err': 'Invalid OTP'})
        
        

        Member.objects.create(
            memberName=data['name'],
            memberMail=data['email'],
            memberPassword=data['password'],
            memberContact=data['contact'],
            memberAddress=data['address'],
            memberType=data['membertype']
        )

        del request.session['otp']
        del request.session['signup_data']

        return redirect('memberlogin')

    return render(request, 'verifymember.html')


# -------------------------
# MEMBER LOGIN
# -------------------------
def memberlogin(request):
    


    if request.method == 'POST':
        email = request.POST.get('loginmail', '').strip()
        password = request.POST.get('loginpassword', '')

        try:
            member = Member.objects.get(memberMail=email)
        except Member.DoesNotExist:
            return render(request, 'memberlogin.html', {'err': 'Invalid email or password'})

        if not check_password(password, member.memberPassword):
            return render(request, 'memberlogin.html', {'err': 'Invalid email or password'})

        request.session['member_id'] = member.id
        request.session['member_name'] = member.memberName
        return redirect('admindashboard')

    return render(request, 'memberlogin.html')


# -------------------------
# LOGOUT
# -------------------------
def memberlogout(request):
    request.session.flush()
    return redirect('admindashboard')


# -------------------------
# LOGIN REQUIRED DECORATOR
# -------------------------
# def member_login_required(view_func):
#     def wrapper(request, *args, **kwargs):
#         if not request.session.get('member_id'):
#             return redirect('memberlogin')
#         return view_func(request, *args, **kwargs)
#     return wrapper


# -------------------------
# PAGES (PROTECTED)
# -------------------------

def admindashboard(request):

    member_id = request.session.get('member_id')
    # if not member_id:
    #     return redirect('admindashboard')
  
    issue_count = Issue.objects.filter(created_by_id=member_id).count()
  
    issue_details = Issue.objects.filter(created_by_id=member_id)
    
    # Calculate resolved issues count
    resolved_issues_count = 0
    if member_id:
        issues = Issue.objects.filter(created_by_id=member_id)
        for issue in issues:
            solutions = Solutions.objects.filter(Issue_details=issue)
            approved_solutions = [sol for sol in solutions if calculate_approval_percent(sol) >= 60]
            if approved_solutions:
                resolved_issues_count += 1
    
    # Add pending members to vote info
    solutions = Solutions.objects.all().select_related('Issue_details', 'submitted_by')
    all_members = Member.objects.all()
    
    # Calculate total members who haven't voted on any solution
    members_who_voted = Vote.objects.values_list('member', flat=True).distinct()
    total_pending_voters = all_members.exclude(id__in=members_who_voted).count()
    
    solutions_with_pending = []
    for solution in solutions:
        voted_members = Vote.objects.filter(solution=solution).values_list('member', flat=True)
        pending_members = all_members.exclude(id__in=voted_members)
        solutions_with_pending.append({
            'solution': solution,
            'pending_members': pending_members
        })
    
    return render(request, 'admindashboard.html', {
        "issue_count": issue_count,
        'issue_details': issue_details,
        'solutions_with_pending': solutions_with_pending,
        'total_pending_voters': total_pending_voters,
        'resolved_issues_count': resolved_issues_count
    })



def issuereport(request):
    member_id = request.session.get('member_id')
    # if not member_id:
    #     return redirect('memberlogin')
 
    issues = Issue.objects.filter(created_by_id=member_id)

    return render(request, 'issuereport.html', {'issue': issues})






def addIssue(request):


    categories = Categoryname.objects.all()

    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('memberlogin')

    member = Member.objects.get(id=member_id)

    if request.method == 'POST':
        issue_title = request.POST.get('title', '')
        issue_description = request.POST.get('description', '')
        issue_category_id = request.POST.get('category', '')
        issue_block = request.POST.get('block', '')
        issue_floor_str = request.POST.get('floor', '')
        issue_flat = request.POST.get('flat_number', '')
        issue_img = request.FILES.get('attachment')

        category = Categoryname.objects.get(id=issue_category_id)
        issue_floor = int(issue_floor_str) if issue_floor_str else 0

        Issue.objects.create(
            title=issue_title,
            description=issue_description,
            location_type='Residential',
            category=category,
            block=issue_block,
            attachment=issue_img,
            floor=issue_floor,
            flat_number=issue_flat,
            created_by=member
        )

        return redirect('issuereport')

    return render(request, 'addissue.html', {'Category_name': categories})

def notification(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('memberlogin')

    
    # Issues created by others (existing)
    notify_issues = Issue.objects.exclude(created_by_id=member_id)
    
    # Solutions to user's issues that are not yet approved
    user_issues = Issue.objects.filter(created_by_id=member_id)
    pending_solutions = Solutions.objects.filter(Issue_details__in=user_issues, is_approved=False).select_related('Issue_details', 'submitted_by')

    return render(request, 'notification.html', {
        'notify_issues': notify_issues,
        'pending_solutions': pending_solutions
    })


def approve_solution(request, solution_id):
    member_id = request.session.get('member_id')
    if not member_id:   
        return redirect('memberlogin')

    try:
        solution = Solutions.objects.get(id=solution_id, Issue_details__created_by_id=member_id, is_approved=False)
        solution.is_approved = True
        solution.save()
    except Solutions.DoesNotExist:
        pass  # Maybe add error message

    return redirect('notification')





def secretary_login(request):
    if request.session.get('secretary_id'):
        return redirect('secretarydashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        try:
            secretary = Secretary.objects.get(email=email, is_active=True)
        except Secretary.DoesNotExist:
            return render(request, 'secretarylogin.html', {'err': 'Invalid credentials'})

        if not secretary.check_password(password):
            return render(request, 'secretarylogin.html', {'err': 'Invalid credentials'})

        # Generate OTP
        otp = str(random.randint(1000, 9999))

        request.session['secretary_otp'] = otp
        request.session['secretary_temp_id'] = secretary.id
    

        send_mail(
            subject='Secretary OTP Verification',
            message=f'Your OTP is: {otp}',
            from_email='admin@residential.com',
            recipient_list=[secretary.email],
            fail_silently=False
        )

        return redirect('secretaryotp')

    return render(request, 'secretarylogin.html')

def secretary_otp_verify(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp', '').strip()
        actual_otp = request.session.get('secretary_otp')
        secretary_id = request.session.get('secretary_temp_id')

        if not actual_otp or not secretary_id:
            return render(request, 'secretaryotp.html', {
                'err': 'Session expired. Please login again.'
            })

        if user_otp != actual_otp:
            return render(request, 'secretaryotp.html', {
                'err': 'Invalid OTP'
            })

   
        request.session['secretary_id'] = secretary_id

       
        del request.session['secretary_otp']
        del request.session['secretary_temp_id']

        return redirect('secretarydashboard')

    return render(request, 'secretaryotp.html')

def secretarydashboard(request):
    return render(request, 'secretarydashboard.html')


def issue_solution(request, issue_id):
    
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('memberlogin')

    member = Member.objects.get(id=member_id)
    issue = Issue.objects.get(id=issue_id)

    # Check if user has already submitted a solution for this issue
    existing_solution = Solutions.objects.filter(Issue_details=issue, submitted_by=member).exists()

    if request.method=='POST':
        if existing_solution:
            return render(request, 'solution.html', {
                'issue': issue,
                'already_submitted': True,
                'mess': 'You have already submitted a solution for this issue.'
            })

        sol_issue_title = request.POST.get('title', '')
        sol_issue_description = request.POST.get('description', '')

        Solutions.objects.create(
            Issue_details=issue,
            submitted_by=member,
            title=sol_issue_title,
            Description=sol_issue_description,
        )

        return redirect('admindashboard')

    return render(request, 'solution.html', {
        'issue': issue,
        'already_submitted': existing_solution,
        'solutions':Solutions,

    })




def voting(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('memberlogin')

    member = Member.objects.get(id=member_id)

    selected_user_id = request.session.get('selected_user')

    if request.method == 'POST':
        if 'select_user' in request.POST:
            selected_user_id = request.POST.get('selected_user_id')
            request.session['selected_user'] = selected_user_id
            return redirect('voting')
        
        solution_id = request.POST.get('solution_id')
        vote_type = request.POST.get('vote')

        solution = Solutions.objects.get(id=solution_id)

       
        already_voted = Vote.objects.filter(
            solution=solution,
            member=member
        ).exists()

        if not already_voted:
            Vote.objects.create(
                solution=solution,
                member=member,
                is_approved=(vote_type == 'approve')
            )

            if vote_type == 'approve':
                solution.approve_count += 1
            else:
                solution.reject_count += 1

            solution.save()

        return redirect('voting')

    if not selected_user_id:
        # Show user selection page
        other_members = Member.objects.exclude(id=member_id)
        return render(request, 'votting.html', {
            'select_user': True,
            'other_members': other_members
        })

    # Voting page
    suggestions = Solutions.objects.filter(submitted_by_id=selected_user_id, is_approved=True).select_related('Issue_details', 'submitted_by')
    all_members = Member.objects.all()

    voted_solutions = Vote.objects.filter(
        member=member
    ).values_list('solution_id', flat=True)

    # Add pending voter info for each solution
    suggestions_with_pending = []
    for suggestion in suggestions:
        voted_members = Vote.objects.filter(solution=suggestion).values_list('member', flat=True)
        pending_members = all_members.exclude(id__in=voted_members)
        pending_count = pending_members.count()
        suggestions_with_pending.append({
            'solution': suggestion,
            'pending_count': pending_count,
            'has_voted': suggestion.id in voted_solutions
        })

    selected_user = Member.objects.get(id=selected_user_id)
    return render(request, 'votting.html', {
        'suggestions': suggestions_with_pending,
        'selected_user': selected_user,
        'message' : 'your vote has been submitted'
    })


def clear_selected_user(request):
    if request.method == 'POST':
        request.session.pop('selected_user', None)
    return redirect('voting')


def view_solutions(request):
    member_id = request.session.get('member_id')

    if not member_id:
        return redirect('admindashboard')  # Assuming there's a URL name, or use render(request, 'admindashboard.html')
    
    issue = Issue.objects.filter(created_by_id = member_id)
    solutions = Solutions.objects.filter(Issue_details__in = issue, is_approved=True).select_related('submitted_by', 'Issue_details')
    
    # Filter solutions that have 60% or more approval
    approved_solutions = [sol for sol in solutions if calculate_approval_percent(sol) >= 60]

    # Calculate total votes across all approved solutions
    total_votes = sum(sol.approve_count + sol.reject_count for sol in approved_solutions)

    return render(request, 'submittedsolution.html' , {'issues':issue, "solutions":approved_solutions, "total_votes": total_votes})




    # return render(request , {'member_signup': member_signup})


    


    