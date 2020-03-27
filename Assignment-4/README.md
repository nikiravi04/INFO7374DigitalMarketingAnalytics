# Snack Recommendation System

## NeuMF: A fusion of GMF and MLP

NCF has 2 components GMF and MLP with the following benefits :
- GMF that applies the linear kernel to model user-item interactions like vanilla MF
- MLP that uses multiple neural layers to layer nonlinear interactions

NCF combines these models together to superimpose their desirable characteristics. NCF concatenates the output of GMF and MLP before feeding them into NeuMF layer.


*Our snack recommendation system recommends unbought snacks by the user and the respective score for the user*

Steps to run the code :

- Run the NCF-Assignment-4 notebook on Jupyter notebook
- We save few user_ids and their recommended snacks in a csv so we can use them for our Streamlit dashboard
- Run the Streamlit-NCF notebook by running the last cell only
- Opens up a streamlit dashboard , where you can choose the user_ids you want to visualize

Following are the graphs displayed in the Streamlit dashboard for a specific user:


