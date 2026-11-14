"""
파일 : agent_core.py 
역할 : Agent의 판단과 행동 실행 제어
주요 함수 : ask_llm(), execute_action()
"""
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from agent_tools import check_calendar, search_transport

# 환경변수를 먼저 로드합니다.
MODULE_DIR = Path.cwd().resolve()

for directory in (MODULE_DIR, *MODULE_DIR.parents):
    env_path = directory / ".env"
    if env_path.is_file():
        load_dotenv(env_path)
        break  

# 클라이언트를 한 번 생성하고 재사용합니다.
client = OpenAI()        

# LLM에게 전달하는 판단 지침입니다.
DECISION_INSTRUCTIONS = """
당신은 부산 출장 준비를 돕는 AI Agent의 판단 역할입니다.
사용자의 목표, 현재 상태, 실행 이력을 보고 다음 행동 하나를 선택하세요.

[실습 범위]
- 캘린더의 출장 일정을 확인하고 이용 가능한 교통편을 찾습니다.
- 실제 예약이나 결제는 수행하지 않습니다.

[사용 가능한 도구의 역할]
- check_calendar: 출장 날짜와 미팅 시간을 확인합니다.
- search_transport: 출장 일정에 맞춰 KTX 또는 BUS 좌석을 검색합니다.

[판단 지침]
1. 현재 상태와 실행 이력에서 이용 가능한 교통편이 확인되면
   action을 null로 반환하세요.
2. 출장 날짜나 미팅 시간이 없으면
   check_calendar를 선택하세요.
3. 출장 일정이 확인되었고 아직 교통편을 검색하지 않았다면
   search_transport로 KTX를 검색하세요.
4. KTX가 매진되었고 아직 BUS를 검색하지 않았다면
   search_transport로 BUS를 검색하세요.
5. 실행 이력을 확인하고 동일한 조건으로 실패한 검색을 반복하지 마세요.
6. action은 available_actions에 포함된 도구 또는 null만 선택하세요.
   필요한 도구가 없거나 더 이상 진행할 수 없으면 null로 반환하세요.

[실행 인자 작성 규칙]
7. search_transport를 선택하면 arguments를 다음과 같이 작성하세요.
   - trip_date: current_state의 출장 날짜를 그대로 사용하세요.
   - meeting_time: current_state의 미팅 시간을 그대로 사용하세요.
   - transport_type: 판단 지침에 따라 KTX 또는 BUS를 지정하세요.
   - 날짜와 시간은 추측하거나 변경하지 마세요.
8. check_calendar 또는 null을 선택하면 arguments의
   trip_date, meeting_time, transport_type을 모두 null로 작성하세요.

[선택 이유 작성 규칙]
9. reason에는 현재 상태와 실행 이력에 근거한 선택 이유를
   간결하게 작성하세요.
   action이 null이면 교통편을 찾아 종료하는 것인지,
   진행할 수 없어 종료하는 것인지 구분해서 설명하세요.
10. 아직 실행하지 않은 행동을 완료했다고 표현하거나,
    실제 예약이나 결제를 완료했다고 주장하지 마세요.
"""

# JSON 스키마 키워드 설명은 이 파일 하단 참고
def build_decision_schema(available_actions):
  """LLM 이 반환할 판단 결과의 항목과 자료형을 정의합니다.    
  
  이 스키마에 맞춰 LLM이 반환할 수 있는 응답 예시 :
  {
    "action": "search_transport",
    "arguments": {
        "trip_date": "2026-11-20",
        "meeting_time": "14:00",
        "transport_type": "KTX"
    },
    "reason": "출장 일정이 확인되어 KTX 교통편을 검색합니다."
  }
  """
  
  # 1. 실행할 행동 (None은 '실행할 행동 없음'을 의미)
  action_schema = {
    "type": ["string", "null"],
    "enum": list(available_actions) + [None],
  }
  
  # 2. 도구 실행에 사용할 인자
  arguments_schema = {    
    "type": "object",
    "properties": {
      "trip_date": {
        "type": ["string", "null"],
      },
      "meeting_time": {
        "type": ["string", "null"],
      },
      "transport_type": {
        "type": ["string", "null"],
        "enum": ["KTX", "BUS", None],  
      } 
    },
    "required": [
      "trip_date",
      "meeting_time",
      "transport_type"
    ],
    "additionalProperties": False,
  }
  
  # 3. 행동을 선택한 이유
  reason_schema = {
    "type": "string",  
  }
  
  # 4. 전체 판단 결과
  return {
    "type": "object",
    "properties": {
      "action": action_schema,
      "arguments": arguments_schema,
      "reason": reason_schema,
    },
    "required": ["action", "arguments", "reason"],
    "additionalProperties": False, 
  }

def ask_llm(goal, current_state, available_actions, history=None):  
  """목표와 현재 상태, 실행 이력을 바탕으로 LLM에 다음 행동을 요청합니다.

  Args:
      goal (str): 사용자가 달성하려는 목표
      current_state (dict): 현재까지 확인된 정보
      available_actions (list): 실행 가능한 행동 목록
      history (list, optional): 이전 행동과 실행 결과 기록. 생략하면 None.

  Returns:
      dict: 선택한 행동(action), 실행 인자(arguments), 선택 이유(reason).
            선택할 행동이 없으면 action은 None.
  """  
  # LLM이 다음 행동을 판단하는데 필요한 정보를 모읍니다.
  context = {    
    "goal": goal,                           # 달성하려는 목표    
    "current_state": current_state,         # 현재까지 확인된 정보    
    "available_actions": available_actions, # 실행 가능한 행동 목록    
    "history": history if history is not None else [],  # 실행 이력, 없으면 빈 목록
  }

  # LLM 보낼 정보 : 입력 정보를 JSON 문자열로 변환
  context_input =json.dumps(context, ensure_ascii=False)
  
  # LLM 받을 형식 : 판단 결과의 항목과 자료형을 정의
  decision_schema = build_decision_schema(available_actions)
  
  # LLM 에게 판단을 요청합니다.
  response = client.responses.create(
    # 사용할 모델
    model="gpt-5.6",      
    # 목표, 현재 상태, 실행 이력 등 판단에 필요한 정보
    input=context_input,        
    # 다음 행동을 선택할 때 따를 판단 지침
    instructions=DECISION_INSTRUCTIONS,  
    # 답변의 출력 형식 설정
    text={
        "format": {          
          "type": "json_schema",        # JSON 스키마에 맞춰 답변          
          "name": "agent_decision",     # 응답 형식에 붙인 이름          
          "strict": True,               # 지정한 스키마를 엄격하게 준수          
          "schema": decision_schema,    # 답변의 항목과 자료형 규칙
        }
    }
  )

  # LLM의 답변을 JSON 문자열로 가져옵니다.
  answer_text = response.output_text
  
  # JSON 문자열을 파이썬 딕셔너리로 변환합니다.
  decision = json.loads(answer_text)

  # 선택한 행동이 실행 가능한 목록에 있는지 검사합니다.
  if decision["action"] is not None:
    if decision["action"] not in available_actions:
      raise ValueError(f"허용되지 않은 행동: {decision['action']}")

  # LLM 판단 결과를 반환합니다.
  return decision

def execute_action(decision):
  """선택한 행동에 따라 도구를 실행합니다."""
  
  action = decision["action"]
  arguments = decision["arguments"]
  
  # 선택한 행동이 없으면 -> 실행하지 않음 
  if action is None:
    return None
    
  # 캘린더 조회면 -> 캘린더 실행
  elif action == "check_calendar":
    result = check_calendar()

  # 교통편 검색이면 -> 필요한 값 확인 후 검색 
  elif action == "search_transport":    
    trip_date = arguments["trip_date"]
    meeting_time = arguments["meeting_time"]
    transport_type = arguments["transport_type"]
     
    if transport_type not in ("KTX", "BUS"):
        raise ValueError("검색할 교통수단을 지정해야 합니다.")
    
    if not trip_date or not meeting_time:
      raise ValueError("출장 날짜와 시간을 먼저 확인해야 합니다.")
    
    result = search_transport(
      trip_date,
      meeting_time,
      transport_type
    )
    
  # 그 외의 행동이면 -> 오류로 알림
  else:
    raise ValueError(f"지원하지 않는 행동: {action}")
  
  return result

# ------------------------------------------------------------
# 참고 : build_decision_schema() 에서 사용하는 JSON 스키마 키워드
# ------------------------------------------------------------
# JSON 스키마(schema)는 데이터의 형식과 규칙을 정의합니다.
# 
# type 
#   값의 자료형을 지정합니다.
#   - "string": 문자열 (예: "KTX")
#   - "object": 여러 항목을 담는 객체
#   - "null": 값이 없음 
#   - ["string", "null"]: 문자열 또는 null을 허용 
# 
# properties
#   객체 안에 들어갈 항목과 각 항목의 규칙을 정의합니다.
#   예: "trip_date": {"type": ["string", "null"]}
#     -> trip_date의 값으로 문자열 또는 null을 허용 
# 
# required
#   반드시 포함해야 하는 항목의 이름을 지정합니다.
#   항목이 필수여도, type에서 null을 허용하면 값은 null일 수 있습니다.
# 
# enum
#   사용할 수 있는 값을 나열합니다.
#   예: ["KTX", "BUS", None] -> 이 세 값 중 하나만 허용
# 
# additionalProperties
#   properties에 정의하지 않은 추가 항목을 허용할 지 정합니다.
#   False이면 추가 항목을 허용하지 않습니다.
