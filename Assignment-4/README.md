# Snack Recommendation System

## NeuMF: A fusion of GMF and MLP

NCF has 2 components GMF and MLP with the following benefits :
- GMF that applies the linear kernel to model user-item interactions like vanilla MF
- MLP that uses multiple neural layers to layer nonlinear interactions

<img width="962" alt="neuMF" src="https://user-images.githubusercontent.com/46007043/77786892-a5c14480-702c-11ea-83fd-6229de4b69a7.png">

NCF combines these models together to superimpose their desirable characteristics. NCF concatenates the output of GMF and MLP before feeding them into NeuMF layer.


*Our snack recommendation system recommends unbought snacks by the user and the respective score for the user*

Steps to run the code :

- Run the NCF-Assignment-4 notebook on Jupyter notebook
- We save few user_ids and their recommended snacks in a csv so we can use them for our Streamlit dashboard
- Run the Streamlit-NCF notebook by running the last cell only
- Opens up a streamlit dashboard , where you can choose the user_ids you want to visualize

Following are the graphs displayed in the Streamlit dashboard for a specific user:

<img width="749" alt="Screen Shot 2020-03-27 at 12 11 48 PM" src="https://user-images.githubusercontent.com/46007043/77786950-ba9dd800-702c-11ea-83a0-e9a50df42cc9.png">
<img width="802" alt="Screen Shot 2020-03-27 at 12 12 03 PM" src="https://user-images.githubusercontent.com/46007043/77786952-bb366e80-702c-11ea-9557-511612d9cae4.png">
<img width="846" alt="Screen Shot 2020-03-27 at 12 12 13 PM" src="https://user-images.githubusercontent.com/46007043/77786954-bbcf0500-702c-11ea-81e0-bfe2c8260a8b.png">
<img width="873" alt="Screen Shot 2020-03-27 at 12 12 21 PM" src="https://user-images.githubusercontent.com/46007043/77786955-bc679b80-702c-11ea-9c0a-93ef552f07b5.png">
<img width="816" alt="Screen Shot 2020-03-27 at 12 12 40 PM" src="https://user-images.githubusercontent.com/46007043/77786959-bd98c880-702c-11ea-894a-6d35beeefef2.png">
<img width="892" alt="Screen Shot 2020-03-27 at 12 12 50 PM" src="https://user-images.githubusercontent.com/46007043/77786960-be315f00-702c-11ea-8e96-adaa0cbe8b6d.png">
<img width="876" alt="Screen Shot 2020-03-27 at 12 12 58 PM" src="https://user-images.githubusercontent.com/46007043/77786963-bec9f580-702c-11ea-9c3e-90aa22f11366.png">



