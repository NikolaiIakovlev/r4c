import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Robot

from django.utils import timezone
from django.core.exceptions import ValidationError


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            model = data.get('model')
            version = data.get('version')
            created_str = data.get('created')

            #Проверка обязательных полей и формат даты
            if not model or not version or not created_str:
                return HttpResponseBadRequest("Missing required fields.")
            try:
                created = timezone.datetime.fromisoformat(created_str.replace(' ', 'T'))
            except ValueError:
                return HttpResponseBadRequest("Invalid date format.")

            robot = Robot(model=model, version=version, created=created)
            robot.save()  #Валидация происходит в модели Robot.save
            return JsonResponse({'message': 'Robot created successfully.', 'id': robot.id})

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Данные JSON некорректны.")
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))

    else:
        return HttpResponseBadRequest("Метод должен быть POST.")
