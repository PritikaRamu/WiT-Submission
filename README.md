# Token Management System

#### Short Description
A chatbot to manage a token system to reduce wait time and maintain social distancing while shopping.

#### Long Description
In my apartment complex, to ensure that residents did not have to wait in long lines and to control the number of people at the shop, the management came up with a token system. Physical tokens were handed out on a first come first serve basis. There were few days when the line to collect the physical token was also long. It was a tedious task to constantly look out of the window and inform the next set of token holders. They also had to sanitise the tokens after each use. To make this task easier, I wanted to automate this process with an easy to use application. Instead of making a mobile application, I decided to build a Telegram chatbot as most residents are already on Telegram. This application is written in Python and is deployed in IBM Cloud Foundry. This is how the bot works:
1.	The application is started by the administrator. A message is sent to the Telegram group of the residents informing them that they can request for tokens.
2.	The resident requests for a token by entering a valid flat number into the chatbot. The token number is given on first come first serve basis. One token is given per flat, per user.
3.	By sending certain commands, the resident may know the status of the tokens and the list of residents with the corresponding token numbers, to keep them up to date and give an idea on when to go to the shop.
4.	Once the resident is done with their billing, they send “Done” to the chatbot. This keeps track of how many residents are done with the shopping.
5.	Initially 10 residents go down, once 5 are done with their billing, a message goes to the residents’ group requesting the next 5 to come down. This ensures that only 10 people are at the shop at a time.

Valid commands:

•	Flat number (e.g. D702)    
•	Status – to view how many tokens have been given out and how many are done with billing.      
•	List all – to view the complete list of residents with the corresponding token numbers as well as the tokens that have been collected i.e. done with billing.              
•	Done – this is to be sent when a resident is done with their billing to keep track of how many residents are done and to inform the rest.   
•	/exit – this command can only be used by the administrator to stop the token issue process.  
•	For any invalid command, the bot responds with a list of valid commands.


I tested this with residents on 6th June, 2020. I was surprised to see the amount of token numbers that were allotted within a minute.

