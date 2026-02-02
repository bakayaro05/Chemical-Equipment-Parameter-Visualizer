import pandas as pd
import tempfile

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from reportlab.pdfgen import canvas
from django.http import FileResponse

from .models import Dataset


#UPLOAD API 

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    df = pd.read_csv(file)

    summary = {
        "total_equipment": len(df),
        "avg_flowrate": float(df["Flowrate"].mean()),
        "avg_pressure": float(df["Pressure"].mean()),
        "avg_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict()
    }

    Dataset.objects.create(summary=summary)

    # Keep only last 5 datasets
    if Dataset.objects.count() > 5:
        Dataset.objects.order_by('uploaded_at').first().delete()

    return Response(summary)


#HISTORY API 
@api_view(['GET'])
@permission_classes([AllowAny])
def history(request):
    data = Dataset.objects.order_by('-uploaded_at').values()
    return Response(data)


# PDF GENERATION API 

@api_view(['GET'])
@permission_classes([AllowAny])
def generate_pdf(request):
    dataset = Dataset.objects.latest('uploaded_at')
    summary = dataset.summary

    tmp = tempfile.NamedTemporaryFile(delete=False)
    c = canvas.Canvas(tmp.name)

    y = 800
    c.drawString(50, y, "Chemical Equipment Summary Report")
    y -= 40

    for key, value in summary.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

    c.save()

    return FileResponse(
        open(tmp.name, 'rb'),
        as_attachment=True,
        filename="equipment_report.pdf"
    )

#FOR PROTECTED

