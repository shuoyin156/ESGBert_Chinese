import pandas as pd
from sklearn.model_selection import train_test_split

# 读取CSV文件
data_path = './data/'
data = pd.read_csv(data_path+'sample.csv')

# 将pos列和neg列合并成一列，并添加对应的标签
# all_data = pd.DataFrame(columns=['text', 'label'])
# data['text'] = data['pos'].fillna('') + ' ' + data['neg'].fillna('')
# data['label'] = data['pos'].apply(lambda x: 1) + data['neg'].fillna('').apply(lambda x: 0)
# data = data[['text', 'label']]

# 划分数据集为训练集和测试集
data = data.sample(frac=1, random_state=1234).reset_index(drop=True)
train_data, test_data = train_test_split(data, test_size=0.2, random_state=1234)

# 将数据集保存为CSV文件
train_data.to_csv(data_path+'train.csv', index=False)
test_data.to_csv(data_path+'test.csv', index=False)
