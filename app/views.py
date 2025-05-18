from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import subprocess
import tempfile
import os
import threading
from django.shortcuts import render


def home(request):
    return render(request , 'app/index.html')
@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        import json
        body = json.loads(request.body)
        code = body.get('code', '')
        stdin = body.get('input', '')

        try:
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w', encoding='utf-8') as temp:
                temp.write(code)
                temp_path = temp.name  # store path before closing

            # Now run the file after it's closed
            result = subprocess.run(
                ['python', temp_path],
                input=stdin.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )

            os.unlink(temp_path)  # cleanup

            output = result.stdout.decode() + result.stderr.decode()
        except subprocess.TimeoutExpired:
            output = "Error: Execution timed out."
        except Exception as e:
            output = f"Error: {str(e)}"

        return JsonResponse({'output': output})
