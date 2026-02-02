import pandas as pd
import tempfile

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Dataset
from .serializers import DatasetSerializer
from django.http import JsonResponse
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

import matplotlib.pyplot as plt
import io




#history api    
@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def history(request):
    datasets = Dataset.objects.order_by("-uploaded_at")[:5]
    serializer = DatasetSerializer(datasets, many=True)
    return Response(serializer.data)

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
    # keep only last 5
    qs = Dataset.objects.order_by("-uploaded_at")
    if qs.count() > 5:
     for old in qs[5:]:
        old.delete()

    return Response(summary)

#get dataset by id 
def dataset_detail(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        return JsonResponse({
            "id": dataset.id,
            "uploaded_at": dataset.uploaded_at,
            "summary": dataset.summary
        })
    except Dataset.DoesNotExist:
        return JsonResponse({"error": "Dataset not found"}, status=404)


# PDF GENERATION API 

@api_view(['GET'])
@permission_classes([AllowAny])
def generate_pdf(request):
    dataset = Dataset.objects.last()
    summary = dataset.summary

    # Create PDF response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=equipment_report.pdf"

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Chemical Equipment Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Summary text
    elements.append(Paragraph(f"Total Equipment: {summary['total_equipment']}", styles["Normal"]))
    elements.append(Paragraph(f"Average Flowrate: {summary['avg_flowrate']}", styles["Normal"]))
    elements.append(Paragraph(f"Average Pressure: {summary['avg_pressure']}", styles["Normal"]))
    elements.append(Paragraph(f"Average Temperature: {summary['avg_temperature']}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # ===== Generate Chart using Matplotlib =====
    types = list(summary["type_distribution"].keys())
    counts = list(summary["type_distribution"].values())

    plt.figure(figsize=(6, 4))
    plt.bar(types, counts)
    plt.title("Equipment Type Distribution")
    plt.xlabel("Equipment Type")
    plt.ylabel("Count")
    plt.tight_layout()

    # Save chart to memory buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close()
    img_buffer.seek(0)

    # Add image to PDF
    elements.append(Paragraph("Equipment Distribution Chart", styles["Heading2"]))
    elements.append(Spacer(1, 10))
    elements.append(Image(img_buffer, width=5 * inch, height=3 * inch))

    # Build PDF
    doc.build(elements)
    return response


#FOR PROTECTED

