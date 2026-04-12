from fastapi import FastAPI
from pydantic import BaseModel

from env.environment import Environment
from agent.llm_agent import get_llm_response

app = FastAPI()


class PromptAction(BaseModel):
    is_attack: bool
    type: str
    confidence: float = 0.0
    explanation: str = ""


class AnalyzeRequest(BaseModel):
    input: str


env = Environment()


@app.post("/reset")
def reset():
    obs = env.reset()

    if isinstance(obs, list):
        obs_text = " | ".join(obs)
    else:
        obs_text = obs

    return {
        "input_text": obs_text,
        "difficulty": "easy",
        "turn": 1,
        "total_tasks": env.total_steps
    }


@app.post("/step")
def step(action: PromptAction):
    action_dict = action.dict()

    next_state, reward, done, info = env.step(action_dict)

    if next_state is not None:
        if isinstance(next_state, list):
            next_text = " | ".join(next_state)
        else:
            next_text = next_state
    else:
        next_text = ""

    return {
        "observation": {
            "input_text": next_text,
            "difficulty": "easy",
            "turn": info["steps_done"],
            "total_tasks": info["total_steps"]
        },
        "reward": reward,
        "done": done,
        "info": info
    }


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    return get_llm_response(req.input)


# 🔥 IMPORTANT PART (validator ke liye)
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()