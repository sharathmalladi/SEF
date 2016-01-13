# SEF

Project description
This is a project that I undertook for a non-profit organization called Sankara Eye Foundation (SEF, www.giftofvision.org).
SEF performs free eye surgeries for the underprivileged people in India.  

This project is a study of a dataset containing the donations made to this organization. The dataset was organized for day-to-day operational use by the organization and my contribution is to extract useful information from this data and help understand it better.

Input dataset
The dataset consists of transactions made by donors to the organization. Each row represents a single transaction. A transaction can be money given towards a fund-raiser or a charitable contribution (donation).

High-level Process
1. Break down each transaction as a fund-raiser or a donation.
2. From the fund-raiser dollars, extract information about the fund-raisers (location, time, size, amount raised).
3. From the donation dollars, extract information about the donors (frequency of donation, amount donated, churn by region).
4. Provide visualizations that are insightful to the organization.
5. Build a web application (hosted in Flask) with an actionable dashboard (this is work in progress).
6. A time-series analysis followed by predictions of the donation amounts into the future.

Folder structure
- notebooks: This folder has ipython notebooks to perform the steps of feature extraction, visualizations and the time-series analysis. The readme under this folder has more detail about the individual notebooks.
- web_app: This folder has the web application.
