import os
import requests
from openai import OpenAI

class News_Authenticator:
    def __init__(self, groq_api_key, merge_prompt, groq_model="llama-3.3-70b-versatile"):
        self.client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.groq_model = groq_model
        self.system_prompt = merge_prompt
        
    def merge_text(self, summaries):
        """
        Merges multiple pre-existing summaries using Groq.
        """
        if not summaries:
            raise ValueError("At least one summary must be provided")

        merge_input = ""
        for i, summary in enumerate(summaries, 1):
            merge_input += f"Summary {i}:\n{summary}\n\n"
        prompt = f"{self.system_prompt}\n\nHere are the summaries to merge\n\n{merge_input}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content if response.choices[0].message.content else "Merging failed"
        except Exception as e:
            print(f"Error in merging summaries with Groq: {str(e)}")
            return "Merging failed"

class ImgBBUploader:
    def __init__(self, api_key=None):
        self.api_key = api_key or "YOUR_API_KEY"
        self.upload_url = "https://api.imgbb.com/1/upload"

    def upload_image(self, image_path):
        """Upload image to ImgBB using multipart/form-data and return the URLs"""
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError("Image file not found!")

            with open(image_path, "rb") as file:
                files = {
                    "image": file
                }
                payload = {
                    "key": self.api_key,
                    "name": os.path.basename(image_path)
                }

                response = requests.post(self.upload_url, data=payload, files=files)
                response.raise_for_status()
                
                data = response.json()
                if data["success"]:
                    return {
                        "direct_url": data["data"]["url"],
                        "delete_url": data["data"]["delete_url"],
                        "thumbnail_url": data["data"]["thumb"]["url"],
                        "medium_url": data["data"].get("medium", {}).get("url"),
                    }
                else:
                    raise Exception("Upload failed: " + str(data))

        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {str(e)}")
            return None
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None