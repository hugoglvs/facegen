# FaceGen - A Dell Technologies internship project

To deploy the project on new machines, you can download the setup executable file from [facegen-setup](https://github.com/hugoglvs/facegen/blob/main/facegen-setup.exe) and execute it. 
The only pre-requisite is to have firefox installed.
The installer will normally set-up all the environment needed to deploy the project, it will be installed in Program Files so we reduce the chances to be mistakingly edited by someone. A new executable `Facegen.exe` will then appear on the Desktop.
When running `Facegen.exe`, a PowerShell window will pop and it is where you will see the state of the server, at the same time, a Firefox window will open on the Facegen home page and you are now able to use it !


If you want to edit the source code:

Clone the repo wherever you want it to be without using the setup.exe because as I said before, it will be installed in Program Files which needs admin rights to edit files.
You will have to install `tailwindcss` if you want to change the css and so you will have to install node.js and npm before.
I think it is the only "not explicit" step. All major dependencies of Facegen are registered in `requirements.txt`.
