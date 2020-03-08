# Criteo Attribution Modeling 

Comparing 5 attribution models and which is the best model amongst the 5 models based on ROI generated based on the blog below 

https://blog.griddynamics.com/cross-channel-marketing-spend-optimization-deep-learning/

### How to run the code

- Run the notebook on google colab as the dataset is large and hence memory intensive on the RAM
- Run the bokeh visulizations on jupyter notebook itself as there is interactivity and google colab does not work with it

### Assumptions made from the dataset

- Every user ID has the same campaign ID which has been used for targeting
- Each user ID has many conversion ID's
- Each conversion ID will have a start of 0 for click_pos all the way to the click_nb value within the 30 days of impression

### Attribution Models

- Time-decay attribution: gives more credit to the touchpoints that are closer in time to the conversion
- Linear attribution: gives equal credit to all touchpoints in the journey
- U-shaped attribution: gives most of the credit to the first and last touchpoints, and some credit to intermediate touchpoints
- First-touch attribution: gives all credit to the first touchpoint in the journey
- Last-touch attribution : gives all credit to the last touchpoint in the journey

### Insights from the models & budget optimization code
- The results confirm that for values below the actual attribution weight (i.e weights below 1), the U-shaped and Linear attribution model shows similar and best performance for budget allocation. 
- Whereas, for values above the actual weights (i.e weight above 1) the FTA and LTA attribution models show similar and better performance. 
- The Time decay attribution model shows a fair performance throughout the different parameter values. 

### Bokeh Visualizations - attribution models and budget optimization for the 5 models

<img width="1015" alt="Screen Shot 2020-03-07 at 3 13 32 PM" src="https://user-images.githubusercontent.com/46007043/76164689-d3e2f100-611e-11ea-8701-522c222c84ed.png">

<img width="1032" alt="Screen Shot 2020-03-07 at 3 13 09 PM" src="https://user-images.githubusercontent.com/46007043/76164691-d6dde180-611e-11ea-97d4-176eae41a2d0.png">

<img width="919" alt="Screen Shot 2020-03-07 at 9 18 23 PM" src="https://user-images.githubusercontent.com/46007043/76164699-ec530b80-611e-11ea-9110-c86763e2585a.png">

#### Citatioon 
When using this dataset, please cite the paper with following bibtex(final ACM bibtex coming soon):

```json
@inproceedings{DiemertMeynet2017,
author = {{Diemert Eustache, Meynet Julien} and Galland, Pierre and Lefortier, Damien},
title={Attribution Modeling Increases Efficiency of Bidding in Display Advertising},
publisher = {ACM},
pages={To appear},
booktitle = {Proceedings of the AdKDD and TargetAd Workshop, KDD, Halifax, NS, Canada, August, 14, 2017},
year = {2017}
}
```

### Data description
This dataset represent a sample of  30 days of Criteo live traffic data.  Each line corresponds to one impression (a banner) that was displayed to a user.
For each banner we have detailed information about the context, if it was clicked, if it led to a conversion and if it led to a conversion that was attributed to Criteo or not. Data has been sub-sampled and anonymized so as not to disclose proprietary elements.

Here is a detailed description of the fields (they are tab-separated in the file):

  * **timestamp**: timestamp of the impression (starting from 0 for the first impression). The dataset is sorted according to timestamp.
  *  **uid** a unique user identifier
  * **campaign** a unique identifier for the campaign
  * **conversion** 1 if there was a conversion in the 30 days after the impression (independently of whether this impression was last click or not)
  * **conversion_timestamp** the timestamp of the conversion or -1 if no conversion was observed
  *	**conversion_id**	a unique identifier for each conversion (so that timelines can be reconstructed if needed). -1 if there was no conversion
  * **attribution** 1 if the conversion was attributed to Criteo, 0 otherwise
  * **click** 1 if the impression was clicked, 0 otherwise
  *	**click_pos** the position of the click before a conversion (0 for first-click)
  * **click_nb** number of clicks. More than 1 if there was several clicks before a conversion
  * **cost** the price paid by Criteo for this display (**disclaimer:** not the real price, only a transformed version of it)
  *	 **cpo** the cost-per-order  in case of attributed conversion (**disclaimer:** not the real price, only a transformed version of it)
  * **time\_since\_last\_click** the time since the last click (in s) for the given impression
  *	 **cat[1-9]** contextual features associated to the display. Can be used to learn the click/conversion models. We do not disclose the meaning of these features but it is not relevant for this study. Each column is a categorical variable. In the experiments, they are mapped to a fixed dimensionality space using the Hashing Trick (see paper for reference).

### Key figures
  * 2,4Gb uncompressed
  * 16.5M impressions
  * 45K conversions
  * 700 campaigns
  
  
   
