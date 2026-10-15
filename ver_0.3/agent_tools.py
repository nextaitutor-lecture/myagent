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
  
def search_transport(trip_date, meeting_time):
  """
  출장 날짜를 기준으로 KTX 좌석을 검색합니다.
  
  실습에서 실패 상황을 재현하기 위해
  KTX 매진 결과를 고정으로 반환합니다.
  
  Args:
    trip_date (str): 출장 날짜 (YYYY-MM-DD)
    meeting_time (str) : 회의 시간
    
  Returns:
    dict: 
  """
  
  return {
    "transport_status": "sold_out",
    "transport_message":
      '2026-10-08 부산행 KTX 좌석이 매진되었습니다.',
  }
