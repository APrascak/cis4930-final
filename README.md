# Final OBS Project - Team 5
* Sydney Achinger
* Alexander Prascak
* Rahul Rudra
* Ganna Voytseshko

### Microservices
Individual implementations in respective branches.  
The Swagger Documentation is [here.](https://app.swaggerhub.com/apis-docs/APrascak/cis-team-5/1.0.0)  
* American Express: https://americanexpressservice.appspot.com/  
* Pinterest: http://pinterestservice.appspot.com/  
* Raytheon:  https://sonorous-bounty-258117.appspot.com/
* Snapchat:  https://firestore-demo-3ebe9.appspot.com
* Uber: https://aqueous-choir-258117.appspot.com/  

### Links
CI server:
OBS deployment:
Swagger Hub API documentation: https://app.swaggerhub.com/apis-docs/APrascak/cis-team-5/1.0.0
Style guides / lint tools: 

### CIS 4930 Final Project Setup
To create the backend of our final project, we wrote our stock microservices in Python and used the Flask micro web framework. To create the frontend of our final project, we wrote the OBS System in JavaScript and used the React library. We used the Google Firebase database for all databases. Each stock micro service stands alone and has its own database to track stock amounts. The OBS System, which tracks user account funds and user action logs, also uses its own Firebase database. For authentication we used the Cloud Firestore REST API. The Firestore authentication uses a Firebase ID token to authenticate users. 

We used GitHub for version control and kept all code in the same repository. The python microservices are stored on separate branches from the frontend code. The python package manager we used is pip and for JavaScript we used npm. We deployed using Google App Engine and user a requirements.txt file to include dependencies for deployment. The continuous integration pipeline we used is Jenkins.


### Firebase Authentication
To run the signup/login script in obs-auth branch: `python obs.py`

### Coverage Reports
![UBER coverage report](https://github.com/APrascak/cis4930-final/blob/uber/uber-coverage-report.png?raw=true)
![AMERICAN EXPRESS coverage report](https://github.com/APrascak/cis4930-final/blob/AmericanExpress/AXP-Coverage.PNG)
![RAYTHEON coverage report](https://github.com/APrascak/cis4930-final/blob/raytheon/coverage.png)
![PINTEREST coverage report](https://github.com/APrascak/cis4930-final/blob/master/Pinterest-Coverage.png)
![image](https://user-images.githubusercontent.com/42813401/69832779-1c287400-11fe-11ea-8f8e-278bafe2786a.png)

