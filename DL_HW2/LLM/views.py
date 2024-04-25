from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
import torch
import LLM.models
import LLM.utils

class Chatbot:

    FILE = "./LLM/new_data.pth"

    with open('./LLM/assets/new_intents.json', 'r') as f:
        intents = json.load(f)

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # self.device = 'cpu'
        self.data = torch.load(self.FILE)
        self.bot_name = "Chatbot"
        self.prep = LLM.utils.Preprocessor()
        self._get_info()
        self._make_model()

    def _get_info(self):
        self.input_size = self.data["input_size"]
        self.hidden_size = self.data["hidden_size"]
        self.output_size = self.data["output_size"]
        self.all_words = self.data['all_words']
        self.tags = self.data['tags']
        self.model_state = self.data["model_state"]

    def _make_model(self):
        self.model = LLM.models.ANN(self.input_size, self.hidden_size, self.output_size).to(self.device)
        self.model.load_state_dict(self.model_state)
        self.model.eval()
        
    def chat(self, message):
        sentence = self.prep.chatbot_msg_process(message)
        x = self.prep.bag_of_words(sentence, self.all_words)
        x = x.reshape(1, x.shape[0])
        x = torch.from_numpy(x).to(self.device)

        output = self.model(x)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])
        else:
            return "I do not understand..."

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            if message:
                
                # 在這裡可以對訊息進行處理，然後給予回覆
                chatbot = Chatbot()
                response_message = chatbot.chat(message)
                print(response_message)

                # response_message = "Chatbot > " + message
                return JsonResponse({'status': True, 'data': response_message})
            else:
                return JsonResponse({'status': False, 'message': '參數錯誤：請提供訊息'})
        except Exception as e:
            return JsonResponse({'status': False, 'failed': str(e)})
    else:
        return JsonResponse({'status': False, 'message': '只支援 POST 請求'})
