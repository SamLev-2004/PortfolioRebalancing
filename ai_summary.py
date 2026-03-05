from google import genai
import pandas as pd
from typing import List, Dict, Union, Any

def generate_trade_rationale(api_key: str, trades_list: List[Dict[str, Any]], tax_report: Union[Dict[str, float], str]) -> str:
    """
    Sends the optimized mathematical trades to Google Gemini to translate 
    into a conversational, human-friendly summary.
    
    Args:
        api_key (str): The Google Gemini API Key
        trades_list (list): List of dictionaries containing the recommended trades
        tax_report (dict|str): The estimated tax impact dictionary, or a string indicating no tax hit
        
    Returns:
        str: A human-friendly explanation of the trades
    """
    if not api_key:
        return "Please enter a Google Gemini API Key in the sidebar to generate AI Insights."
        
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are a highly intelligent, empathetic AI Roboadvisor. 
        Your job is to explain a set of rebalancing trades to a user in a simple, friendly paragraph.
        
        Here are the trades we are suggesting mathematically:
        {trades_list}
        
        Here is the estimated Canadian tax impact:
        {tax_report}
        
        Write a concise, 3-4 sentence explanation. Use a friendly tone, start with "Hey there! I've analyzed your portfolio..." 
        Explain *why* we are making the swaps (e.g., locking in profits, sheltering in TFSA, etc.) and address the tax hit gently if there is one. 
        Do not use markdown lists, just a conversational paragraph.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Could not generate AI summary: {e}"

