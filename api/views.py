from ast import If
from datetime import datetime
from django.db.models import Count, Q
from sqlite3 import Date
from xmlrpc.client import DateTime
from django.http import response
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .serializer import CandidateSerializer, PollSerializer, ElectionSerializer
from votingBackend.settings import REST_FRAMEWORK
from .models import Candidate, Poll, Election, Vote
from user.models import User
import json
from django.core.exceptions import ObjectDoesNotExist

@api_view(["POST"])
def add_candidate(request):
    payload = json.loads(request.body)
    try:
        Candidate.objects.create(
            user=User.objects.get(id=payload['userId']),
            election=Election.objects.get(id=payload["electionId"]),
            creation_date = datetime.now()
        )
        return JsonResponse({'message': 'Candidate Created Successfully'}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong '}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_candidates(request):
    paginator = PageNumberPagination()
    paginator.page_size = REST_FRAMEWORK['PAGINATE_BY']
    candidates = Candidate.objects.get_queryset().order_by('id')

    result_page = paginator.paginate_queryset(candidates, request)

    serializer = CandidateSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
def get_candidates_by_election(request, election_id):
    paginator = PageNumberPagination()
    paginator.page_size = REST_FRAMEWORK['PAGINATE_BY']
    candidates = Candidate.objects.filter(election=election_id).order_by('id')
    result_page = paginator.paginate_queryset(candidates, request)
    serializer = CandidateSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["PUT"])
def update_candidate(request, candidate_id):
    payload = json.loads(request.body)
    try:
        candidate_item = Candidate.objects.filter(id=candidate_id)
        # returns 1 or 0
        candidate_item.update(**payload)
        candidate = Candidate.objects.get(id=candidate_id)
        serializer = CandidateSerializer(candidate)
        return JsonResponse({'candidate': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
def delete_candidate(request, candidate_id):
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        candidate.delete()
        return response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def add_poll(request):
    payload = json.loads(request.body)
    try:
        Poll.objects.create(
            poll_name=payload["poll_name"],
            dateCreated=payload["dateCreated"],
            status=payload["status"],
            created_by=User.objects.get(id=payload['user']),
        )
        return JsonResponse({'message': 'Poll Created Successfully'}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def get_polls(request):
    paginator = PageNumberPagination()
    paginator.page_size = REST_FRAMEWORK['PAGINATE_BY']
    polls = Poll.objects.get_queryset().order_by('id')

    result_page = paginator.paginate_queryset(polls, request)

    serializer = PollSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["PUT"])
def update_poll(request, poll_id):
    payload = json.loads(request.body)
    try:
        poll_item = Poll.objects.filter(id=poll_id)
        # returns 1 or 0
        poll_item.update(**payload)
        poll = Poll.objects.get(id=poll_id)
        serializer = PollSerializer(poll)
        return JsonResponse({'poll': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
def delete_poll(request, poll_id):
    try:
        poll = Candidate.objects.get(id=poll_id)
        poll.delete()
        return response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def add_election(request):
    payload = json.loads(request.body)
    try:
        Election.objects.create(
            election_name=payload["election_name"],
            start_date=payload["start_date"],
            end_date=payload["end_date"],
            created_by=User.objects.get(id=payload['user']),
        )
        return JsonResponse({'message': 'Election Created Successfully'}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def get_elections(request):
    paginator = PageNumberPagination()
    paginator.page_size = REST_FRAMEWORK['PAGINATE_BY']
    elections = Election.objects.get_queryset().order_by('id')

    result_page = paginator.paginate_queryset(elections, request)

    serializer = ElectionSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
def get_elections_by_id(request, election_id):
    paginator = PageNumberPagination()
    paginator.page_size = REST_FRAMEWORK['PAGINATE_BY']
    elections = Election.objects.filter(id=election_id).order_by('id')

    result_page = paginator.paginate_queryset(elections, request)

    serializer = ElectionSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(["DELETE"])
def delete_election(request, election_id):
    try:
        election = Election.objects.get(id=election_id)
        election.delete()
        return response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def vote(request):
    payload = json.loads(request.body)
    try:
        voteExist = Vote.objects.filter(user=payload['userId'])
        # print(voteExist)
        if(voteExist):
            return JsonResponse({'message': 'You Have Already Voted'}, safe=False, status=status.HTTP_302_FOUND)
        else:
            Vote.objects.create(
                vote_date= datetime.now(),
                candidate=Candidate.objects.get(id=payload['candidateId']),
                poll=Poll.objects.get(id=payload['pollId']),
                election=Election.objects.get(id=payload['electionId']),
                user=User.objects.get(id=payload['userId']),
            )
            return JsonResponse({'message': 'Your Vote Was Collated Successfully'}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def get_votes(request, election_id):
    paginator = PageNumberPagination()
    paginator.page_size = REST_FRAMEWORK['PAGINATE_BY']
    votes = Vote.objects.values("election", "poll","candidate").annotate(count=Count('candidate', filter=Q(election_id=election_id))).order_by('-count')

    result_page = paginator.paginate_queryset(votes, request)


    return paginator.get_paginated_response(result_page)
