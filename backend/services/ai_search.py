import json
import re
from typing import Optional, Dict, List
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class AISearchService:
    """AI-powered search service using natural language processing"""
    
    @staticmethod
    def parse_natural_language_query(query: str) -> Dict:
        """Parse natural language query into structured filters"""
        prompt = f"""Parse this real estate search query and extract structured filters.
        
Query: "{query}"

Return a JSON object with these optional fields:
{{
    "min_price": number or null,
    "max_price": number or null,
    "bedrooms": number or null,
    "bathrooms": number or null,
    "property_type": string or null,
    "location": string or null,
    "keywords": [list of relevant keywords]
}}

Only include fields that are mentioned in the query. Return ONLY valid JSON."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract real estate search parameters. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            result_text = response['choices'][0]['message']['content']
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception as e:
            print(f"Error parsing query: {e}")
            return {}
    
    @staticmethod
    def generate_recommendations(
        user_query: str,
        budget: Optional[int] = None,
        bedrooms: Optional[int] = None,
        location: Optional[str] = None
    ) -> str:
        """Generate personalized property recommendations"""
        
        context = f"User is looking for: {user_query}"
        if budget:
            context += f"\nBudget: PKR {budget:,}"
        if bedrooms:
            context += f"\nPreferred bedrooms: {bedrooms}"
        if location:
            context += f"\nPreferred location: {location}"
        
        prompt = f"""{context}

Based on the above criteria, provide 3 personalized property recommendations with reasoning."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional real estate advisor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"
    
    @staticmethod
    def generate_investment_insights(
        property_price: int,
        rental_income: Optional[float] = None,
        location: Optional[str] = None,
        area_sqft: Optional[float] = None
    ) -> Dict:
        """Generate investment insights for a property"""
        
        context = f"Property price: PKR {property_price:,}"
        if rental_income:
            context += f"\nEstimated monthly rental: PKR {rental_income:,}"
        if location:
            context += f"\nLocation: {location}"
        if area_sqft:
            context += f"\nArea: {area_sqft} sqft"
        
        prompt = f"""{context}

Provide investment analysis in JSON format:
{{
    "roi_percentage": number,
    "payback_period_years": number,
    "risk_level": "low|medium|high",
    "investment_potential": "poor|fair|good|excellent",
    "recommendation": "string",
    "reasons": ["list of reasons"]
}}

Return ONLY valid JSON."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a real estate investment analyst. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            result_text = response['choices'][0]['message']['content']
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception as e:
            print(f"Error generating investment insights: {e}")
            return {}
    
    @staticmethod
    def compare_areas(area1: str, area2: str, criteria: Optional[List[str]] = None) -> str:
        """Compare two areas"""
        
        compare_criteria = criteria or ["pricing", "safety", "amenities", "investment potential", "development"]
        
        prompt = f"""Compare {area1} and {area2} based on these criteria:
{', '.join(compare_criteria)}

Provide a detailed comparison for real estate investors."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a real estate market analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error comparing areas: {str(e)}"
    
    @staticmethod
    def generate_market_insights(location: str) -> Dict:
        """Generate market insights for a location"""
        
        prompt = f"""Provide market insights for {location} in JSON format:
{{
    "market_trend": "string (bull/bear/stable)",
    "average_price_trend": "string (increasing/decreasing/stable)",
    "investment_rating": number (1-10),
    "key_factors": ["list"],
    "recommendations": ["list"],
    "risk_factors": ["list"]
}}

Return ONLY valid JSON."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a real estate market analyst. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            result_text = response['choices'][0]['message']['content']
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception as e:
            print(f"Error generating market insights: {e}")
            return {}

# Initialize service
ai_search_service = AISearchService()
