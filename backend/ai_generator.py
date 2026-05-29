import os
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


class BossData(BaseModel):
    name: str = Field(description="A creative, intimidating name for a geometric Star Boss.")
    taunt: str = Field(description="A short, one-sentence taunt aimed at the player.")
    speed_multiplier: float = Field(description="A speed multiplier between 0.5 and 1.5.")
    color_hex: str = Field(description="A dark, menacing hex color code.")


class AIBossGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.9,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_boss(self, wave_number: int) -> BossData:
        prompt = PromptTemplate(
            template="You are the architect of a geometric universe. The player has survived {wave} waves. Generate a final Star Boss.",
            input_variables=["wave"]
        )

        chain = prompt | self.llm.with_structured_output(BossData)
        return chain.invoke({"wave": wave_number})