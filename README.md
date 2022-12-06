# MIDS_W210Capstone_Fall22_AniML
W210 - Section 7 - AniML Group

Ivan Wong,
Lana Elauria,
Lucas Harvey-Schroyer, 
Whit Blodgett

Introducing AniML, the no code AI computer vision tool that allows anyone, even those without a technical backgrounds, to easily build and implement their own computer vision systems. Take control of a chaotic image folder by uploading it to the platform where it automatically filters down to images with objects of interest. Label these representative images and easily train your own custom model which you can use to further streamline your workflow. Once trained, AniML models generate a detailed analytics dashboard full of rich insights. 

AniML was originally designed to help biologists automatically sort through hundereds of thousands of field camera images tracking animal populations. Automating this previosuly manual process, AniML frees up biologists' time so they can focus where it counts - applying their unique skills to solve pressing global challenges, such as climate change, disease outbreaks, and food insecurity.




GitHub Repository For Hosting Code for the Web Application - Computer Vision AI Model
EC2 server running FastAPI server
- for running the website locally or in a virtual server (i.e. EC2 AWS):
  - cd fastapi_ui folder
  - pip install -r requirements.txt (only need to do it once)
  - run `python3 -m uvicorn app.main:app --reload --port 8080`
  - the website layout should always be available if one runs it locally however some of the api calls embeded in the website may be inactive

Testing endpoints (only while endpoints are running in EC2)
- http://13.56.94.163:8000/docs
- `curl -o /dev/null -s -w '%{http_code}\n' -X 'GET'  'http://13.56.94.163:8000/docs'  -H 'accept: application/json`


