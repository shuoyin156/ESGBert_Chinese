import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel

# 设置随机种子，以确保实验结果可以被重现
SEED = 1234
torch.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 加载预训练的Bert模型和tokenizer
PRETRAINED_MODEL = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(PRETRAINED_MODEL)
bert_model = BertModel.from_pretrained(PRETRAINED_MODEL)

# 定义数据集类
class SentimentDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data.iloc[idx]['text']
        label = self.data.iloc[idx]['label']
        encoding = self.tokenizer(text, padding='max_length', truncation=True, max_length=256, return_tensors='pt')
        input_ids = encoding['input_ids'].squeeze(0)
        attention_mask = encoding['attention_mask'].squeeze(0)
        return input_ids, attention_mask, label

def main():
    # 加载数据集
    train_data = pd.read_csv('data/train.csv')
    val_data = pd.read_csv('data/test.csv')
    train_dataset = SentimentDataset(train_data, tokenizer)
    val_dataset = SentimentDataset(val_data, tokenizer)

    # 初始化模型和优化器
    NUM_CLASSES = 2
    model = BertModel.from_pretrained(PRETRAINED_MODEL)
    classifier = nn.Linear(model.config.hidden_size, NUM_CLASSES)
    optimizer = optim.Adam(classifier.parameters())

    # 定义损失函数和设备
    # criterion = nn.BCEWithLogitsLoss()
    criterion = nn.CrossEntropyLoss()
    model = model.to(device)
    classifier = classifier.to(device)
    criterion = criterion.to(device)

    # 训练模型
    NUM_EPOCHS = 5
    BATCH_SIZE = 32
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)
    for epoch in range(NUM_EPOCHS):
        train_loss = 0
        train_acc = 0
        model.train()
        for input_ids, attention_mask, labels in train_loader:
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask).last_hidden_state[:, 0]
            logits = classifier(outputs)

            loss = criterion(logits, labels)
            # loss = criterion(logits.view(-1, 2), labels.unsqueeze(1).view(-1))
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

            # train_acc += ((torch.sigmoid(logits) > 0.5).float() == labels.unsqueeze(1)).sum().item()
            train_acc += (logits.argmax(dim=1) == labels).sum().item()

        train_loss /= len(train_loader)
        train_acc /= len(train_dataset)

        val_loss = 0
        val_acc = 0
        model.eval()
        with torch.no_grad():
            for input_ids, attention_mask, labels in val_loader:
                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)
                labels = labels.to(device)

                outputs = model(input_ids, attention_mask).last_hidden_state[:, 0]
                logits = classifier(outputs)
                loss = criterion(logits, labels)

                val_loss += loss.item()
                # val_acc += ((torch.sigmoid(logits) > 0.5).float() == labels.unsqueeze(1)).sum().item()
                val_acc += (logits.argmax(dim=1) == labels).sum().item()

            val_loss /= len(val_loader)
            val_acc /= len(val_dataset)

            print(
                f'Epoch {epoch + 1}/{NUM_EPOCHS}: Train Loss={train_loss:.3f}, Train Acc={train_acc:.3f}, Val Loss={val_loss:.3f}, Val Acc={val_acc:.3f}')

        # 测试
        test_data = pd.read_csv('data/test.csv')
        test_dataset = SentimentDataset(test_data, tokenizer)
        test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

        test_loss = 0
        test_acc = 0
        model.eval()
        with torch.no_grad():
            for input_ids, attention_mask, labels in test_loader:
                input_ids = input_ids.to(device)
                attention_mask = attention_mask.to(device)
                labels = labels.to(device)

                outputs = model(input_ids, attention_mask).last_hidden_state[:, 0]
                logits = classifier(outputs)
                loss = criterion(logits, labels)

                test_loss += loss.item()
                test_acc += (logits.argmax(dim=1) == labels).sum().item()

        test_loss /= len(test_loader)
        test_acc /= len(test_dataset)

        print(f'Test Loss: {test_loss:.3f}, Test Acc: {test_acc:.3f}')

        torch.save(model, 'models/save_model.pt')


if __name__ == '__main__':
    main()

