import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel,function_tool
from agents import  set_tracing_disabled
set_tracing_disabled(True)
load_dotenv(override=True)


gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# Config setup
config = RunConfig(
    model=model,
    model_provider=external_client
)
    

# Predefined FAQs
FAQS = {
    "what is your name?": "I am a simple FAQ bot.",
    "who created you?": "I was created for an assignment using the OpenAI Agent SDK.",
    "what can you do?": "I can answer some basic predefined questions.",
    "how are you?": "I am just a bot, but I am doing great!",
    "bye": "Goodbye! Have a nice day."
}

# Create FAQ Agent
faq_agent = Agent(
    name="faq_bot",
    model=model,
    instructions="You are a helpful FAQ bot. Answer only based on the predefined FAQs.",
)

# Function to handle FAQ lookup
@function_tool
def answer_faq(question: str) -> str:
    q = question.lower().strip()
    return FAQS.get(q, "Sorry, I don’t know the answer to that question.")

# Async main loop
async def main():
    print("FAQ Bot is running! Ask me something (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break

        # Run agent asynchronously
        result = await Runner.run(faq_agent, input=user_input, )
        print("Bot:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())