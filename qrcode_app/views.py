from django.shortcuts import render, redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import qrcode
from io import BytesIO
import base64

def generate_qr_code(request):
    qr_code_base64 = None
    error_message = None
    validator = URLValidator()  
    
    
    if request.method == 'POST':
        url = request.POST.get('url')
        
        if not url:
            error_message = "Insira uma URL para gerar o QR Code."
        else:
            try:
                validator = URLValidator()
                validator(url)
                img = qrcode.make(url)
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                qr_code_base64 = f"data:image/png;base64,{img_str}"
                buffer.close()
                error_message
            except ValidationError:
                error_message = "URL inválida. Por favor, insira uma URL válida."
    

    return render(request, 'qrcode_app/index.html', {'qr_code_base64': qr_code_base64,'error_message': error_message})