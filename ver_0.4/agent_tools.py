"""
파일 : agent_tools.py 
역할 : Agent가 사용할 수 있는 도구 구현
주요 함수 : check_calendar(), search_transport()
"""

def check_calendar():
  """
  출장 날짜와 미팅 시간을 캘린더에서 확인합니다.
  실제 캘린더 API 대신 실습용 고정 데이터를 반환합니다.
  
  Returns:
    dict: 출장 날짜(trip_date)와 미팅 시간(meeting_time)
  """
  
  return {
    "trip_date": "2026-10-08",
    "meeting_time": "14:00",
  }
  
def search_transport(trip_date, meeting_time, transport_type):
  """
  교통수단에 따라 좌석을 검색합니다.
  """
  
  if transport_type == "KTX":    
    return {
      "transport_type": "KTX",
      "transport_status": "sold_out",
      "transport_message": 'KTX 좌석이 매진되었습니다.',
    }
    
  elif transport_type == "BUS":    
    return {
      "transport_type": "BUS",
      "transport_status": "available",
      "transport_message": '버스 좌석이 있습니다.',
    }
    
  else:
    raise ValueError(f"지원하지 않는 교통수단: {transport_type}")
    
