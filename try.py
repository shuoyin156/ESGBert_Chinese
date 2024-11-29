import torch
import torch.nn as nn
from main import device, tokenizer
import warnings

warnings.filterwarnings("ignore")

 # 使用模型进行预测
def predict_sentiment(text, model, tokenizer):
    model.eval()
    encoding = tokenizer(text, padding='max_length', truncation=True, max_length=128, return_tensors='pt')
    input_ids = encoding['input_ids'].squeeze(0)
    attention_mask = encoding['attention_mask'].squeeze(0)

    input_ids = input_ids.to(device)
    attention_mask = attention_mask.to(device)

    with torch.no_grad():
        output = model(input_ids.unsqueeze(0), attention_mask.unsqueeze(0)).last_hidden_state[:, 0]
        logits = classifier(output)
        probs = nn.functional.softmax(logits, dim=1)
        pred = probs.argmax(dim=1).item()

    return 'Positive' if pred == 1 else 'Negative', probs[0][1].item()


text = "燕谷坊集团作为国家农业产业化重点龙头企业，积极实践“碳达峰”和“碳中和”时代使命。深入围绕“低碳农业、有机农业、绿色农业”，全产业链减碳。从产业上游推广“育种技术创新，绿色有机栽培技术推广，燕麦治沙。燕谷坊集团燕麦种植面积50万亩，促进大规模土地绿化行动进一步推进，加速碳减排协调实现；在数字化、智能化、科技化的引领下，产业中游深入开发燕麦全谷物加工链，不浪费燕麦一点，减少从良田到餐桌的食品损失，共同耕耘“无形良田”，利用数字化、智能化技术打造全谷物加工生产线，提高生产资源利用效率，减少温室气体排放；推动工业下游精心打造健康美味的绿色食品，获得国家绿色食品认证，促进绿色消费，发展绿色经济。"


model = torch.load('models/save_model.pt',map_location='cpu').to(device)
classifier = nn.Linear(model.config.hidden_size, 2).to(device)
sentiment, prob = predict_sentiment(text, model, tokenizer)
#print(f'Text: {text}')
print(f'Text:{text}')
print(f'Sentiment: {sentiment}, Probability: {prob:.3f}')