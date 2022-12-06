# MIDS_W210Capstone_Fall22_AniML
W210 - Section 7 - AniML Group

Ivan Wong,
Lana Elauria,
Lucas Harvey-Schroyer, 
Whit Blodgett

Introducing the no code AI computer vision tool that allows anyone, even those without a technical background, to easily build and implement their own computer vision systems. With this revolutionary tool, you can quickly and easily create and train powerful AI models that can analyze and understand images and video, all without writing a single line of code. Whether you're a small business owner looking to improve efficiency, a researcher exploring new applications for AI, or simply a tech enthusiast looking to try out the latest advances in computer vision, this no code tool has you covered. With its intuitive user interface and powerful capabilities, you'll be able to build and deploy AI models that can make sense of the world around us like never before. So why wait? Try out this no code AI computer vision tool today and see the amazing things you can create.

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


