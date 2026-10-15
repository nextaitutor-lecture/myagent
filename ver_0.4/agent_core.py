"""
파일 : agent_core.py 
역할 : Agent의 판단과 행동 실행 제어
주요 함수 : ask_llm(), execute_action()
"""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from agent_tools import check_calendar, search_transport

# 프로젝트 루트
PROJECT_ROOT = Path(r"D:\nextaitutor\myagent")

# Python 모듈 검색 경로에 추가
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
# OpenAI API 클라이언트 생성
client = OpenAI()

def ask_llm(goal, current_state, available_actions, history=None):
  """
  현재 상태와 실행 이력을 바탕으로 LLM이 다음 행동을 선택합니다.
  
  Args:
    goal (str) : 사용자가 달성하려는 목표
    current_state (dict) : 현재까지 확인된 출장 정보
    available_actions (list) : 실행 가능한 행동 목록
    history (list) : 이전 행동과 실행 결과 기록
  
  Returns:
    dict: 선택한 행동(action)과 선택 이유(reason)
          적절한 행동이 없으면 action은 None    
  """
  
  context = {
    "goal": goal,
    "current_state": current_state,
    "available_actions": available_actions,
    "history": history if history is not None else [],
  }

  context_input =json.dumps(context, ensure_ascii=False)
  
  print("===== LLM에 전달하는 Context =====")    
  print(context_input)

  response = client.responses.create(
      model="gpt-5.6",    
      input=context_input,
      instructions=(
        "당신은 부산 출장 준비 AI Agent입니다. "
        "현재 상태와 실행 이력을 보고 다음 행동을 선택하세요. "
        "출장 날짜가 없으면 check_calendar를 선택하세요. "
        "출장 날짜가 확인되면 KTX를 먼저 검색하세요. "
        "KTX가 매진되었다면 BUS를 검색하세요. "
        "동일한 조건으로 실패한 검색을 반복하지 마세요. "
        "교통편이 확보 가능하면 action을 null로 반환하세요. "
        "사용 가능한 도구 외의 행동을 선택하지 마세요. "
        "search_transport를 선택할 때 arguments.transport_type에 "
        "KTX 또는 BUS를 지정하세요. "
        "check_calendar 또는 null을 선택하면 transport_type은 null 입니다."
        "행동을 실제로 실행했다고 주장하지 마세요. "
      ),        
      text={
          "format": {
              "type": "json_schema",
              "name": "agent_decision",
              "strict": True,
              "schema": {
                  "type": "object",
                  "properties": {
                      "action": {
                          "type": ["string", "null"],
                          "enum": available_actions + [None]
                      },
                      "arguments": {
                          "type": "object",
                          "properties": {
                              "transport_type": {
                                  "type": ["string", "null"],
                                  "enum": ["KTX", "BUS", None]
                              }
                          },
                          "required": ["transport_type"],
                          "additionalProperties": False
                      },
                      "reason": {
                          "type": "string"
                      }
                  },
                  "required": [
                      "action",
                      "arguments",
                      "reason"
                  ],
                  "additionalProperties": False
              }
          }
      }
  )

  decision = json.loads(response.output_text)

  if decision["action"] is not None:
    if decision["action"] not in available_actions:
      raise ValueError(f"허용되지 않은 행동: {decision['action']}")

  return json.loads(response.output_text)

def execute_action(decision, current_state, history):
  """
  선택한 도구를 실행하고 현재 상태와 실행 이력을 갱신합니다.
  """
  
  action = decision["action"]
  arguments = decision["arguments"] or {}
  
  if action == "check_calendar":
    result = check_calendar()
    
  elif action == "search_transport":
    transport_type = arguments["transport_type"]
    
    if transport_type not in ("KTX", "BUS"):
        raise ValueError("올바른 교통수단을 선택해야 합니다.")
    
    if not current_state.get("trip_date"):
      raise ValueError("출장 날짜가 확인되지 않았습니다.")
    
    result = search_transport(
      current_state["trip_date"],
      current_state["meeting_time"],
      transport_type
    )

  elif action is None:
    print("실행할 다음 행동이 없습니다.")
    return None
  
  else:
    raise ValueError(f"지원하지 않는 행동: {action}")
  
  current_state.update(result)
  
  history.append({
   "action": action,
   "arguments": arguments,
   "result": result
  })  
  
  return result