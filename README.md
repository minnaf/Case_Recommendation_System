# Case_Recommendation_System


This project seeks to help underprivileged defendants during the trial process by recommending cases similar to their own, thereby empowering them to help in their own criminal justice proceedings. 

By: Minna Fingerhood, 2019

-------------------------------

Outline:

1. Motivation
2. Data Collection & Feature Engineering
3. EDA
4. Recommendation Engine 
5. Further Steps

-----------------------------------------

1. Motivation: 

The American Criminal Justice System is far from just. While algorithims have been deployed in various stages of the system as a means of increasing efficiency and reducing human bias, they  often times overlook the racial prejudice engrained in the system, which becomes intrinsic to the data. Ultimately, this results in algorithims that unintentionally perpetuate inequality. Further, mass incarceration and overworked public defenders further disadvantage poor defendants during the trial process. Therefore, this project seeks to empower underpriviledged defendants during the trial process by providing them with a tool to find cases similar to their own. In doing so, they can learn more about arguements presented by other and perhaps less overworked lawyers. 


2. Data Collection:

This project relied on data collected from the CaseLaw Access Project (CAP):

    The President and Fellows of Harvard University. "Caselaw Access Project." 2018, 
    [https://case.law/about/].
    
I utilized case data from 1970 (the year that the term 'war on drugs' was coined). As of now, I have 15,000 cases from Jan 1 (1970) to Feb (1970). In the near future, I would like to gather cases up until the current date, to get the most accurate of results. 

The most important feature engineering I performed was converting the majority opinion of every case into a vector, through Doc2Vec. Doc2Vec is a shallow neural network that analyzes patterns in the location and distance of words. Each document is turned into a vector (with a length of 300) and can be compared through cosine similarity. I also utilized date as an input, but weighted it much lower than the text vectors (see visual representation below):



Other features were considered, but I ulimtately decided I wanted an engine that returns a broad array of cases, from different types of courts and different locations. jurisdictions. 




3.EDA: 

TSNE plot of words used in the legal corpus: 

 <p align="center">
        <img src="Screen Shot 2019-09-24 at 9.38.49 PM.png">
    </p> 
    
 
 Topic Analysis: 
  <p align="center">
        <img src="Screen Shot 2019-09-24 at 9.39.00 PM.png">
    </p> 
    




4. Recommendation Engine: 

Using my engineered features, I generated a recommendation engine. The inputs for the engine are text from the case (ideally the first couple pages of an arrest report or criminal charge, docuements the defendant is likely to possess), and the date of the case. The engine (hosted on a local plotly dash app) then returns a list of the top 10 cases including the name and the majority opinion. 

  <p align="center">
        <img src="Screen Shot 2019-09-11 at 2.23.52 PM.png">
    </p> 




5. Further Steps:

As previously mentioned, I would like to include the rest of the case data into the recommendation engine. I would also like to include filter options for jurisdiction so that if desired, the defendant can limit the results. Another feature I would like to include is data regarding the judge and the attorneys. This will be useful information from the most recent cases and for county courts as it will enable individuals to learn more about a judge's case history and how they tend to lean in their cases. 







