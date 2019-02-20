# Building an Accounting Fraud Classification Model

## Abstract

[Slides](https://docs.google.com/presentation/d/1zLSNhcjEG1QAUX_T6kX5mTN187Hze6NA68W-U2k29aw/edit#slide=id.g4b294b7a6a_0_6)

I built a Machine Learning model to detect accounting fraud. My model achieved its best metrics with a Gradient Boosting Classifier: .99 AUC; .85 F1 Score; .91 Cross Validation; and .96 Accuracy.

## Motivation

As an accountant, there is so much compliance and regulation you have to comply with in an effort to reduce fraud. But companies and executives continue to commit fraud. This is an excellent opportunity to introduce data science into the mix because it would remove the human element and potentially could be used as 
Sarbanes oxley, enron

## Research

First, I needed to find the companies that had actually committed fraud. I did this by combing through the Securities and Exchange Commission's (SEC) Press Releases for the last 5 years to gather a list of 25 companies that had been accused of fraud by the SEC. There, I had access to the SEC orders which specified which financial statements were deemed fraudulent, when they had previously been filed, and the companies' CIK numbers (a unique identifier assigned each corporation).

## Dataset

Then, I downloaded the [Financial Statement Data Sets](https://www.sec.gov/dera/data/financial-statement-data-sets.html) containing the above mentioned fraudulent filings as well as some non-fraudulent filings.


### Feature Engineering

Once I had my datasets, I added [Benford's Law] (https://medium.com/@erika.russi/benny-and-the-di-gits-e6bb9f40c552) as my first feature. Benford's Law is the "Mathematical theory of leading digits. Specifically, in data sets, the leading digit(s) is (are) distributed in a specific, nonuniform way." 
<p align="center">
<img width="500" alt="Benford's Law" src="https://github.com/Erika-Russi/accounting_fraud_detect/blob/master/images/benford_theory.jpeg">




