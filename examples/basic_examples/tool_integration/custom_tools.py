import json
from datetime import datetime
from typing import Dict, List, Any


def calculator_tool(expression: str) -> str:
    """Evaluates mathematical expressions safely."""
    try:
        # Remove any extra whitespace and normalize operators
        expression = expression.strip()
        
        # Basic safety check - only allow basic math operations
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return json.dumps({
                "error": "Expression contains invalid characters. Only basic math operations (+, -, *, /, .) and parentheses are allowed.",
                "expression": expression
            })
        
        # Evaluate the expression
        result = eval(expression)
        
        return json.dumps({
            "expression": expression,
            "result": result,
            "calculation_steps": f"Evaluated: {expression} = {result}",
            "timestamp": datetime.now().isoformat()
        })
    except ZeroDivisionError:
        return json.dumps({
            "error": "Division by zero is not allowed",
            "expression": expression
        })
    except Exception as e:
        return json.dumps({
            "error": f"Error evaluating expression: {str(e)}",
            "expression": expression
        })


def weather_lookup_tool(city: str) -> str:
    """Simulates a weather lookup for a given city."""
    # Simulated weather data
    weather_data = {
        "New York": {"temperature": 72, "condition": "sunny", "humidity": 65},
        "London": {"temperature": 58, "condition": "cloudy", "humidity": 80},
        "Tokyo": {"temperature": 75, "condition": "rainy", "humidity": 70},
        "Sydney": {"temperature": 68, "condition": "partly cloudy", "humidity": 55},
        "Paris": {"temperature": 62, "condition": "overcast", "humidity": 75}
    }
    
    if city in weather_data:
        data = weather_data[city]
        return json.dumps({
            "city": city,
            "temperature": data["temperature"],
            "condition": data["condition"],
            "humidity": data["humidity"],
            "timestamp": datetime.now().isoformat()
        })
    else:
        return json.dumps({
            "error": f"Weather data not available for {city}",
            "available_cities": list(weather_data.keys())
        })


def currency_converter_tool(amount: float, from_currency: str, to_currency: str) -> str:
    """Simulates currency conversion."""
    # Simulated exchange rates
    rates = {
        "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0, "CAD": 1.25},
        "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 129.0, "CAD": 1.47},
        "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150.0, "CAD": 1.71},
        "JPY": {"USD": 0.009, "EUR": 0.0077, "GBP": 0.0067, "CAD": 0.011},
        "CAD": {"USD": 0.80, "EUR": 0.68, "GBP": 0.58, "JPY": 88.0}
    }
    
    if from_currency in rates and to_currency in rates[from_currency]:
        converted_amount = amount * rates[from_currency][to_currency]
        return json.dumps({
            "original_amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "converted_amount": round(converted_amount, 2),
            "exchange_rate": rates[from_currency][to_currency],
            "timestamp": datetime.now().isoformat()
        })
    else:
        return json.dumps({
            "error": f"Conversion not available from {from_currency} to {to_currency}",
            "supported_currencies": list(rates.keys())
        })


def text_analyzer_tool(text: str) -> str:
    """Analyzes text and provides basic statistics."""
    words = text.split()
    sentences = text.split('.')
    characters = len(text)
    
    # Basic sentiment analysis (simplified)
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'sad', 'angry']
    
    positive_count = sum(1 for word in words if word.lower() in positive_words)
    negative_count = sum(1 for word in words if word.lower() in negative_words)
    
    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return json.dumps({
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "character_count": characters,
        "average_word_length": round(sum(len(word) for word in words) / len(words), 2) if words else 0,
        "sentiment": sentiment,
        "positive_words": positive_count,
        "negative_words": negative_count,
        "timestamp": datetime.now().isoformat()
    }) 