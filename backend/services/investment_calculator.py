from typing import Optional
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class InvestmentCalculator:
    """Investment analysis and calculation service"""
    
    @staticmethod
    def calculate_roi(
        property_price: int,
        annual_rental_income: float,
        annual_appreciation_rate: float = 0.05
    ) -> dict:
        """Calculate ROI for property investment"""
        
        # Year 1 metrics
        annual_roi = (annual_rental_income / property_price) * 100
        first_year_appreciation = property_price * annual_appreciation_rate
        first_year_total_return = annual_rental_income + first_year_appreciation
        first_year_roi = (first_year_total_return / property_price) * 100
        
        return {
            "annual_rental_roi": round(annual_roi, 2),
            "first_year_total_roi": round(first_year_roi, 2),
            "first_year_appreciation": round(first_year_appreciation, 0),
            "payback_period_years": round(property_price / annual_rental_income, 1) if annual_rental_income > 0 else None
        }
    
    @staticmethod
    def calculate_mortgage(
        loan_amount: float,
        annual_interest_rate: float,
        loan_tenure_years: int
    ) -> dict:
        """Calculate mortgage EMI"""
        
        monthly_rate = annual_interest_rate / 12 / 100
        num_payments = loan_tenure_years * 12
        
        if monthly_rate == 0:
            monthly_emi = loan_amount / num_payments
        else:
            monthly_emi = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
                         ((1 + monthly_rate) ** num_payments - 1)
        
        total_amount = monthly_emi * num_payments
        total_interest = total_amount - loan_amount
        
        return {
            "monthly_emi": round(monthly_emi, 0),
            "total_amount": round(total_amount, 0),
            "total_interest": round(total_interest, 0),
            "num_payments": num_payments
        }
    
    @staticmethod
    def analyze_investment_property(
        property_price: int,
        location: str,
        property_type: str,
        annual_rental_income: float,
        annual_appreciation_rate: float = 0.05,
        maintenance_cost_percentage: float = 0.05
    ) -> dict:
        """Comprehensive investment analysis"""
        
        annual_maintenance = property_price * maintenance_cost_percentage
        net_annual_income = annual_rental_income - annual_maintenance
        
        roi_data = InvestmentCalculator.calculate_roi(
            property_price,
            net_annual_income,
            annual_appreciation_rate
        )
        
        # Risk assessment
        if net_annual_income <= 0:
            risk_level = "high"
            investment_potential = "poor"
        elif roi_data["first_year_total_roi"] < 5:
            risk_level = "high"
            investment_potential = "fair"
        elif roi_data["first_year_total_roi"] < 10:
            risk_level = "medium"
            investment_potential = "good"
        else:
            risk_level = "low"
            investment_potential = "excellent"
        
        return {
            "property_price": property_price,
            "location": location,
            "property_type": property_type,
            "annual_rental_income": annual_rental_income,
            "annual_maintenance_cost": annual_maintenance,
            "net_annual_income": net_annual_income,
            "annual_rental_roi": roi_data["annual_rental_roi"],
            "first_year_total_roi": roi_data["first_year_total_roi"],
            "payback_period_years": roi_data["payback_period_years"],
            "risk_level": risk_level,
            "investment_potential": investment_potential,
            "recommendation": f"This {property_type} in {location} is rated as {investment_potential} investment."
        }
    
    @staticmethod
    def calculate_appreciation_value(
        current_price: int,
        annual_appreciation_rate: float,
        years: int
    ) -> dict:
        """Calculate future property value"""
        
        future_value = current_price * ((1 + annual_appreciation_rate) ** years)
        total_appreciation = future_value - current_price
        
        year_wise = {}
        for year in range(1, years + 1):
            year_wise[f"year_{year}"] = round(
                current_price * ((1 + annual_appreciation_rate) ** year), 0
            )
        
        return {
            "current_price": current_price,
            "future_value": round(future_value, 0),
            "total_appreciation": round(total_appreciation, 0),
            "appreciation_percentage": round((total_appreciation / current_price) * 100, 2),
            "year_wise_values": year_wise
        }
    
    @staticmethod
    def compare_investment_scenarios(
        property_price: int,
        scenarios: list
    ) -> dict:
        """Compare different investment scenarios"""
        
        comparison = {}
        
        for scenario in scenarios:
            name = scenario.get("name", "Scenario")
            rental_income = scenario.get("annual_rental_income", 0)
            appreciation = scenario.get("annual_appreciation_rate", 0.05)
            
            roi_data = InvestmentCalculator.calculate_roi(
                property_price,
                rental_income,
                appreciation
            )
            
            comparison[name] = {
                "annual_rental_income": rental_income,
                "annual_roi": roi_data["annual_rental_roi"],
                "first_year_total_roi": roi_data["first_year_total_roi"],
                "payback_period": roi_data["payback_period_years"]
            }
        
        return comparison
    
    @staticmethod
    def get_price_prediction(
        location: str,
        current_price: int,
        property_type: str,
        years: int = 5
    ) -> dict:
        """Get AI-powered price prediction"""
        
        prompt = f"""Based on real estate market trends, predict the future price of a {property_type} 
        in {location} currently priced at PKR {current_price:,} over the next {years} years.
        
        Provide response in JSON format:
        {{
            "year_1": number,
            "year_3": number,
            "year_5": number,
            "confidence_percentage": number,
            "market_factors": ["list"],
            "prediction_rationale": "string"
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
            
            import json
            result_text = response['choices'][0]['message']['content']
            import re
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception as e:
            print(f"Error predicting price: {e}")
            return {}
