"""
파일 : agent_runner.py
역할 : LLM의 판단을 도구 실행으로 연결하고, 현재 상태와 실행 이력을 관리합니다.

주요 함수:
    step(): 판단과 실행을 한 번 수행하고, 결과를 상태와 이력에 반영합니다.
            선택한 행동이 없으면 도구를 실행하지 않습니다.
    run(): step()을 반복 호출하고, 종료 여부와 최대 판단 횟수를 확인합니다.
"""

from agent_core import ask_llm, execute_action

def step(goal, current_state, available_actions, history):
    """LLM 판단과 도구 실행을 한 번 수행합니다.

    Args:
        goal (str): 사용자가 달성하려는 목표
        current_state (dict): 현재 상태. 실행 결과로 갱신합니다.
        available_actions (list): 실행 가능한 행동 목록
        history (list): 실행 이력. 이번 행동과 결과를 추가합니다.

    Returns:
        dict: 판단 결과(decision)와 도구 실행 결과(result).
                선택한 행동이 없으면 result는 None.
    """
    
    # 1. 현재 상태와 실행 이력을 바탕으로 다음 행동을 요청합니다. 
    decision = ask_llm(
        goal=goal,
        current_state=current_state,
        available_actions=available_actions,
        history=history,
    )    
    
    # 2. 선택한 행동이 없으면 실행하지 않고 리턴합니다.
    if decision["action"] is None:
        return {
            "decision": decision,
            "result": None,
        }
    
    # 3. LLM의 판단 결과(action, arguments)를 전달하여 선택한 도구를 실행합니다.
    result = execute_action(decision)
    
    # 4. 실행 결과를 현재 상태에 반영합니다.
    current_state.update(result)
    
    # 5. 이번 행동과 실행 결과를 이력에 기록합니다.
    history.append({
        "action": decision["action"],       # LLM이 선택한 행동
        "arguments": decision["arguments"], # 도구 실행에 전달한 인자
        "reason": decision["reason"],       # LLM이 이 행동을 선택한 이유
        "result": result,                   # 도구가 반환한 실제 실행 결과
    })
    
    # 6. 이번 판단과 실행 결과를 호출한 곳(쥬피터 노트북 또는 run 함수)에 반환합니다.
    return {
        "decision": decision, # LLM 의 판단 결과 (행동, 실행 인자, 선택 이유)
        "result": result,   # 도구가 반환한 실행 결과
    }
    
def run(goal, max_steps=5):
    """step()을 반복 호출하고 종료 결과를 반환합니다.
    
    Args:
        goal (str): 사용자가 달성하려는 목표
        max_steps (int): 최대 판단 횟수. 기본값은 5.
    
    Returns:
        dict: 종료 상태(status), 종료 이유(reason),
                현재 상태(current_state), 실행 이력(history).
    """
    
    if max_steps < 1:
        raise ValueError("최대 판단 횟수는 1 이상이어야 합니다.")
    
    # 1. 현재 상태, 실행 가능한 행동, 실행 이력을 초기화합니다.
    current_state = {
        "trip_date": None,          # 출장 일자
        "meeting_time": None,       # 미팅 시간
        "transport_type": None,     # 교통수단 (KTX, BUS)
        "transport_status": None,   # 교통편 검색 상태(sold_out, available)
        "transport_message": None,  # 검색 결과를 설명하는 문장
    }

    available_actions = [
        "check_calendar",
        "search_transport",
    ]
    
    history = []
    
    # 최대 판단 횟수에 도달했을 때 사용할 기본 종료 결과입니다.
    status = "MAX_STEPS"
    reason = "최대 판단 횟수에 도달했습니다."

    # 2. 판단과 실행을 반복합니다.
    for step_number in range(1, max_steps + 1):
        print(f"\n[STEP {step_number}]")
        
        step_result = step(
            goal=goal,
            current_state=current_state,
            available_actions=available_actions,
            history=history,            
        )
    
        decision = step_result["decision"]
        result = step_result["result"]
        
        print("선택한 행동:", decision["action"] )
        print("실행 인자:", decision["arguments"])
        print("선택 이유:", decision["reason"])
        
        # 3. 선택한 행동이 없으면 종료 상태를 정하고 반복을 끝냅니다.
        if decision["action"] is None:
            # LLM이 종료를 선택한 경우
            reson = decision["reason"]
            
            if current_state["transport_status"] == "available":
                status = "SUCCESS"
            else:
                status = "INCOMPLETE"                            
            break
        else:
            print("실행 결과:", result)
    
            
    # 4. 반복이 끝나면 최종 결과를 반환 합니다.
    # - action이 None이면: break로 반복을 종료한 뒤 이곳으로 이동합니다.
    # - 최대 판단 횟수를 채우면: 반복을 모두 마친 뒤 이곳으로 이동합니다.    
    return {
        "status": status,
        "reason": reason,
        "current_state": current_state,
        "history": history,
    }