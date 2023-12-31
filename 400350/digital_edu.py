#создай здесь свой индивидуальный проект!
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('train.csv')

df.drop(['id', 'bdate', 'has_photo', 'has_mobile', 'followers_count', 'graduation', 
        'relation', 'life_main', 'people_main', 'city', 'last_seen', 'occupation_name', 
        'career_start', 'career_end'], axis = 1, inplace = True)

#print(df['education_form'].value_counts())
df['education_form'].fillna('Full-time', inplace = True)

df[list(pd.get_dummies(df['education_form']).columns)] = pd.get_dummies(df['education_form'])
df.drop(['education_form'], axis = 1, inplace = True)

#print(df['education_status'].value_counts())

def edu_status_apply(edu_status):
    if edu_status == 'Undergraduate applicant':
        return 0
    elif edu_status == 'Student (Specialist)' or edu_status == "Student (Bachleor's)" or edu_status == "Student (Master's)":
        return 1
    elif edu_status == 'Alumnus (Specialist)' or edu_status == "Alumnus (Bachleor's)" or edu_status == "Alumnus (Master's)":
        return 2
    else:
        return 3

df['education_status'] = df['education_status'].apply(edu_status_apply)

def lang_apply(langs):
    if langs.find('Русский') != -1 and langs.find('English') != -1:
        return 2
    return 1

df['langs'] = df['langs'].apply(lang_apply)

#print(df['occupation_type'].value_counts())

def ocu_type_apply(ocu_type):
    if ocu_type == 'university':
        return 0 
    return 1

df['occupation_type'] = df['occupation_type'].apply(ocu_type_apply)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

x = df.drop('result', axis = 1)
y = df['result']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25)

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

classifier = KNeighborsClassifier(n_neighbors = 3)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)
print('Процент правильно предсказанных исходов', round(accuracy_score(y_test, y_pred) * 100, 2))

###

test = pd.read_csv('test.csv')
ID = test['id']

test.drop(['id', 'bdate', 'has_photo', 'has_mobile', 'followers_count', 'graduation', 
        'relation', 'life_main', 'people_main', 'city', 'last_seen', 'occupation_name', 
        'career_start', 'career_end'], axis = 1, inplace = True)

test['education_form'].fillna('Full-time', inplace = True)

test[list(pd.get_dummies(test['education_form']).columns)] = pd.get_dummies(test['education_form'])
test.drop(['education_form'], axis = 1, inplace = True)

test['education_status'] = test['education_status'].apply(edu_status_apply)
test['langs'] = test['langs'].apply(lang_apply)
test['occupation_type'] = test['occupation_type'].apply(ocu_type_apply)

x_test = sc.transform(test)
y_pred = classifier.predict(x_test)
print(y_pred)
result = pd.DataFrame({'id': ID, 'result': y_pred})
result.to_csv('res.csv', index = False)
