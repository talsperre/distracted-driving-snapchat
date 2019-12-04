from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
import datetime
from annotation.models import Block, Annotation
from videos.models import Video

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    return HttpResponseRedirect('/snap')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def instructions(request):
    if request.user.is_authenticated:
        return render(request, 'instructions.html')
    return HttpResponseRedirect('/snap')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def understood(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('./')
    return HttpResponseRedirect('/snap')


def update_block():
    now = datetime.datetime.now(datetime.timezone.utc)
    timed_out = [block for block in Block.objects.all()
    if (now - block.start_time).days*86400 + (now - block.start_time).seconds > 60
    ]
    print(timed_out)
    print(Block.objects.all())
    [block.delete() for block in timed_out]


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def sendContent(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/snap')
    update_block()

    block = Block.objects.filter(user = request.user)
    if block.exists():
        return JsonResponse({'videoPath': block.first().video.path, 'numAnnotated': 0})

    # Get all videos which need annotation
    pending = Video.objects.exclude(num_annotations__gte = 3)
    # Get all videos annotated by user
    done_by_user = Video.objects.filter(annotation__user=request.user)
    # Get all videos which need annotation and not annotated by user
    possible_for_user = pending.difference(done_by_user)
    # Get all videos that are blocked
    blocked = Block.objects.all().values('video')
    blocked_vids =  Video.objects.filter(pk__in = blocked)
    # Get all videos which need annotation and not annotated by user and not blocked
    possible_for_user = possible_for_user.difference(blocked_vids)

    try:
        video = possible_for_user.first()
    except:
        return HttpResponse(status=404)
    Block.objects.create(user=request.user, video=video)
    num_annotated = Annotation.objects.filter(user=request.user, skipped=False).count()
    return JsonResponse({'videoPath': '../media/' + video.path, 'numAnnotated': num_annotated})

@csrf_exempt
def submitAnnotation(request):
    marked_labels = request.POST.getlist('labels[]')
    width = request.POST.get('width')
    depth = request.POST.get('depth')

    update_block()

    bitstring = ["0"]*10
    labels = ["outdoors", "indoors", "fashion", "social", "food", "health", "travelling", "religion", "driving", "dangerous"]
    if marked_labels[-1] == "":
        marked_labels = marked_labels[:-1]

    for label in  marked_labels:
        bitstring[labels.index(label)]="1"
    block = Block.objects.filter(user=request.user)
    if not block.exists():
        return HttpResponse(status=406)

    Annotation.objects.create(user=request.user, video=block[0].video, annotation = ''.join(bitstring), width = width, depth = depth)
    video = Video.objects.filter(block__user=request.user).first()
    video.num_annotations = video.num_annotations + 1
    video.save()
    block.delete()
    return HttpResponse(status=200)


@csrf_exempt
def videoSkip(request):
    update_block()

    bitstring = ["0"]*10
    block = Block.objects.filter(user=request.user)
    if not block.exists():
        return HttpResponse(status=406)

    Annotation.objects.create(user=request.user, video=block[0].video, annotation = ''.join(bitstring), width = "", depth = "", skipped=True)
    block.delete()
    return HttpResponse(status=200)
