from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def chat(request):
    user_query = request.data.get('query', '')
    # Placeholder: call NLP API and return response
    # For now, return a canned response
    return Response({
        'reply': f"This is a placeholder response to: '{user_query}'. We'll integrate an NLP API here.",
        'suggestions': [
            'Track my order',
            'Show popular products',
            'Apply available coupons'
        ]
    })
