import requests
import json
import logging

class RLMContextLayer:
    """
    Recursive Language Model (RLM) layer.
    Manages expanding conversation context for very large context windows.
    Automatically summarizes older messages if the context ceiling is reached,
    maintaining a "recursive" understanding of the conversation history.
    """
    def __init__(self, max_tokens=100000):
        self.history = []
        self.max_tokens = max_tokens
        self.system_prompt = {
            "role": "system",
            "content": (
                "You are an expert remote sensing and geospatial AI. "
                "You analyze land cover change metrics across years to predict "
                "the possibility of natural calamities and discuss environmental impacts. "
                "Base your insights on parameters like Barren Land, Buildings, Water Bodies, and Vegetation."
            )
        }
        self.history.append(self.system_prompt)

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        self._manage_context()

    def _manage_context(self):
        # A simple estimation of token count (e.g. 1 token ~= 4 chars)
        current_length = sum(len(m["content"]) for m in self.history) // 4
        
        # If the history exceeds max tokens, recursive trimming/summarization is applied
        if current_length > self.max_tokens:
            logging.info("Context limit reached. Applying recursive summarization / trimming.")
            # Keep system prompt + last 10 interactions as a simplified strategy
            self.history = [self.system_prompt] + self.history[-10:]

    def get_messages(self):
        return self.history

class OpenWeightLLMClient:
    """
    Client for interacting with open-weight LLMs (like an OSS 120B model) via an API endpoint.
    Assumes an OpenAI-compatible interface commonly used by vLLM or standard inference servers.
    """
    def __init__(self, api_url, api_key=None, model_name="oss-120b"):
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name
        self.rlm_layer = RLMContextLayer()

    def send_prompt(self, text_input):
        self.rlm_layer.add_message("user", text_input)
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        payload = {
            "model": self.model_name,
            "messages": self.rlm_layer.get_messages(),
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        try:
            # Assuming openai compatible `/v1/chat/completions` endpoint
            response = requests.post(
                f"{self.api_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0  # Prevent hanging requests
            )
            response.raise_for_status()
            response_data = response.json()
            
            # Additional validation
            if 'choices' not in response_data or len(response_data['choices']) == 0:
                raise ValueError("Invalid response format from API: missing 'choices' array")
                
            assistant_reply = response_data['choices'][0]['message']['content']
            self.rlm_layer.add_message("assistant", assistant_reply)
            return assistant_reply
            
        except requests.exceptions.Timeout:
            logging.error("LLM API request timed out.")
            return "Error: The AI model took too long to respond. Please try again."
        except requests.exceptions.ConnectionError:
            logging.error(f"Failed to connect to LLM API at {self.api_url}")
            return "Error: Could not connect to the AI model server. Verify the server is running."
        except requests.exceptions.RequestException as e:
            logging.error(f"LLM API Request Failed: {e}")
            if e.response is not None:
                logging.error(f"Response status: {e.response.status_code}, body: {e.response.text}")
            return f"Error: Communication with the AI model failed (HTTP Error)."
        except ValueError as e:
            logging.error(f"JSON Parsing Error: {e}")
            return "Error: Parsing the AI model response failed."
        except Exception as e:
            logging.error(f"Unexpected error in LLM client: {e}")
            return "An unexpected error occurred while processing the request."

# Example test logic
if __name__ == "__main__":
    client = OpenWeightLLMClient(api_url="http://localhost:8000", model_name="llama-120b")
    
    # Simulating feeding the change detection report
    report_input = (
        "Land cover change report for Target Region between 2010 and 2020:\n"
        "- Buildings: Increased by 45%\n"
        "- Vegetation: Decreased by 30%\n"
        "- Water Bodies: Decreased by 15%\n"
        "\nPredict natural calamity occurrence based on these metrics."
    )
    
    print("SENDING ANALYSIS REPORT:", report_input)
    # response = client.send_prompt(report_input)
    # print("LLM RESPONSE:", response)
