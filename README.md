## Options EIKON API APP:

This Project Aims To Explore The Possibility Of Doing Custom Application With The Eikon Data Api And Dash/Plotly. 

It An Opensource Project That Intends To Engage The Community Around The Refinitiv Apis. On The Future, I Intend To Improve The Current Code That Is Now On Version 0.1v. The Application Is 100% Made In Python

### Requirements:
- Eikon installed on the computer.
- Python version 3.6x or greater.

	Libraries:
		dash==0.43.0
		dash_table==3.7.0
		dash_bootstrap_components==0.6.3
		eikon==1.0.0
		json==2.0.9
		pandas==0.24.2
		numpy==1.15.4
		plotly==4.0.0
		scipy==1.1.0


## How it Works:
Create an Eikon API key with the <App Key Generator>app in Eikon.
Run the code: OptionDash.py

## How to use it:

After installing all the dependences you will be able to run the code from the terminal.

<!-- <img src="./assets/cmd.jpeg" alt="Drawing" style="width: 500px"> -->
![alt text](https://github.com/PedroAMBH/Eikon_API_Oprions_Dash_App/blob/master/assets/cmd.jpg?raw=true)


It will automatically open a tab on your Browser:
-	You need to paste the API key (from the API KEY GENERATOR) on the first text box, and submit.
-	On the second text box you should paste the options Chain and submit, it will downloaded the options information from Eikon.

<!-- <img src="./assets/1.jpeg" alt="Drawing" style="width: 500px"> -->
![alt text](https://github.com/PedroAMBH/Eikon_API_Oprions_Dash_App/blob/master/assets/1.jpg?raw=true)

On the ?Options filter? block:
-	Select the maturity?s  you are entrusted in and the number of strikes around the spot price do you want to see and submit.

![alt text](https://github.com/PedroAMBH/Eikon_API_Oprions_Dash_App/blob/master/assets/2.jpg?raw=true)
<!-- <img src="./assets/2.jpeg" alt="Drawing" style="width: 500px"> -->

?	Each of the alternatives is a difference options, presenting the different strikes and maturity's. 


-	When selecting the options on the checkbox?s they will be showed on the table below, where you can tune your strategy on the ?Amount? column.

-	By checking the rows on the Table you will be including the selected options to a strategy profit chart.

![alt text](https://github.com/PedroAMBH/Eikon_API_Oprions_Dash_App/blob/master/assets/3.jpg?raw=true)
<!-- <img src="./assets/3.jpeg" alt="Drawing" style="width: 500px"> -->
