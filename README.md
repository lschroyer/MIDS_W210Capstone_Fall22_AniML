# MIDS_W210Capstone_Fall22_AniML
W210 - Section 7 - AniML Group

Ivan Wong,
Lana Elauria,
Lucas Harvey-Schroyer, 
Whit Blodgett

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


