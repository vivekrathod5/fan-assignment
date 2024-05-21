import json
from .models import Fan, FanLog
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ConsumptionForm
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def fan_simulator(request):
    """
    View function for handling fan simulation requests.

    This view processes POST requests sent from the fan simulator interface to control the fan's status and speed level.

    Returns:
    - JsonResponse: JSON response indicating the success or failure of the fan operation.
    - HttpResponse: Renders the fan simulator interface for GET requests.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            speed_level = data.get('speed_level')
            # Assuming there's only one fan in the database
            fan = Fan.objects.first()

            if action == 1:
                fan.status = True
                if speed_level in range(1, 6):
                    fan.speed_level = speed_level
                fan.save()
                FanLog.objects.create(fan=fan, status=fan.status, speed_level=fan.speed_level)
                return JsonResponse({'status': 'success', 'message': f'Fan turned on to speed {speed_level}'})
            elif action == 0:
                fan.status = False
                fan.speed_level = 0
                fan.save()
                FanLog.objects.create(fan=fan, status=fan.status, speed_level=fan.speed_level)
                return JsonResponse({'status': 'success', 'message': 'Fan turned off'})

            return JsonResponse({'status': 'error', 'message': 'Invalid action'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    else:
        return render(request, 'simulator.html')


def consumption_interface(request):
    """
    View function for rendering the consumption interface and handling consumption data requests.

    This view renders the consumption interface for GET requests and calculates power and energy consumption
    based on user input for POST requests.

    Returns:
    - HttpResponse: Renders the consumption interface.
    - JsonResponse: JSON response containing power and energy consumption data.
    """
    if request.method == 'POST':
        form = ConsumptionForm(request.POST)
        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            
            total_power_consumption, total_energy_consumption = calculate_consumption(start_time, end_time)
            return render(request, 'consumption_results.html', {
                'form': form,
                'total_power_consumption': total_power_consumption,
                'total_energy_consumption': total_energy_consumption
            })
    else:
        form = ConsumptionForm()
    return render(request, 'consumption_interface.html', {'form': form})


def calculate_consumption(start_time, end_time):
    """
    Calculate total power and energy consumption between the specified start and end times.

    Parameters:
    - start_time (datetime): The start time for the calculation.
    - end_time (datetime): The end time for the calculation.

    Returns:
    - Tuple[float, float]: A tuple containing the total power consumption (in kW) and total energy consumption (in kWh).
    """
    start_time = make_aware(start_time)
    end_time = make_aware(end_time)
    fan_logs = FanLog.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time)

    total_power_consumption = 0
    total_energy_consumption = 0

    for log in fan_logs:
        power_consumptions = {1: 0.63, 2: 0.69, 3: 0.74, 4: 0.89, 5: 0.97}
        power_consumption = power_consumptions.get(log.speed_level, 0) * log.fan.voltage * log.fan.power_factor / 1000  # Converted to kW
        total_power_consumption += power_consumption

        if log.status:
            time_difference = (log.timestamp - start_time).total_seconds() / 3600  # Converted to hours
            energy_consumption = power_consumption * time_difference
            total_energy_consumption += energy_consumption

    return total_power_consumption, total_energy_consumption


def consumption_data(request):
    """
    View function for fetching power and energy consumption data via API.

    This view handles GET requests containing start and end times and returns JSON response
    containing power and energy consumption data within the specified time range.

    Returns:
    - JsonResponse: JSON response containing power and energy consumption data.
    """
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    try:
        start_time = timezone.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        end_time = timezone.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DDTHH:MM:SS'})

    total_power_consumption, total_energy_consumption = calculate_consumption(start_time, end_time)

    return JsonResponse({
        'total_power_consumption': total_power_consumption,
        'total_energy_consumption': total_energy_consumption
    })