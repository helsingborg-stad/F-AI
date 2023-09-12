import asyncio
import os
import pandas as pd
from planning_permission.app_main_stream import use_chat_stream
from langstream import collect_final_output

VERSION = 'v4'
EXCEL_INPUT_PATH = os.environ.get("EXCEL_INPUT_PATH", "./planning_qa.xlsx")
EXCEL_OUTPUT_PATH = os.environ.get("EXCEL_OUTPUT_PATH", "./planning_qa_output.xlsx")

async def join_stream_result(query: str, stream: callable, map_stream: callable = lambda x: x)-> str:
    result = await collect_final_output(stream(query))
    return ''.join(list(map(map_stream, list(result))))

def generate_answer(question: str)-> str:
    stream, prompts = use_chat_stream(question)
    print(question)
    return asyncio.run(join_stream_result(question, stream, lambda x: x.content))

def main():
    print(f"Input path: {EXCEL_INPUT_PATH} \nOutput path: {EXCEL_OUTPUT_PATH}")
    df = pd.read_excel(EXCEL_INPUT_PATH, engine='openpyxl')
    df = df[['GPT-4 fråga (v1)']]
    df[f'GPT-4 svar ({VERSION})'] = df['GPT-4 fråga (v1)'].apply(generate_answer)
    df.to_excel(EXCEL_OUTPUT_PATH, index=False, engine='openpyxl')

if __name__ == "__main__":
    main()